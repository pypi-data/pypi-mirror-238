import pysam
import time

def get_pileup_info(pileupcolumn, min_mapping_quality=20, min_base_quality=20):
    # depth = pileupcolumn.nsegments

    base_counts = {}

    for pileupread in pileupcolumn.pileups:
        if not pileupread.is_del and not pileupread.is_refskip:
            read_base = pileupread.alignment.query_sequence[pileupread.query_position]
            base_qual = pileupread.alignment.query_qualities[pileupread.query_position]
            map_qual = pileupread.alignment.mapping_quality

            if map_qual < min_mapping_quality or base_qual < min_base_quality:
                continue

            if read_base not in base_counts:
                base_counts[read_base] = 1
            else:
                base_counts[read_base] += 1

    return base_counts


def get_contig_snps(bamfile, reffile, contig, min_mapping_quality=20, min_base_quality=20, min_depth=2, min_var_freq=0.3):
    """
    :param bamfile: bamfile = pysam.AlignmentFile(sorted_bam_file, "rb")
    :param reffile: reffile = pysam.FastaFile(ref_genome_file)
    :param contig: "scaffold_1"
    :param min_mapping_quality:
    :param min_base_quality:
    :return: 0-based position: {"ref_base": ref_base, "depth": depth, "base_counts": base_counts}
    """

    ref_seq = reffile.fetch(contig)

    snp_dict = {}
    start = time.time()
    for pileupcolumn in bamfile.pileup(contig):
        # report processing
        if time.time() - start > 5:
            print(f"{contig}:{pileupcolumn.reference_pos}")
            start = time.time()

        base_counts = get_pileup_info(
            pileupcolumn, min_mapping_quality, min_base_quality)
        depth = sum(base_counts.values())
        ref_base = ref_seq[pileupcolumn.reference_pos]

        if ref_base not in base_counts:
            base_counts[ref_base] = 0

        try:

            if depth < min_depth:
                continue

            if 1 - base_counts[ref_base] / depth < min_var_freq:
                continue

            snp_dict[pileupcolumn.reference_pos] = {
                "ref_base": ref_base,
                "depth": depth,
                "base_counts": base_counts
            }

        except:
            raise Exception(f"Error: {contig}:{pileupcolumn.reference_pos}")

    return snp_dict

def bcf_filter(input_bcf_file, variant_ratio_threshold=0.3, depth_threshold=2):
    """
    :param input_bcf_file: pysam.VariantFile('input.bcf')
    :param variant_ratio_threshold: 0.3
    :param depth_threshold: 2
    :return:
    """
    input_bcf = pysam.VariantFile(input_bcf_file)

    # chromosome = 'Pjv1Scaffold_0'

    start = time.time()
    num = 0
    record_list = []
    # for record in input_bcf.fetch(chromosome):
    for record in input_bcf.fetch():
        # report processing
        if time.time() - start > 5:
            print("Processing: ", num)
            start = time.time()
        num += 1

        ref_base = record.ref

        alt_count_dict = {}
        for alt in record.alleles:
            if alt == '<*>':
                continue
            alt_count_dict.setdefault(alt, 0)
            alt_count_dict[alt] += record.samples[0]['AD'][record.alleles.index(alt)]

        depth = sum(alt_count_dict.values())
        variant_ratio = 1 - alt_count_dict[ref_base] / depth if depth > 0 else 0

        if variant_ratio > variant_ratio_threshold and depth > depth_threshold:
            record_list.append(record)

    input_bcf.close()

    return record_list

record_list = bcf_filter(input_bcf_file, variant_ratio_threshold=0.3, depth_threshold=2)

import pickle
with open('record_list.pkl', 'wb') as f:
    pickle.dump(record_list, f)

input_bcf_file = "/lustre/home/xuyuxing/Work/Other/Cui/Sample_lane5/lane5.bcf"
output_bcf_file = "/lustre/home/xuyuxing/Work/Other/Cui/Sample_lane5/lane5.f0.3.d2.bcf"

