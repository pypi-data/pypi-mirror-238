from Bio.codonalign.codonseq import cal_dn_ds, CodonSeq
from Bio.pairwise2 import align
from Bio.Seq import translate
from collections import namedtuple
from itertools import combinations
from scipy import stats
from toolbiox.config import clustalw_path
from toolbiox.lib.common.math.bin_and_window import split_sequence_to_bins
from toolbiox.lib.common.os import mkdir, rmdir, cmd_run, multiprocess_running
from toolbiox.lib.common.util import time_now
import os
import re
import toolbiox.lib.common.genome.seq_base as fasta
import uuid
import random


def fasta_to_paml(fasta_file, paml_file):
    seqdict, seqname_list = fasta.read_fasta(fasta_file)

    all_length = []
    for i in seqdict:
        record = seqdict[i]
        all_length.append(record.seqs_length())
    all_length = tuple(set(all_length))
    if len(all_length) != 1:
        raise UserWarning

    all_length = all_length[0]
    seq_num = len(seqdict)

    with open(paml_file, 'w') as f:
        f.write("  %d   %d\n\n" % (seq_num, all_length))
        for i in seqdict:
            record = seqdict[i]
            f.write("%s\n%s\n\n" % (record.seqname_short(), record.seq))


# use codeml get positive selection
def codeml_ctl_maker(ctl_file, seqfile, treefile, outfile, model=0, NSsites=0, fix_omega=0, omega=1):
    with open(ctl_file, 'w') as f:
        f.write("""
      seqfile = %s
     treefile = %s
      outfile = %s
        noisy = 9   * 0,1,2,3,9: how much rubbish on the screen
      verbose = 1   * 1: detailed output, 0: concise output
      runmode = 0   * 0: user tree;  1: semi-automatic;  2: automatic
                    * 3: StepwiseAddition; (4,5):PerturbationNNI 

      seqtype = 1   * 1:codons; 2:AAs; 3:codons-->AAs
    CodonFreq = 2   * 0:1/61 each, 1:F1X4, 2:F3X4, 3:codon table
        clock = 0   * 0: no clock, unrooted tree, 1: clock, rooted tree

        model = %d
        * models for codons:
        * 0:one, 1:b, 2:2 or more dN/dS ratios for branches

        NSsites = %d
        icode = 0   * 0:standard genetic code; 1:mammalian mt; 2-10:see below

    fix_kappa = 0   * 1: kappa fixed, 0: kappa to be estimated
        kappa = 2   * initial or fixed kappa

    fix_omega = %d
        omega = %d

    fix_alpha = 1   * 0: estimate gamma shape parameter; 1: fix it at alpha
        alpha = .0  * initial or fixed alpha, 0:infinity (constant rate)
       Malpha = 0   * different alphas for genes
        ncatG = 4   * # of categories in the dG or AdG models of rates

        getSE = 0   * 0: don't want them, 1: want S.E.s of estimates
 RateAncestor = 0   * (1/0): rates (alpha>0) or ancestral states (alpha=0)
       method = 0   * 0: simultaneous; 1: one branch at a time
  fix_blength = 0   * 0: ignore, -1: random, 1: initial, 2: fixed, 3: proportional


    * Specifications for duplicating results for the small data set in table 1
    * of Yang (1998 MBE 15:568-573).
    * see the tree file lysozyme.trees for specification of node (branch) labels

        """ % (seqfile, treefile, outfile, model, NSsites, fix_omega, omega))


def codeml_out_parser(file_name):
    with open(file_name, 'r') as f:
        for each_line in f:
            matchobj = re.match(
                r'^lnL\(ntime:\s+\d+\s+np:\s+(\d+)\):\s+(\S+)\s+.*', each_line)
            if matchobj:
                np, lnL = int(matchobj.group(1)), float(matchobj.group(2))
                return np, lnL


def LRT_test(H0_file, H1_file):
    np0, lnL0 = codeml_out_parser(H0_file)
    np1, lnL1 = codeml_out_parser(H1_file)

    df = np1 - np0
    chi2 = 2*(lnL1 - lnL0)

    pvalue = stats.distributions.chi2.sf(chi2, df)

    return pvalue


# use yn00 get Ka/Ks

def aa_aln_to_cds_aln(aa_aln_fasta, cds_fasta, cds_aln_fasta):
    cmd_string = "treebest backtrans "+aa_aln_fasta+" "+cds_fasta+" > "+cds_aln_fasta
    cmd_run(cmd_string, silence=True)


