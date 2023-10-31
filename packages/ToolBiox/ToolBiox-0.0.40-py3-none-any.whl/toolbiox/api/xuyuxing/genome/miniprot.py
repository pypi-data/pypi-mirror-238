import re
from math import ceil
from Bio.Data.CodonTable import standard_dna_table
from toolbiox.lib.common.genome.genome_feature2 import read_gff_file
from toolbiox.lib.common.genome.seq_base import read_fasta, BioSeq
import re


def cs_tag_parser(cs_string, ref_seq_string, ref_start, ref_end):

    ref_seq = ref_seq_string[ref_start-1:ref_end]
    op_sig = set([":", "*", "+", "-", "~"])
    coden_table_dict = standard_dna_table.forward_table

    op_tuples = []
    now = ""
    for i in cs_string:
        if i in op_sig:
            op_tuples.append(now)
            now = i
        else:
            now += i
    op_tuples.append(now)

    p = 0
    out_str = ""
    for op in op_tuples[3:]:
        r = re.findall("\:([0-9]+)", op)
        s = re.findall("\*([acgtn]+)([A-Z*])", op)
        a = re.findall("\+([A-Z]+)", op)
        d = re.findall("\-([acgtn]+)", op)
        i = re.findall("\~([acgtn]{2})([0-9]+)([acgtn]{2})", op)

        if len(r) > 0:
            r = int(r[0])
            # print("r", r)

            out_str += ref_seq[p:p+r]
            p += r

        elif len(s) > 0:
            sub_nuc, ref_aa = s[0]
            # print("s", sub_nuc, ref_aa)

            r_aa = ref_seq[p:p+1]
            p += 1

            if ref_aa != r_aa:
                print("error %s, %s" % (ref_aa, r_aa))

            if sub_nuc.upper() in coden_table_dict:
                out_str += coden_table_dict[sub_nuc.upper()]
            else:
                out_str += "X"

        elif len(a) > 0:
            ref_aa = a[0]
            # print("a", ref_aa)

            p += len(ref_aa)

        elif len(d) > 0:
            sub_nuc = d[0]
            # print("d", sub_nuc)

            if intron_flag:
                sub_nuc = last_sub_nuc + sub_nuc

            for j in range(ceil(len(sub_nuc)/3)):
                j = j*3
                c = sub_nuc[j:j+3]

                if c.upper() in coden_table_dict:
                    out_str += coden_table_dict[c.upper()]
                else:
                    out_str += "X"

        if len(i) > 0:
            iss, il, ie = i[0]
            # print("i", iss, il, ie)

            intron_flag = True
            last_sub_nuc = ""

            if out_str[-1] == 'X':
                out_str = out_str[:-1]
                last_sub_nuc = sub_nuc
        else:
            intron_flag = False
            last_sub_nuc = ""

        # print(out_str)

    return out_str


def miniprot_gff_parser(miniprot_gff, query_fasta=None):

    mRNA_dict = read_gff_file(miniprot_gff)['mRNA']
    if query_fasta:
        query_dict = read_fasta(query_fasta)[0]

    subject_paf_info_dict = {}
    with open(miniprot_gff, 'r') as f:
        for l in f:
            l = l.strip()
            info = l.split()
            if "##PAF" in l:
                paf_info = info
            if len(info) >= 9 and info[2] == 'mRNA':
                subject_id = info[8].split(";")[0].split("=")[1]
                subject_paf_info_dict[subject_id] = paf_info

    miniprot_output_dict = {}
    for subject_id in mRNA_dict:
        sgf = mRNA_dict[subject_id]
        sgf.qualifiers['PAF'] = subject_paf_info_dict[sgf.id]
        cs_string = [i for i in subject_paf_info_dict[sgf.id]
                     if re.match(r'^cs', i)][0]

        query_id = sgf.qualifiers['Target'][0].split()[0]
        query_start = int(sgf.qualifiers['Target'][0].split()[1])
        query_end = int(sgf.qualifiers['Target'][0].split()[2])

        if query_fasta:
            output_string = cs_tag_parser(
                cs_string, query_dict[query_id].seq, query_start, query_end)
        else:
            output_string = None

        sgf.qualifiers['Target'] = query_id
        sgf.qualifiers['Target_Start'] = query_start
        sgf.qualifiers['Target_End'] = query_end
        sgf.qualifiers['Protein'] = output_string
        sgf.qualifiers['Rank'] = int(sgf.qualifiers['Rank'][0])
        sgf.qualifiers['score'] = float(sgf.qualifiers['score'][0])

        miniprot_output_dict.setdefault(query_id, []).append(sgf)

    for q_id in miniprot_output_dict:
        if query_fasta:
            q_seq = query_dict[q_id]
        else:
            q_seq = BioSeq("", seqname=q_id, seq_type='prot')
        s_list = miniprot_output_dict[q_id]

        s_list = sorted(s_list, key=lambda x: x.qualifiers['Rank'])
        q_seq.subjects = s_list

        miniprot_output_dict[q_id] = q_seq

    return miniprot_output_dict