bcf_filter(input_bcf_file, output_bcf_file, variant_ratio_threshold=0.3, depth_threshold=2)

# 打开bcf文件
bcf_file = pysam.VariantFile('/lustre/home/xuyuxing/Work/Other/Cui/Sample_lane5/lane5.bcf')
output_bcf = pysam.VariantFile('output.bcf', 'w', header=input_bcf.header)

# 获取某个位点的变异频率
chromosome = 'Pjv1Scaffold_0'  # 变异位点所在的染色体
position = 98     # 变异位点的位置
variant_ratio_threshold = 0.01  # 变异频率阈值
depth_threshold = 10  # 深度阈值

# 遍历变异位点，查找所需的变异
for record in bcf_file.fetch(chromosome, position-1, position):
    ref_base = record.ref

    alt_count_dict = {}
    for alt in record.alleles:
        if alt == '<*>':
            continue
        alt_count_dict.setdefault(alt, 0)
        alt_count_dict[alt] += record.samples[0]['AD'][record.alleles.index(alt)]

    depth = sum(alt_count_dict.values())
    variant_ratio = 1 - alt_count_dict[ref_base] / depth if depth > 0 else 0

    if variant_ratio > variant_ratio_threshold and depth > depth_threshold:
        output_bcf.write(record)



    print(variant_ratio, depth, alt_count_dict)


import pysam

# 设置阈值（变异频率超过该值的位点将被筛选）
threshold = 0.01

# 打开原始bcf文件
input_bcf = pysam.VariantFile('input.bcf')

# 新建输出bcf文件
output_bcf = pysam.VariantFile('output.bcf', 'w', header=input_bcf.header)

# 遍历每个位点，筛选符合条件的位点并写入到新的bcf文件中
for record in input_bcf.fetch():
    # 计算变异频率
    total_count = sum(record.samples[0]['AD'])
    ref_count = record.samples[0]['AD'][0]
    alt_count = total_count - ref_count
    alt_frequency = alt_count / total_count

    # 判断是否符合条件
    if alt_frequency > threshold:
        output_bcf.write(record)

# 关闭文件
input_bcf.close()
output_bcf.close()



# 打印变异频率
print(f'Mutation frequency at {chromosome}:{position} is {mutation_frequency}')

"""
TAG=$1
REF=$2
R1=$3
R2=$4
CPU=$5

bwa mem -o $TAG.sam -t $CPU $REF $R1 $R2
samtools view -bS -@ $CPU -o $TAG.bam $TAG.sam
samtools fixmate -@ $CPU -r -m $TAG.bam $TAG.fm.bam
samtools sort -@ $CPU -o $TAG.st.fm.bam $TAG.fm.bam
samtools markdup -@ $CPU -r $TAG.st.fm.bam $TAG.ud.st.fm.bam
# samtools mpileup -g -f $REF $TAG.ud.st.fm.bam > $TAG.bcf
samtools mpileup -I -t DP,AD -q 20 -Q 20 -g -o $TAG.bcf -f $REF $TAG.ud.st.fm.bam
bcftools index $TAG.bcf
"""

# samtools index -@ $CPU $TAG.sorted.bam
# rm -rf $TAG.bam
# rm -rf $TAG.sam




if __name__ == "__main__":

    sorted_bam_file = "/lustre/home/xuyuxing/Work/Other/Cui/Sample_lane5/lane5.ud.st.fm.bam"
    ref_genome_file = "/lustre/home/xuyuxing/Work/Other/Cui/Pjreference/PjScaffold_ver1.fasta"

    bamfile = pysam.AlignmentFile(sorted_bam_file, "rb")
    reffile = pysam.FastaFile(ref_genome_file)

    args_list = []
    args_id_list = []
    for contig in bamfile.references:
        args_list.append((bamfile, reffile, contig, 20, 20, 2, 0.3))
        args_id_list.append(contig)


    bamfile.close()
    reffile.close()