def yn00_ctl_maker(ctl_file, input_seq_file, output_prefix):
    with open(ctl_file, 'w') as f:
        f.write("""
      seqfile = %s * sequence data file name
      outfile = %s           * main result file
      verbose = 1  * 1: detailed output (list sequences), 0: concise output

        icode = 0  * 0:universal code; 1:mammalian mt; 2-10:see below

    weighting = 0  * weighting pathways between codons (0/1)?
   commonf3x4 = 0  * use one set of codon freqs for all pairs (0/1)?
    *       ndata = 1


    * Genetic codes: 0:universal, 1:mammalian mt., 2:yeast mt., 3:mold mt.,
    * 4: invertebrate mt., 5: ciliate nuclear, 6: echinoderm mt.,
    * 7: euplotid mt., 8: alternative yeast nu. 9: ascidian mt.,
    * 10: blepharisma nu.
    * These codes correspond to transl_table 1 to 11 of GENEBANK.    
    """ % (input_seq_file, output_prefix))


def yn00_runner(input_seq_file, work_dir):
    """
    input_seq_file should is a cds aln in fasta
    """

    mkdir(work_dir, True)
    paml_input_file = work_dir + "/paml_input.nuc"
    ctl_file = work_dir + "/yn00.ctl"

    fasta_to_paml(input_seq_file, paml_input_file)

    yn00_ctl_maker(ctl_file, paml_input_file, "yn_results")

    cmd_run("yn00", cwd=work_dir, silence=True)

    return work_dir + "/yn_results"


def get_dNdS_from_yn00_results(yn00_results_file):
    "dn/ds, dn, ds"

    with open(yn00_results_file, 'r') as f:
        read_flag = False

        NG_info_lines = []

        for each_line in f:
            each_line = each_line.rstrip()

            if re.match(r'^Use runmode.*', each_line):
                read_flag = True
            if re.match(r'^\(B\).*', each_line):
                read_flag = False

            if read_flag and len(each_line) > 0:
                NG_info_lines.append(each_line)

        NG_info_lines = NG_info_lines[1:]

    gene_list = []
    for each_line in NG_info_lines:
        gene_list.append(each_line.split()[0])

    q_index = 0
    d_number_dict = {}
    for each_line in NG_info_lines:
        d_numbers = re.findall(
            '(-?\d+.\d+) \((-?\d+.\d+) (-?\d+.\d+)\)', each_line)
        q_id = gene_list[q_index]
        for s_index in range(len(d_numbers)):
            s_id = gene_list[s_index]
            d_number_dict[(q_id, s_id)] = float(d_numbers[s_index][0]), float(
                d_numbers[s_index][1]), float(d_numbers[s_index][2])
        q_index += 1

    output_dict = {}
    for i in gene_list:
        output_dict[i] = {}
        for j in gene_list:
            if i == j:
                continue
            if (i, j) in d_number_dict:
                output_dict[i][j] = d_number_dict[(i, j)]
            elif (j, i) in d_number_dict:
                output_dict[i][j] = d_number_dict[(j, i)]
            else:
                raise ValueError("Parser error: %s" % yn00_results_file)

    return output_dict


def pairwise_aa_aln_2_cds_aln(gene1, gene2, aa_aln):
    gene1_trans_dict = {}
    for i in range(len(gene1.model_aa_seq)):
        gene1_trans_dict[i] = (gene1.model_aa_seq[i],
                               gene1.model_cds_seq[i*3:i*3+3])

    gene2_trans_dict = {}
    for i in range(len(gene2.model_aa_seq)):
        gene2_trans_dict[i] = (gene2.model_aa_seq[i],
                               gene2.model_cds_seq[i*3:i*3+3])

    Alignment = namedtuple("Alignment", ("seqA, seqB"))

    seqA_cds = ""
    num = 0
    for i in aa_aln.seqA:
        if i == '-':
            seqA_cds += "---"
        if i != '-':
            seqA_cds += gene1_trans_dict[num][1]
            num += 1

    seqB_cds = ""
    num = 0
    for i in aa_aln.seqB:
        if i == '-':
            seqB_cds += "---"
        if i != '-':
            seqB_cds += gene2_trans_dict[num][1]
            num += 1

    return Alignment(seqA_cds, seqB_cds)


