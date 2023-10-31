from toolbiox.lib.common.genome.genome_feature2 import read_gff_file
import sys

gff_file = sys.argv[1]
gtf_file = sys.argv[2]

gene_dict = read_gff_file(gff_file)['gene']

with open(gtf_file, 'w') as f:
    for gf_id in gene_dict:
        gf = gene_dict[gf_id]
        gene_name = gf.qualifiers['Name'][0]
        f.write("%s\t%s\tgene\t%d\t%d\t.\t%s\t.\tgene_id \"%s\"; gene_name \"%s\"\n" % (gf.chr_id, gf.qualifiers['source'][0], gf.start, gf.end, gf.strand, gene_name, gene_name))

        for sgf in gf.sub_features:
            t_name = sgf.qualifiers['Name'][0]
            f.write("%s\t%s\ttranscript\t%d\t%d\t.\t%s\t.\ttranscript_id \"%s\"; transcript_name \"%s\"; gene_id \"%s\"; gene_name \"%s\"\n" % (gf.chr_id, gf.qualifiers['source'][0], gf.start, gf.end, gf.strand, t_name, t_name, gene_name, gene_name))
            f.write("%s\t%s\texon\t%d\t%d\t.\t%s\t.\ttranscript_id \"%s\"; transcript_name \"%s\"; gene_id \"%s\"; gene_name \"%s\"; exon_id \"%s.1\"\n" % (gf.chr_id, gf.qualifiers['source'][0], gf.start, gf.end, gf.strand, t_name, t_name, gene_name, gene_name, t_name))