if __name__ == "__main__":
    cs_string = "cs:Z::7*gagP*aagF*aggE:3*gagS:1*gagK*aagC*ttgA*gccT*atgK*gatR:2*atgE*cagM:1*ttgV:1*gagK:1*aggA*aaaM:1+LR*gcgG*atgK*gccT:1*ggaC*gggP*ataN*cagV*gggF:2*cagT*gccS:1*gtcA*ttcP*tctD*caaK*gacE*cagV*aaaC:1*gacE:1*tgcK*aacD*atgY*tttL*gctS*cttM-ggg*gttI*catY*cccM*catN*tccD*attE*aggE*gttA*cccL*tccK*ctcY:2*tccE*aatQ*cccC*cctR*cacD*ttcV*ggS~gt198ag-g+L:1*acgY*gtgL*gaaK*acaK*tacC*acgK*agaA*gaaM*atgI*aggS:1*ttgI*tgcL*gagK*aagG:1*atgL*aagE*tatG*ataL:1*atcV*actG:1+E*aatE:1*aacA*ggcL*gacE*gttA*ttcY*gacM*aggE:1-tttgcgaaggggtgtgtg*cagK:2*aggN*atgL:7*aggN:1*gatE:1*gttT*ttgV:1*cttV*agcG*ccaR:3*gggL*agtA:5*caaL:1*cccD*aatE*ttcI:1-ccgccg:2*cagY*ataV*ctcK*aatV:2*aatG-gaa:1*gtcI*caaE*gttI*cccS*tctP*cttV:1*aatG:9*atcL:1~gt223ag*gtgI:1*actS:2*aaaR:3*gtgA:3*gcgV*gtgM*acgA*gacS*aaaG*gagS*aggK*gacE:1*ctgV:2*gtcP*acaI:1*tatV*gcgS:1*agtR*tacP*gaaH*atgT*gaaM:5*gaaG*atgL:1-acc:2*aacG*ccgK:1*caaV*ttcY*aggG*accR*tacL*aacL*catF:2*ttcY*agcM*aaaA*cacN:1*gttF*accG*agcA*aagG*cttH:3*aaaS:5*aagR*ttcI"
    ref_seq_string = "MALVLENPFPKSLSKTGPTKFSDDGKLLELVVKEGYGVKGMVDSGIAELPQRYIHPPHERIVRKEAIDALCYLAKPIDLSKLGREGGEEVARALCESAEKLGFFQVVNHGVPFELLESMKCATKRFFEMPVEKKAMYLRGKTPCPNVFYGTSFAPDKEVCLEWKDYLSMIYMNDEEALKYWPEQCRDVSLEYLKKCKAMISGILKGLLEGLGVGLEEGALEAYMEAKAVNLNYYPPCPNPELTVGVGRHSDLAALTVLLQDEIGGLYVKVDKGWIEISPVPGALVINVGDTLEILSNGRYKSAEHRVMASGSKERVSIPIFVSPRPHTMIGPLPGLVEDGKAVYGRLLFGEYMANYFGAGHQGKSSLDFARI"
    ref_start = 105
    ref_end = 372

    output_string = "QVVNHGVEKRLLEEMEKLAMDFFMQPLEEKRKYAMAPGGIQGYGQAFVFSQDQKLDWCNMFALGVHPHSIRVPSLWPSNPPHFGETVETYTREMRGLCEKLMKYIGITLNGNGDVFDRAFAKGCVQAVRMNYYPPCPRPDLVLGLSPHSDGSALTVLQQPNFGPPGLQILNDKNEWVQVPSLPNALVINVGDTIEVLTNGKYKSVEHRAVTDKERDRLSIVTFYAPSYEMEIGPLPEMVTEDNPAQFRTYNHGEFSKHYVTSKLQGKKSLDFAKF"

    cs_tag_parser(cs_string, ref_seq_string,
                  ref_start, ref_end) == output_string

    miniprot_gff = "/lustre/home/xuyuxing/tmp/Typha_latifolia/PlantAnno_out/2.BRAKER2/miniprot/Species24.gff"
    query_fasta = "/lustre/home/xuyuxing/Database/OrthoDB/plants/OrthoFinder/Results_Sep23/WorkingDirectory/Species24.fa"

    miniprot_output_dict = miniprot_gff_parser(miniprot_gff, query_fasta)