def get_dNdS_for_genepair_by_biopython(gene1, gene2, method='YN00'):
    """
    Get dnds via biopython, but get different results than paml

    class abc():
        pass

    gene1 = abc()
    gene1.id = 'T4577N0C002G00364'
    gene1.model_aa_seq = 'MNLWSGGGWSLTSWRTPTTPRRGNSGTRWSGEGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRARCLANCSCVAYAAADVQGGGDDVGTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGTGRLKKETVVLVAAGSTLGFIGLVMLAIFVVQAVRIRRRNLLIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHGLAGRTIAVKRLKPIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDAYIFGTPRERALLNWCRRLQIIQGIADGVKHLHEGEGSAGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTP'
    gene1.model_cds_seq = 'ATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGACGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGCTTTGTCCGTTTGCCGGGAGTGAAGCTGCCAGACACGCTCAACTCGTCGCTGGACACGAGCATCACGTTGGACGAGTGCAGGGCGAGGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTGGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGGACTGGAAGGTTAAAGAAAGAAACGGTGGTTCTCGTAGCAGCTGGATCAACATTGGGTTTCATTGGCCTTGTCATGCTGGCCATCTTCGTTGTGCAGGCGGTTCGCATAAGGCGTCGGAACTTGTTAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGGGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAACCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACGCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGTGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGGCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACACCGTAA'

    gene2 = abc()
    gene2.id = 'T4577N0C002G00365'
    gene2.model_aa_seq = 'MTKTNTMRSHHHGYSHRHCHLLVQSSILLFLGTFAAAQAASDILSKGSNLTNGETLVSANGSFTLGFFTRGVPARRYLGIWFTVANSSSDAVCWVANRDLPLGDTSGVLVISDTGSLVLLDGSGRTAWSSNTTAGAASPTVKLLESGNLVLLDGNGGRDDYDVVKLWQSFDHPTNTLLPGAKIGMNLWSGGGWSLTSWRDADDPSTGEFRYAMVRRGGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRAKCLANCSCVAYAAADVQGGGDDVSTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGRNLIIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHVLAGRTIAVKRLKSIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDSYIFGTPRERALLNWRRRLQIIQGIADGVKHLHEGEGSSGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTAGYMAPEYVQSDGSETTLKCDVYSFGVTLMETLSGRKNCDTPGLVSEAWRLWVGRCVTALLDPAVAPAPAKPELAQLRRCIQVGLLCVQEKPDERPAMSAVVEMLGSPCSELAEPMVPTVVGNAALATLLEADLSRPTVYETIDFR'
    gene2.model_cds_seq = 'ATGACGAAGACGAACACCATGAGAAGCCACCACCATGGATACAGCCACCGCCACTGCCACCTACTCGTACAGTCTTCAATCCTGCTTTTCCTCGGAACTTTTGCCGCCGCACAAGCTGCATCCGACATCCTCAGCAAGGGCAGTAACCTTACTAACGGCGAGACCCTGGTCTCCGCTAACGGGTCGTTCACATTAGGGTTCTTCACTCGCGGCGTGCCGGCAAGGAGGTACCTGGGCATCTGGTTCACGGTGGCCAACTCCAGCAGCGACGCTGTATGCTGGGTGGCGAACCGGGACCTCCCTCTCGGCGACACCTCCGGCGTGCTGGTGATCAGCGACACGGGAAGCCTTGTCCTGCTCGACGGTTCTGGCCGGACGGCGTGGTCTTCGAACACGACTGCAGGCGCCGCTTCCCCGACGGTGAAGCTACTCGAGTCCGGCAACCTCGTCCTGCTCGACGGGAACGGCGGCCGCGACGACTACGACGTGGTGAAGCTGTGGCAGTCGTTCGATCACCCGACGAACACCTTGCTCCCGGGCGCCAAGATCGGCATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGAGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGATGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGGTTTGTCCGTTTGCCGGGAGTGAAGCTGCCCGACACGCTCAACTCGTCGCTGGACACGAGCATCACGCTGGACGAGTGCAGGGCGAAGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTAGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGTCGGAACTTGATAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGTGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAATCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACTCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGCGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGTCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACAGCTGGATACATGGCTCCAGAGTACGTTCAGAGCGACGGTAGCGAGACGACGCTCAAGTGCGACGTGTATAGCTTCGGAGTCACTTTAATGGAGACACTGAGCGGACGAAAGAACTGTGACACGCCAGGCCTCGTCTCAGAAGCCTGGAGACTCTGGGTGGGCCGCTGCGTCACGGCACTCCTTGATCCAGCGGTTGCACCGGCGCCTGCCAAGCCCGAGCTTGCGCAACTGCGCAGGTGCATCCAGGTCGGCCTCCTCTGCGTCCAGGAGAAGCCGGACGAGAGGCCCGCCATGTCCGCGGTTGTCGAGATGCTAGGCAGCCCCTGCTCGGAGCTTGCCGAGCCCATGGTGCCGACGGTCGTCGGCAATGCAGCCTTGGCTACTCTCCTGGAGGCCGATCTCTCCAGACCGACGGTGTACGAGACAATCGATTTTAGATAA'

    """

    gene1.model_aa_seq = translate(
        gene1.model_cds_seq, to_stop=False).replace("*", "")
    gene2.model_aa_seq = translate(
        gene2.model_cds_seq, to_stop=False).replace("*", "")

    aa_aln = align.localxx(
        gene1.model_aa_seq, gene2.model_aa_seq, one_alignment_only=True)[0]
    cds_aln = pairwise_aa_aln_2_cds_aln(gene1, gene2, aa_aln)

    code1 = CodonSeq(cds_aln.seqA)
    code2 = CodonSeq(cds_aln.seqB)

    dN, dS = cal_dn_ds(code1, code2, method=method)

    return dN, dS


def quick_get_dNdS_one(tag, aa_fasta_file, cds_fasta_file, work_dir):
    aa_aln_file = os.path.join(work_dir, tag + ".aa.aln")
    cmd_string = clustalw_path + \
        " -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=protein" % (
            aa_fasta_file, aa_aln_file)
    cmd_run(cmd_string, silence=True)

    cds_aln_file = os.path.join(work_dir, tag + ".cds.aln")
    aa_aln_to_cds_aln(aa_aln_file, cds_fasta_file, cds_aln_file)

    results_file = yn00_runner(cds_aln_file, work_dir)

    dn_ds_dict = get_dNdS_from_yn00_results(results_file)

    return dn_ds_dict

def get_dNdS(gene_list, work_dir=None, debug=False):

    if work_dir is None:
        work_dir = "/run/user/%d/%s_%d" % (os.getuid(),
                                           uuid.uuid1().hex, int(random.random()*1000000))
    mkdir(work_dir, False)

    try:
        num = 0
        rename_dict = {}
        
        for gene in gene_list:
            rename_dict[gene.id] = "gene%d" % num
            num += 1

        aa_fasta_file = os.path.join(work_dir, "aa.fasta")
        with open(aa_fasta_file, 'w') as f:
            for gene in gene_list:
                f.write(">%s\n%s\n" % (rename_dict[gene.id], gene.model_aa_seq))

        cds_fasta_file = os.path.join(work_dir, "cds.fasta")
        with open(cds_fasta_file, 'w') as f:
            for gene in gene_list:
                f.write(">%s\n%s\n" % (rename_dict[gene.id], gene.model_cds_seq))

        aa_aln_file = os.path.join(work_dir, "aa.aln")
        cmd_string = clustalw_path + \
            " -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=protein" % (
                aa_fasta_file, aa_aln_file)
        
        cmd_run(cmd_string, silence=True)

        cds_aln_file = work_dir + "/cds.aln.fasta"
        aa_aln_to_cds_aln(aa_aln_file, cds_fasta_file, cds_aln_file)

        results_file = yn00_runner(cds_aln_file, work_dir)

        dn_ds_dict = get_dNdS_from_yn00_results(results_file)
        
        output_dict = {}
        for gp in combinations([gene.id for gene in gene_list], 2):
            gp = tuple(sorted(gp))
            if not gp in output_dict:
                output_dict[gp] = dn_ds_dict[rename_dict[gp[0]]][rename_dict[gp[1]]]
    except:
        pass

    if debug is False:
        rmdir(work_dir)

    return output_dict

def quick_get_dNdS_many(list_of_gene_list, work_dir=None, debug=False, threads=56, job_split=100000):
    if work_dir is None:
        work_dir = os.path.join("/tmp", uuid.uuid1().hex)
    mkdir(work_dir, False)

    tag_dict = {}
    output_dict = {}
    for i, s, e in split_sequence_to_bins(len(list_of_gene_list), job_split):
        print("%s parse: %d in %d" % (time_now(), e, len(list_of_gene_list)))

        sub_work_dir = os.path.join(work_dir, uuid.uuid1().hex)
        mkdir(sub_work_dir, False)

        # tag
        tag_list = []
        for gene_list in list_of_gene_list[s-1:e]:
            tag = uuid.uuid1().hex
            tag_work_dir = os.path.join(sub_work_dir, tag)
            mkdir(tag_work_dir, False)
            tag_dict[tag] = gene_list
            tag_list.append(tag)

        # clustalw
        args_list = []
        for tag in tag_list:
            gene_list = tag_dict[tag]
            tag_work_dir = os.path.join(sub_work_dir, tag)

            rename_file = os.path.join(tag_work_dir, "rename.map")
            num = 0
            rename_dict = {}
            with open(rename_file, 'w') as f:
                for gene in gene_list:
                    f.write("%s\tgene%d\n" % (gene.id, num))
                    rename_dict[gene.id] = "gene%d" % num
                    num += 1

            aa_fasta_file = os.path.join(tag_work_dir, "aa.fasta")
            with open(aa_fasta_file, 'w') as f:
                for gene in gene_list:
                    f.write(">%s\n%s\n" % (rename_dict[gene.id], gene.model_aa_seq))

            cds_fasta_file = os.path.join(tag_work_dir, "cds.fasta")
            with open(cds_fasta_file, 'w') as f:
                for gene in gene_list:
                    f.write(">%s\n%s\n" % (rename_dict[gene.id], gene.model_cds_seq))

            aa_aln_file = os.path.join(tag_work_dir, "aa.aln")
            cmd_string = clustalw_path + \
                " -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=protein" % (
                    aa_fasta_file, aa_aln_file)
            args_list.append((cmd_string, tag_work_dir, 1, True, None))

        multiprocess_running(cmd_run, args_list, threads)

        # aa_aln_2_cds_aln
        args_list = []
        for tag in tag_list:
            gene_list = tag_dict[tag]
            tag_work_dir = os.path.join(sub_work_dir, tag)

            aa_aln_file = os.path.join(tag_work_dir, "aa.aln")
            cds_fasta_file = os.path.join(tag_work_dir, "cds.fasta")
            cds_aln_file = os.path.join(tag_work_dir, "cds.aln")

            args_list.append((aa_aln_file, cds_fasta_file, cds_aln_file))

        multiprocess_running(aa_aln_to_cds_aln, args_list, threads)

        # yn00
        args_list = []
        for tag in tag_list:
            tag_work_dir = os.path.join(sub_work_dir, tag)

            cds_aln_file = os.path.join(tag_work_dir, "cds.aln")
            paml_input_file = os.path.join(tag_work_dir, "paml_input.nuc")
            fasta_to_paml(cds_aln_file, paml_input_file)

            ctl_file = os.path.join(tag_work_dir, "yn00.ctl")
            yn00_ctl_maker(ctl_file, paml_input_file, "yn_results")

            args_list.append(("yn00", tag_work_dir, 1, True, None))

        multiprocess_running(cmd_run, args_list, threads)

        # load
        for tag in tag_list:
            tag_work_dir = os.path.join(sub_work_dir, tag)
            yn_results_file = os.path.join(tag_work_dir, "yn_results")
            yn_results_dict = get_dNdS_from_yn00_results(yn_results_file)
            rename_file = os.path.join(tag_work_dir, "rename.map")

            rename_dict = {}
            with open(rename_file, 'r') as f:
                for l in f:
                    l = l.strip()
                    raw_name, new_name = l.split()
                    rename_dict[raw_name] = new_name

            gene_list = tag_dict[tag]
            for gp in combinations([gene.id for gene in gene_list], 2):
                gp = tuple(sorted(gp))
                if not gp in output_dict:
                    output_dict[gp] = yn_results_dict[rename_dict[gp[0]]][rename_dict[gp[1]]]

        if debug is False:
            rmdir(sub_work_dir)

    if debug is False:
        rmdir(work_dir)

    return output_dict


def quick_get_dNdS(gene_list, work_dir=None, debug=False):
    """
    gene_list is a list of Gene object, should have attrs: gene.id, gene.model_cds_seq and gene.model_aa_seq

    class abc():
        pass

    gene1 = abc()
    gene1.id = 'T4577N0C002G00364'
    gene1.model_aa_seq = 'MNLWSGGGWSLTSWRTPTTPRRGNSGTRWSGEGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRARCLANCSCVAYAAADVQGGGDDVGTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGTGRLKKETVVLVAAGSTLGFIGLVMLAIFVVQAVRIRRRNLLIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHGLAGRTIAVKRLKPIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDAYIFGTPRERALLNWCRRLQIIQGIADGVKHLHEGEGSAGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTP'
    gene1.model_cds_seq = 'ATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGACGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGCTTTGTCCGTTTGCCGGGAGTGAAGCTGCCAGACACGCTCAACTCGTCGCTGGACACGAGCATCACGTTGGACGAGTGCAGGGCGAGGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTGGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGGACTGGAAGGTTAAAGAAAGAAACGGTGGTTCTCGTAGCAGCTGGATCAACATTGGGTTTCATTGGCCTTGTCATGCTGGCCATCTTCGTTGTGCAGGCGGTTCGCATAAGGCGTCGGAACTTGTTAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGGGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAACCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACGCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGTGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGGCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACACCGTAA'

    gene2 = abc()
    gene2.id = 'T4577N0C002G00365'
    gene2.model_aa_seq = 'MTKTNTMRSHHHGYSHRHCHLLVQSSILLFLGTFAAAQAASDILSKGSNLTNGETLVSANGSFTLGFFTRGVPARRYLGIWFTVANSSSDAVCWVANRDLPLGDTSGVLVISDTGSLVLLDGSGRTAWSSNTTAGAASPTVKLLESGNLVLLDGNGGRDDYDVVKLWQSFDHPTNTLLPGAKIGMNLWSGGGWSLTSWRDADDPSTGEFRYAMVRRGGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRAKCLANCSCVAYAAADVQGGGDDVSTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGRNLIIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHVLAGRTIAVKRLKSIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDSYIFGTPRERALLNWRRRLQIIQGIADGVKHLHEGEGSSGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTAGYMAPEYVQSDGSETTLKCDVYSFGVTLMETLSGRKNCDTPGLVSEAWRLWVGRCVTALLDPAVAPAPAKPELAQLRRCIQVGLLCVQEKPDERPAMSAVVEMLGSPCSELAEPMVPTVVGNAALATLLEADLSRPTVYETIDFR'
    gene2.model_cds_seq = 'ATGACGAAGACGAACACCATGAGAAGCCACCACCATGGATACAGCCACCGCCACTGCCACCTACTCGTACAGTCTTCAATCCTGCTTTTCCTCGGAACTTTTGCCGCCGCACAAGCTGCATCCGACATCCTCAGCAAGGGCAGTAACCTTACTAACGGCGAGACCCTGGTCTCCGCTAACGGGTCGTTCACATTAGGGTTCTTCACTCGCGGCGTGCCGGCAAGGAGGTACCTGGGCATCTGGTTCACGGTGGCCAACTCCAGCAGCGACGCTGTATGCTGGGTGGCGAACCGGGACCTCCCTCTCGGCGACACCTCCGGCGTGCTGGTGATCAGCGACACGGGAAGCCTTGTCCTGCTCGACGGTTCTGGCCGGACGGCGTGGTCTTCGAACACGACTGCAGGCGCCGCTTCCCCGACGGTGAAGCTACTCGAGTCCGGCAACCTCGTCCTGCTCGACGGGAACGGCGGCCGCGACGACTACGACGTGGTGAAGCTGTGGCAGTCGTTCGATCACCCGACGAACACCTTGCTCCCGGGCGCCAAGATCGGCATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGAGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGATGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGGTTTGTCCGTTTGCCGGGAGTGAAGCTGCCCGACACGCTCAACTCGTCGCTGGACACGAGCATCACGCTGGACGAGTGCAGGGCGAAGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTAGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGTCGGAACTTGATAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGTGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAATCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACTCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGCGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGTCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACAGCTGGATACATGGCTCCAGAGTACGTTCAGAGCGACGGTAGCGAGACGACGCTCAAGTGCGACGTGTATAGCTTCGGAGTCACTTTAATGGAGACACTGAGCGGACGAAAGAACTGTGACACGCCAGGCCTCGTCTCAGAAGCCTGGAGACTCTGGGTGGGCCGCTGCGTCACGGCACTCCTTGATCCAGCGGTTGCACCGGCGCCTGCCAAGCCCGAGCTTGCGCAACTGCGCAGGTGCATCCAGGTCGGCCTCCTCTGCGTCCAGGAGAAGCCGGACGAGAGGCCCGCCATGTCCGCGGTTGTCGAGATGCTAGGCAGCCCCTGCTCGGAGCTTGCCGAGCCCATGGTGCCGACGGTCGTCGGCAATGCAGCCTTGGCTACTCTCCTGGAGGCCGATCTCTCCAGACCGACGGTGTACGAGACAATCGATTTTAGATAA'

    gene_list = [gene1, gene2]
    """
    if work_dir is None:
        work_dir = "/run/user/%d/%s_%d" % (os.getuid(),
                                           uuid.uuid1().hex, int(random.random()*1000000))
    mkdir(work_dir, False)

    try:
        aa_fasta_file = work_dir + "/aa.fasta"
        with open(aa_fasta_file, 'w') as f:
            for gene in gene_list:
                f.write(">%s\n%s\n" % (gene.id, gene.model_aa_seq))

        cds_fasta_file = work_dir + "/cds.fasta"
        with open(cds_fasta_file, 'w') as f:
            for gene in gene_list:
                f.write(">%s\n%s\n" % (gene.id, gene.model_cds_seq))

        aa_aln_file = work_dir + "/aa.aln.fasta"
        cmd_string = clustalw_path + \
            " -INFILE=%s -ALIGN -OUTPUT=FASTA -OUTFILE=%s -type=protein" % (
                aa_fasta_file, aa_aln_file)
        cmd_run(cmd_string, silence=True)

        cds_aln_file = work_dir + "/cds.aln.fasta"
        aa_aln_to_cds_aln(aa_aln_file, cds_fasta_file, cds_aln_file)

        results_file = yn00_runner(cds_aln_file, work_dir)

        dn_ds_dict = get_dNdS_from_yn00_results(results_file)

    except:
        dn_ds_dict = {}

    if debug is False:
        rmdir(work_dir)

    return dn_ds_dict


if __name__ == '__main__':
    aa_aln_fasta = "/lustre/home/xuyuxing/Program/paml4.9g/test/OG0023783.aa.aln"
    cds_fasta = "/lustre/home/xuyuxing/Program/paml4.9g/test/OG0023783.cds.fa"
    cds_aln_fasta = "/lustre/home/xuyuxing/Program/paml4.9g/test/OG0023783.cds.aln"

    aa_aln_to_cds_aln(aa_aln_fasta, cds_fasta, cds_aln_fasta)

    cds_aln_paml = "/lustre/home/xuyuxing/Program/paml4.9g/test/OG0023783.cds.aln.paml"
    fasta_to_paml(cds_aln_fasta, cds_aln_paml)

    work_dir = "/lustre/home/xuyuxing/Program/paml4.9g/test/test"
    results_file = yn00_runner(cds_aln_fasta, work_dir)

    dn_ds_dict = get_dNdS_from_yn00_results(results_file)

    #
    class abc():
        pass

    gene1 = abc()
    gene1.id = 'T4577N0C002G00364'
    gene1.model_aa_seq = 'MNLWSGGGWSLTSWRTPTTPRRGNSGTRWSGEGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRARCLANCSCVAYAAADVQGGGDDVGTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGTGRLKKETVVLVAAGSTLGFIGLVMLAIFVVQAVRIRRRNLLIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHGLAGRTIAVKRLKPIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDAYIFGTPRERALLNWCRRLQIIQGIADGVKHLHEGEGSAGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTP'
    gene1.model_cds_seq = 'ATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGACGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGCTTTGTCCGTTTGCCGGGAGTGAAGCTGCCAGACACGCTCAACTCGTCGCTGGACACGAGCATCACGTTGGACGAGTGCAGGGCGAGGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTGGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGGACTGGAAGGTTAAAGAAAGAAACGGTGGTTCTCGTAGCAGCTGGATCAACATTGGGTTTCATTGGCCTTGTCATGCTGGCCATCTTCGTTGTGCAGGCGGTTCGCATAAGGCGTCGGAACTTGTTAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGGGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAACCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACGCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGTGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGGCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACACCGTAA'

    gene2 = abc()
    gene2.id = 'T4577N0C002G00365'
    gene2.model_aa_seq = 'MTKTNTMRSHHHGYSHRHCHLLVQSSILLFLGTFAAAQAASDILSKGSNLTNGETLVSANGSFTLGFFTRGVPARRYLGIWFTVANSSSDAVCWVANRDLPLGDTSGVLVISDTGSLVLLDGSGRTAWSSNTTAGAASPTVKLLESGNLVLLDGNGGRDDYDVVKLWQSFDHPTNTLLPGAKIGMNLWSGGGWSLTSWRDADDPSTGEFRYAMVRRGGLLPEIVMLDSSDAIKYRTGVWNGRWFSGIPEMNSYSNMFVFHVTVSQSEVSFSYAANAGAPPSLSRVLLNYTAEAVRVVWVPDKRGWANFFTGPREDCDHYNRCGHSGVCNQTAASTAWPCSCVQGFVPVSSSDWDGRDPSGGCRRNVSLDCGDNGTTDGFVRLPGVKLPDTLNSSLDTSITLDECRAKCLANCSCVAYAAADVQGGGDDVSTGCIMWPENLTDLRYVAGGQTLYLRQATPPSGRNLIIQMTEAVETAQDPSVSSIALATVKSATRNFSTRNVIGEGTFGIVYEGKLPRGHPLLHVLAGRTIAVKRLKSIGDLPDIIVRYFTREMQLMSGLKQHRNVLRLLAYCDEASERILVYEYMHRRSLDSYIFGTPRERALLNWRRRLQIIQGIADGVKHLHEGEGSSGNVIHRDLKPANVLLDGGWQAKVADFGTAKLLVAGATGTRTRIGTAGYMAPEYVQSDGSETTLKCDVYSFGVTLMETLSGRKNCDTPGLVSEAWRLWVGRCVTALLDPAVAPAPAKPELAQLRRCIQVGLLCVQEKPDERPAMSAVVEMLGSPCSELAEPMVPTVVGNAALATLLEADLSRPTVYETIDFR'
    gene2.model_cds_seq = 'ATGACGAAGACGAACACCATGAGAAGCCACCACCATGGATACAGCCACCGCCACTGCCACCTACTCGTACAGTCTTCAATCCTGCTTTTCCTCGGAACTTTTGCCGCCGCACAAGCTGCATCCGACATCCTCAGCAAGGGCAGTAACCTTACTAACGGCGAGACCCTGGTCTCCGCTAACGGGTCGTTCACATTAGGGTTCTTCACTCGCGGCGTGCCGGCAAGGAGGTACCTGGGCATCTGGTTCACGGTGGCCAACTCCAGCAGCGACGCTGTATGCTGGGTGGCGAACCGGGACCTCCCTCTCGGCGACACCTCCGGCGTGCTGGTGATCAGCGACACGGGAAGCCTTGTCCTGCTCGACGGTTCTGGCCGGACGGCGTGGTCTTCGAACACGACTGCAGGCGCCGCTTCCCCGACGGTGAAGCTACTCGAGTCCGGCAACCTCGTCCTGCTCGACGGGAACGGCGGCCGCGACGACTACGACGTGGTGAAGCTGTGGCAGTCGTTCGATCACCCGACGAACACCTTGCTCCCGGGCGCCAAGATCGGCATGAACCTGTGGAGCGGCGGCGGGTGGTCACTCACGTCGTGGCGGGACGCCGACGACCCCTCGACGGGGGAATTCCGGTACGCGATGGTCAGGCGAGGAGGGTTGCTGCCCGAGATCGTGATGCTGGACTCGAGCGATGCCATCAAGTACCGCACGGGAGTGTGGAACGGGCGGTGGTTCAGCGGCATCCCGGAGATGAACTCGTACTCGAACATGTTCGTCTTCCATGTGACGGTGAGCCAGAGCGAGGTCAGCTTCAGCTACGCCGCCAATGCCGGCGCGCCGCCATCCCTTTCCCGCGTCCTCCTCAACTACACGGCTGAGGCCGTGCGCGTCGTGTGGGTGCCGGACAAGCGAGGGTGGGCAAACTTCTTCACGGGACCCCGAGAAGACTGCGACCACTACAACAGGTGCGGGCACTCTGGCGTGTGCAATCAGACTGCAGCGTCGACGGCGTGGCCGTGCAGCTGTGTCCAGGGCTTCGTCCCCGTCTCGTCGTCGGACTGGGACGGGAGAGACCCATCTGGCGGGTGCCGGCGGAACGTGTCGCTGGACTGCGGCGACAATGGCACCACGGACGGGTTTGTCCGTTTGCCGGGAGTGAAGCTGCCCGACACGCTCAACTCGTCGCTGGACACGAGCATCACGCTGGACGAGTGCAGGGCGAAGTGCCTTGCCAACTGCTCCTGCGTGGCGTATGCCGCGGCAGATGTGCAAGGCGGAGGCGATGATGTTAGCACTGGATGCATCATGTGGCCTGAAAACCTCACTGACCTACGCTACGTGGCTGGAGGACAGACCCTGTACCTACGGCAGGCTACTCCCCCATCTGGTCGGAACTTGATAATTCAAATGACGGAGGCAGTTGAAACAGCCCAAGATCCCTCTGTTTCTTCCATTGCTCTGGCTACTGTCAAGAGTGCAACAAGGAATTTCTCCACAAGGAATGTGATAGGCGAAGGCACTTTCGGCATCGTATATGAGGGCAAGTTGCCCAGAGGGCATCCGCTCCTACACGTGCTAGCCGGGAGAACCATTGCCGTGAAGAGGCTGAAATCGATCGGCGATCTTCCGGACATAATCGTCAGGTATTTCACGAGAGAGATGCAGCTCATGTCCGGGCTCAAGCAGCACCGGAATGTGCTCCGCCTCCTTGCCTACTGCGACGAAGCCAGCGAACGGATCCTGGTGTACGAGTACATGCACAGGAGGAGCTTGGACTCCTACATATTCGGAACACCTAGAGAACGCGCGCTGCTGAACTGGCGCCGGAGGCTGCAGATCATTCAGGGGATCGCCGACGGCGTGAAGCACCTCCACGAGGGAGAAGGGTCGTCCGGCAACGTGATCCACCGGGATCTGAAGCCGGCCAATGTGCTGCTGGACGGCGGATGGCAGGCCAAGGTGGCCGACTTCGGGACAGCAAAATTGCTCGTCGCTGGAGCTACCGGAACTCGGACAAGGATAGGCACAGCTGGATACATGGCTCCAGAGTACGTTCAGAGCGACGGTAGCGAGACGACGCTCAAGTGCGACGTGTATAGCTTCGGAGTCACTTTAATGGAGACACTGAGCGGACGAAAGAACTGTGACACGCCAGGCCTCGTCTCAGAAGCCTGGAGACTCTGGGTGGGCCGCTGCGTCACGGCACTCCTTGATCCAGCGGTTGCACCGGCGCCTGCCAAGCCCGAGCTTGCGCAACTGCGCAGGTGCATCCAGGTCGGCCTCCTCTGCGTCCAGGAGAAGCCGGACGAGAGGCCCGCCATGTCCGCGGTTGTCGAGATGCTAGGCAGCCCCTGCTCGGAGCTTGCCGAGCCCATGGTGCCGACGGTCGTCGGCAATGCAGCCTTGGCTACTCTCCTGGAGGCCGATCTCTCCAGACCGACGGTGTACGAGACAATCGATTTTAGATAA'

    gene_list = [gene1, gene2]

    quick_get_dNdS(gene_list, debug=True)

    get_dNdS_for_genepair(gene1, gene2, method='YN00')
