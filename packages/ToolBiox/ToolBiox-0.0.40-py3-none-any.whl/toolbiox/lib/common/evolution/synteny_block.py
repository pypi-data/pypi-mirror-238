from collections import OrderedDict
from interlap import InterLap
from itertools import combinations
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from toolbiox.lib.common.genome.genome_feature2 import read_gff_file, GenomeFeature
from toolbiox.lib.common.genome.seq_base import read_fasta_by_faidx
from toolbiox.lib.common.math.interval import merge_intervals, section
from toolbiox.lib.common.math.set import merge_same_element_set
from toolbiox.lib.common.os import multiprocess_running
import math
import matplotlib.patches as Patches
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.transforms as mtransforms
import pandas as pd
import re


class GeneLoci(GenomeFeature):
    def __init__(self, gene_id, chr_id, loci, species=None, gf=None):
        if gf:
            gf.sp_id = species
            gf.chr_id = chr_id
            gf.id = gene_id
            super(
                GeneLoci,
                self).__init__(
                id=gene_id,
                chr_loci=gf,
                sp_id=gf.sp_id,
                type=gf.type,
                qualifiers=gf.qualifiers,
                sub_features=gf.sub_features)
        else:
            super(
                GeneLoci,
                self).__init__(
                id=gene_id,
                type=None,
                chr_loci=None,
                qualifiers={},
                sub_features=None,
                chr_id=chr_id,
                strand=None,
                start=None,
                end=None,
                sp_id=species)
        self.loci = loci
        self.gf = gf

    def __str__(self):
        return "%s: No. %d gene on %s from %s" % (
            self.id, self.loci, self.chr_id, self.sp_id)


class Genome(object):
    def __init__(self, species_prefix, gff3_file=None, fasta_file=None):
        self.chr_dict = {}
        self.gene_dict = {}
        self.chr_length_dict = {}
        self.id = species_prefix

        if gff3_file:
            gff_dict = read_gff_file(gff3_file)

            chr_dict = {}
            gene_dict = {}
            for i in gff_dict['gene']:
                gf = gff_dict['gene'][i]
                if gf.chr_id not in chr_dict:
                    chr_dict[gf.chr_id] = []
                chr_dict[gf.chr_id].append(gf)
                gene_dict[gf.id] = gf

            for chr_id in chr_dict:
                chr_dict[chr_id] = sorted(
                    chr_dict[chr_id], key=lambda x: x.start)

            chr_gene_id_dict = {}
            for chr_id in chr_dict:
                chr_gene_id_dict[chr_id] = [i.id for i in chr_dict[chr_id]]

            self.chr_dict = {}
            self.gene_dict = {}
            for chr_id in chr_gene_id_dict:
                num = 0
                self.chr_dict[chr_id] = OrderedDict()
                for gene_id in chr_gene_id_dict[chr_id]:
                    gene = GeneLoci(gene_id, chr_id, num,
                                    species_prefix, gene_dict[gene_id])
                    self.chr_dict[chr_id][num] = gene
                    self.gene_dict[gene_id] = gene
                    num += 1

            self.chr_length_dict = {}
            if fasta_file:
                fa_dict = read_fasta_by_faidx(fasta_file)
                self.chr_length_dict = {i: fa_dict[i].len() for i in fa_dict}
            else:
                for chr_id in self.chr_dict:
                    self.chr_length_dict[chr_id] = max(
                        [self.chr_dict[chr_id][i].end for i in self.chr_dict[chr_id]])

            self.chr_gene_number_dict = {}
            for chr_id in self.chr_dict:
                self.chr_gene_number_dict[chr_id] = len(
                    self.chr_dict[chr_id])


class GenePair(object):
    def __init__(self, q_gene, s_gene, property_dict=None):
        self.q_gene = q_gene
        self.s_gene = s_gene
        self.property = property_dict

    def __str__(self):
        return "%s vs %s" % (self.q_gene.id, self.s_gene.id)

    def reverse_myself(self):
        new_GP = GenePair(self.s_gene, self.q_gene, self.property)
        return new_GP


class GenomeBlock(object):
    def __init__(
            self,
            gb_id=None,
            sp_id=None,
            chr_id=None,
            first_gene=None,
            last_gene=None,
            gene_list=None,
            property_dict=None):
        self.id = gb_id
        self.sp_id = sp_id
        self.chr_id = chr_id
        self.first_gene = first_gene
        self.last_gene = last_gene
        self.gene_list = gene_list
        self.property = property_dict

    def get_full_info(self, genome=None):
        full_info_flag = True
        if isinstance(self.first_gene, GeneLoci):
            self.start = self.first_gene.start
        if isinstance(self.last_gene, GeneLoci):
            self.end = self.last_gene.end
        if isinstance(self.gene_list, list):
            for gene in self.gene_list:
                if not isinstance(gene, GeneLoci):
                    full_info_flag = False
        else:
            full_info_flag = False

        if full_info_flag is False and genome is None:
            raise Exception("GenomeBlock is not full info and genome is None")

        if full_info_flag is False:
            self.first_gene = self.get_gene(self.first_gene, genome)
            self.last_gene = self.get_gene(self.last_gene, genome)

            self.gene_list = []
            for i in range(self.first_gene.loci, self.last_gene.loci + 1):
                self.gene_list.append(genome.chr_dict[self.chr_id][i])

            self.start = self.first_gene.start
            self.end = self.last_gene.end

        self.length = self.end - self.start + 1
        self.gene_number = len(self.gene_list)

    def get_gene(self, query, genome):
        if isinstance(query, GeneLoci):
            return query
        elif isinstance(query, str):
            return genome.gene_dict[query]
        elif isinstance(query, int):
            return genome.chr_dict[self.chr_id][query]
        else:
            raise Exception("query is not GeneLoci, str or int")

    def __str__(self):
        if hasattr(self, 'start'):
            return "Specie %s %s:%s-%s, gene: %s - %s, %d gene." % (
                self.sp_id, self.chr_id, self.start, self.end, self.first_gene.id, self.last_gene.id, self.gene_number)
        else:
            return "Specie %s %s:%s-%s" % (
                self.sp_id, self.chr_id, self.first_gene, self.last_gene)

    __repr__ = __str__


class SyntenyBlock(object):
    def __init__(
            self,
            sb_id,
            q_sp,
            s_sp,
            strand,
            gene_pair_dict,
            property_dict,
            parameter_dict):
        self.id = sb_id
        self.property = property_dict
        self.parameter = parameter_dict
        self.strand = strand
        self.q_sp = q_sp
        self.s_sp = s_sp
        self.gene_pair_dict = gene_pair_dict

        if len(gene_pair_dict) > 0:
            self.get_info()

    def get_info(self):
        self.q_chr = self.gene_pair_dict[0].q_gene.chr_id
        self.s_chr = self.gene_pair_dict[0].s_gene.chr_id

        q_gene_list = sorted(
            [self.gene_pair_dict[i].q_gene for i in self.gene_pair_dict], key=lambda x: x.loci)
        self.first_q_gene = q_gene_list[0]
        self.last_q_gene = q_gene_list[-1]

        s_gene_list = sorted(
            [self.gene_pair_dict[i].s_gene for i in self.gene_pair_dict], key=lambda x: x.loci)
        self.first_s_gene = s_gene_list[0]
        self.last_s_gene = s_gene_list[-1]

        self.first_q_gene_loci = self.first_q_gene.loci
        self.last_q_gene_loci = self.last_q_gene.loci
        self.first_s_gene_loci = self.first_s_gene.loci
        self.last_s_gene_loci = self.last_s_gene.loci

        self.query_from = min([self.first_q_gene.gf.start,
                               self.first_q_gene.gf.end,
                               self.last_q_gene.gf.start,
                               self.last_q_gene.gf.end])
        self.query_to = max([self.first_q_gene.gf.start,
                             self.first_q_gene.gf.end,
                             self.last_q_gene.gf.start,
                             self.last_q_gene.gf.end])

        self.subject_from = min([self.first_s_gene.gf.start,
                                 self.first_s_gene.gf.end,
                                 self.last_s_gene.gf.start,
                                 self.last_s_gene.gf.end])
        self.subject_to = max([self.first_s_gene.gf.start,
                               self.first_s_gene.gf.end,
                               self.last_s_gene.gf.start,
                               self.last_s_gene.gf.end])

    def get_full_info(self, q_genome, s_genome):
        self.get_info()

        self.query_gene_list = []
        for i in range(self.first_q_gene_loci, self.last_q_gene_loci + 1):
            self.query_gene_list.append(q_genome.chr_dict[self.q_chr][i])

        self.subject_gene_list = []
        for i in range(self.first_s_gene_loci, self.last_s_gene_loci + 1):
            self.subject_gene_list.append(s_genome.chr_dict[self.s_chr][i])

    def reverse_myself(self, new_sb_id=None):
        gene_pair_dict = {
            i: self.gene_pair_dict[i].reverse_myself() for i in self.gene_pair_dict}
        if new_sb_id is None:
            new_sb_id = self.id

        new_sb = SyntenyBlock(
            new_sb_id,
            self.s_sp,
            self.q_sp,
            self.strand,
            gene_pair_dict,
            self.property,
            self.parameter)

        new_sb.q_chr = new_sb.gene_pair_dict[0].q_gene.chr_id
        new_sb.s_chr = new_sb.gene_pair_dict[0].s_gene.chr_id

        new_sb.query_gene_list = self.subject_gene_list
        new_sb.subject_gene_list = self.query_gene_list

        new_sb.first_q_gene = self.first_s_gene
        new_sb.last_q_gene = self.last_s_gene
        new_sb.first_s_gene = self.first_q_gene
        new_sb.last_s_gene = self.last_q_gene

        new_sb.first_q_gene_loci = new_sb.first_q_gene.loci
        new_sb.last_q_gene_loci = new_sb.last_q_gene.loci
        new_sb.first_s_gene_loci = new_sb.first_s_gene.loci
        new_sb.last_s_gene_loci = new_sb.last_s_gene.loci

        new_sb.query_from = self.subject_from
        new_sb.query_to = self.subject_to
        new_sb.subject_from = self.query_from
        new_sb.subject_to = self.query_to

        return new_sb

    def __str__(self):

        return "Q = %s:%s gene: %d-%d (%d) base: %d-%d (%d) vs S = %s:%s gene: %d-%d (%d) base: %d-%d (%d), %s, have %d gene pair" % (self.q_sp,
                                                                                                                                      self.q_chr,
                                                                                                                                      self.first_q_gene_loci,
                                                                                                                                      self.last_q_gene_loci,
                                                                                                                                      self.last_q_gene_loci - self.first_q_gene_loci + 1,
                                                                                                                                      self.query_from,
                                                                                                                                      self.query_to,
                                                                                                                                      self.query_to - self.query_from + 1,
                                                                                                                                      self.s_sp,
                                                                                                                                      self.s_chr,
                                                                                                                                      self.first_s_gene_loci,
                                                                                                                                      self.last_s_gene_loci,
                                                                                                                                      self.last_s_gene_loci - self.first_s_gene_loci + 1,
                                                                                                                                      self.subject_from,
                                                                                                                                      self.subject_to,
                                                                                                                                      self.subject_to - self.subject_from + 1,
                                                                                                                                      self.strand,
                                                                                                                                      len(self.gene_pair_dict))

    __repr__ = __str__

    def plot(self, save_file=None, debug=False):

        q_gb = GenomeBlock('QGB', self.q_sp, self.q_chr, self.first_q_gene, self.last_q_gene, self.query_gene_list)
        q_gb.get_full_info()
        s_gb = GenomeBlock('SGB', self.s_sp, self.s_chr, self.first_s_gene, self.last_s_gene, self.subject_gene_list)
        s_gb.get_full_info()

        block_dict = {'QGB': q_gb, 'SGB': s_gb}

        link_dict = {('QGB', 'SGB'): [(self.gene_pair_dict[i].q_gene.id, self.gene_pair_dict[i].s_gene.id) for i in self.gene_pair_dict]}

        qgb_plot_length = block_dict['QGB'].length / 1000
        sgb_plot_length = block_dict['SGB'].length / 1000

        block_para_dict = {
            'QGB': {'strand':'+', 'shift_site': (0, 100), 'plot_length': qgb_plot_length},
            'SGB': {'strand':self.strand, 'shift_site': (0, -100), 'plot_length': sgb_plot_length},
        }

        x_lim = max(qgb_plot_length/2, sgb_plot_length/2) * 1.25

        sl_plot_job = SyntenyLinkPlotJob(
            block_dict=block_dict,
            block_para_dict=block_para_dict,
            link_dict=link_dict)

        sl_plot_job.plot(figsize=(x_lim/50, 200/20), x_lim=(-x_lim, x_lim), y_lim=(-200, 200),
                        save_file=save_file, debug=debug)



def merge_blocks(synteny_block_dict, q_genome, s_genome):
    merged_group_list = get_overlaped_block_group(synteny_block_dict)
    num = 0
    merged_synteny_block_dict = {}
    for group_list in merged_group_list:
        merged_synteny_block_dict[num] = get_merged_block(
            num, group_list, synteny_block_dict, q_genome, s_genome)
        num += 1
    return merged_synteny_block_dict


def get_merged_block(
        merge_id,
        group_list,
        synteny_block_dict,
        q_genome,
        s_genome):
    tmp_sb = synteny_block_dict[sorted(group_list, key=lambda x:(abs(
        synteny_block_dict[x].query_to - synteny_block_dict[x].query_from)), reverse=True)[0]]
    q_sp = tmp_sb.q_sp
    s_sp = tmp_sb.s_sp
    strand = tmp_sb.strand
    parameter_dict = tmp_sb.parameter

    gene_pair_dict = {}
    num = 0
    for i in group_list:
        for j in synteny_block_dict[i].gene_pair_dict:
            gene_pair_dict[num] = synteny_block_dict[i].gene_pair_dict[j]
            num += 1

    super_sb = SyntenyBlock(merge_id, q_sp, s_sp, strand,
                            gene_pair_dict, {}, parameter_dict)

    super_sb.get_full_info(q_genome, s_genome)

    return super_sb


def get_overlaped_block_group(synteny_block_dict):
    q_sb_interlap, s_sb_interlap = get_synteny_block_interlap(
        synteny_block_dict)

    group_list = []
    for sb_id in synteny_block_dict:
        group_list.append([sb_id])
        sb = synteny_block_dict[sb_id]

        q_over_list = [i[2] for i in q_sb_interlap[sb.q_chr].find(
            (sb.first_q_gene_loci, sb.last_q_gene_loci))]
        s_over_list = [i[2] for i in s_sb_interlap[sb.s_chr].find(
            (sb.first_s_gene_loci, sb.last_s_gene_loci))]

        overlap_list = list(set(q_over_list) & set(s_over_list))

        if len(overlap_list) > 0:
            # print(overlap_list)
            group_list.append(overlap_list)

    merged_group_list = merge_same_element_set(group_list)

    return merged_group_list


def get_synteny_block_interlap(synteny_block_dict):
    query_synteny_block_chr_interlap_dict = {}
    subject_synteny_block_chr_interlap_dict = {}
    for sb_id in synteny_block_dict:
        sb = synteny_block_dict[sb_id]
        q_chr = sb.q_chr
        s_chr = sb.s_chr
        query_synteny_block_chr_interlap_dict[q_chr] = InterLap()
        subject_synteny_block_chr_interlap_dict[s_chr] = InterLap()

    for sb_id in synteny_block_dict:
        sb = synteny_block_dict[sb_id]
        q_chr = sb.q_chr
        s_chr = sb.s_chr

        query_synteny_block_chr_interlap_dict[q_chr].add(
            (sb.first_q_gene_loci, sb.last_q_gene_loci, sb_id))
        subject_synteny_block_chr_interlap_dict[s_chr].add(
            (sb.first_s_gene_loci, sb.last_s_gene_loci, sb_id))

    return query_synteny_block_chr_interlap_dict, subject_synteny_block_chr_interlap_dict


def gene_cover_depth_stat(
        synteny_block_dict,
        query_or_subject,
        covered_genome):
    q_sb_interlap, s_sb_interlap = get_synteny_block_interlap(
        synteny_block_dict)

    if query_or_subject == 'query':
        sb_interlap = q_sb_interlap
    elif query_or_subject == 'subject':
        sb_interlap = s_sb_interlap

    # gene cover dict
    gene_cover_depth_dict = {}
    for g_id in covered_genome.gene_dict:
        gene = covered_genome.gene_dict[g_id]
        if gene.chr_id in sb_interlap:
            gene_cover_depth_dict[g_id] = len(
                list(sb_interlap[gene.chr_id].find((gene.loci, gene.loci))))
        else:
            gene_cover_depth_dict[g_id] = 0

    # range cover
    range_loci_cover_chr_dict = {}
    for chr_id in covered_genome.chr_dict:
        range_loci_cover_chr_dict[chr_id] = {}
        for gene_num in covered_genome.chr_dict[chr_id]:
            g = covered_genome.chr_dict[chr_id][gene_num]
            g_depth = gene_cover_depth_dict[g.id]
            if g_depth == 0:
                continue
            if g_depth not in range_loci_cover_chr_dict[chr_id]:
                range_loci_cover_chr_dict[chr_id][g_depth] = []
            range_loci_cover_chr_dict[chr_id][g_depth].append(
                (gene_num, gene_num))
            range_loci_cover_chr_dict[chr_id][g_depth] = merge_intervals(
                range_loci_cover_chr_dict[chr_id][g_depth], True)

    range_base_cover_chr_dict = {}
    for chr_id in range_loci_cover_chr_dict:
        range_base_cover_chr_dict[chr_id] = {}
        for depth in range_loci_cover_chr_dict[chr_id]:
            if depth == 0:
                continue
            range_base_cover_chr_dict[chr_id][depth] = []

            for s, e in range_loci_cover_chr_dict[chr_id][depth]:
                start = covered_genome.chr_dict[chr_id][s].gf.start
                end = covered_genome.chr_dict[chr_id][e].gf.end
                range_base_cover_chr_dict[chr_id][depth].append((start, end))

    return gene_cover_depth_dict, range_loci_cover_chr_dict, range_base_cover_chr_dict


class wgdi_collinearity:
    def __init__(self, options, points):
        self.gap_penality = -1
        self.over_length = 0
        self.mg1 = 40
        self.mg2 = 40
        self.pvalue = 1
        self.over_gap = 5
        self.points = points
        self.p_value = 0
        self.coverage_ratio = 0.8
        for k, v in options:
            setattr(self, str(k), v)
        if hasattr(self, 'grading'):
            self.grading = [int(k) for k in self.grading.split(',')]
        else:
            self.grading = [50, 40, 25]
        # if hasattr(self, 'mg'):
        #     self.mg1, self.mg2 = [int(k) for k in self.mg.split(',')]
        # else:
        #     self.mg1, self.mg2 = [40, 40]
        self.pvalue = float(self.pvalue)
        self.coverage_ratio = float(self.coverage_ratio)

    def get_martix(self):
        self.points['usedtimes1'] = 0
        self.points['usedtimes2'] = 0
        self.points['times'] = 1
        self.points['score1'] = self.points['grading']
        self.points['score2'] = self.points['grading']
        self.points['path1'] = self.points.index.to_numpy().reshape(
            len(self.points), 1).tolist()
        self.points['path2'] = self.points['path1']
        self.points_init = self.points.copy()
        self.mat_points = self.points

    def run(self):
        self.get_martix()
        self.score_matrix()
        data = []
        # plus
        points1 = self.points[['loc1', 'loc2',
                               'score1', 'path1', 'usedtimes1']]
        points1 = points1.sort_values(by=['score1'], ascending=[False])
        points1.drop(
            index=points1[points1['usedtimes1'] < 1].index, inplace=True)
        points1.columns = ['loc1', 'loc2', 'score', 'path', 'usedtimes']
        while (self.over_length >= self.over_gap or len(
                points1) >= self.over_gap):
            if self.maxPath(points1):
                if self.p_value > self.pvalue:
                    continue
                data.append([self.path, self.p_value, self.score])
        # minus
        points2 = self.points[['loc1', 'loc2',
                               'score2', 'path2', 'usedtimes2']]
        points2 = points2.sort_values(by=['score2'], ascending=[False])
        points2.drop(
            index=points2[points2['usedtimes2'] < 1].index, inplace=True)
        points2.columns = ['loc1', 'loc2', 'score', 'path', 'usedtimes']
        while (
                self.over_length >= self.over_gap) or (
                len(points2) >= self.over_gap):
            if self.maxPath(points2):
                if self.p_value > self.pvalue:
                    continue
                data.append([self.path, self.p_value, self.score])
        return data

    def score_matrix(self):
        for index, row, col in self.points[['loc1', 'loc2', ]].itertuples():
            points = self.points[(self.points['loc1'] > row) & (self.points['loc2'] > col) & (
                self.points['loc1'] < row + self.mg1) & (self.points['loc2'] < col + self.mg2)]
            row_i_old, gap = row, self.mg2
            for index_ij, row_i, col_j, grading in points[[
                    'loc1', 'loc2', 'grading']].itertuples():
                if col_j - col > gap and row_i > row_i_old:
                    break
                s = grading + (row_i - row + col_j - col) * self.gap_penality
                s1 = s + self.points.at[index, 'score1']
                if s > 0 and self.points.at[index_ij, 'score1'] < s1:
                    self.points.at[index_ij, 'score1'] = s1
                    self.points.at[index, 'usedtimes1'] += 1
                    self.points.at[index_ij, 'usedtimes1'] += 1
                    self.points.at[index_ij,
                                   'path1'] = self.points.at[index,
                                                             'path1'] + [index_ij]
                    gap = min(col_j - col, gap)
                    row_i_old = row_i
        points_revese = self.points.sort_values(
            by=['loc1', 'loc2'], ascending=[False, True])
        for index, row, col in points_revese[['loc1', 'loc2']].itertuples():
            points = points_revese[(points_revese['loc1'] < row) & (points_revese['loc2'] > col) & (
                points_revese['loc1'] > row - self.mg1) & (points_revese['loc2'] < col + self.mg2)]
            row_i_old, gap = row, self.mg2
            for index_ij, row_i, col_j, grading in points[[
                    'loc1', 'loc2', 'grading']].itertuples():
                if col_j - col > gap and row_i < row_i_old:
                    break
                s = grading + (row - row_i + col_j - col) * self.gap_penality
                s1 = s + self.points.at[index, 'score2']
                if s > 0 and self.points.at[index_ij, 'score2'] < s1:
                    self.points.at[index_ij, 'score2'] = s1
                    self.points.at[index, 'usedtimes2'] += 1
                    self.points.at[index_ij, 'usedtimes2'] += 1
                    self.points.at[index_ij,
                                   'path2'] = self.points.at[index,
                                                             'path2'] + [index_ij]
                    gap = min(col_j - col, gap)
                    row_i_old = row_i
        return self.points

    def maxPath(self, points):
        if len(points) == 0:
            self.over_length = 0
            return False
        self.score, self.path_index = points.loc[points.index[0], [
            'score', 'path']]
        self.path = points[points.index.isin(self.path_index)]
        self.over_length = len(self.path_index)
        # Whether the block overlaps with other blocks
        if self.over_length >= self.over_gap and len(
                self.path) / self.over_length > self.coverage_ratio:
            points.drop(index=self.path.index, inplace=True)
            [[loc1_min, loc2_min], [loc1_max, loc2_max]] = self.path[[
                'loc1', 'loc2']].agg(['min', 'max']).to_numpy()
            # calculate pvalues
            gap_init = self.points_init[(loc1_min <= self.points_init['loc1']) & (self.points_init['loc1'] <= loc1_max) & (
                loc2_min <= self.points_init['loc2']) & (self.points_init['loc2'] <= loc2_max)].copy()
            self.p_value = self.pvalue_estimated(
                gap_init, loc1_max - loc1_min + 1, loc2_max - loc2_min + 1)
            self.path = self.path.sort_values(by=['loc1'], ascending=[True])[
                ['loc1', 'loc2']]
            return True
        else:
            points.drop(index=points.index[0], inplace=True)
        return False

    def pvalue_estimated(self, gap, L1, L2):
        N1 = gap['times'].sum()
        N = len(gap)
        self.points_init.loc[gap.index, 'times'] += 1
        m = len(self.path)
        a = (1 - self.score / m / self.grading[0]) * (N1 - \
             m + 1) / N * (L1 - m + 1) * (L2 - m + 1) / L1 / L2
        return round(a, 4)

# wgdi functions


def run_wgdi_collinearity(
        loc_pair_list,
        min_size=5,
        max_gap=25,
        max_pvalue=1,
        min_score=50,
        gap_penality=-1,
        **kargs):
    """
    loc_pair_list = [
        (8, 1618), # loc of homo gene pair
        (11, 273),
    ]

    return data.append([self.path, self.p_value, self.score])
    """

    loc_pair_list = sorted(loc_pair_list, key=lambda x: x[0])

    options = {
        "gap_penality": gap_penality,
        "over_length": 0,
        # The maximum gap(mg) value is an important parameter for detecting
        # collinear regions.
        "mg1": max_gap,
        # The maximum gap(mg) value is an important parameter for detecting
        # collinear regions.
        "mg2": max_gap,
        # Evaluate the compactness and uniqueness of collinear blocks, the
        # range is 0-1, and the better collinearity range is 0-0.2.
        "pvalue": 1,
        "over_gap": 5,
        "p_value": 0,
        "coverage_ratio": 0.8,
    }

    for i in kargs:
        options[i] = kargs[i]

    loc1 = [i[0] for i in loc_pair_list]
    loc2 = [i[1] for i in loc_pair_list]

    df = pd.DataFrame(
        {
            'loc1': loc1,
            'loc2': loc2,
            'grading': 50,
        }
    )

    options = [(i, options[i]) for i in options]
    my_collinearity = wgdi_collinearity(
        options, df)

    data = my_collinearity.run()
    data = [i for i in data if len(
        i[0]) >= min_size and i[1] <= max_pvalue and i[2] >= min_score]

    return data


def get_synteny_block(
        gene_pair_list,
        min_size=5,
        max_gap=25,
        max_pvalue=1,
        min_score=50,
        gap_penality=-1,
        tandem_repeat_gap=10):
    for gp in gene_pair_list:
        q = gp.q_gene
        s = gp.s_gene

        if q.sp_id == s.sp_id and q.chr_id == s.chr_id and abs(
                q.loci - s.loci) <= tandem_repeat_gap:
            gp.is_tandem = True
        else:
            gp.is_tandem = False

    loc_pair_list = [(gp.q_gene.loci, gp.s_gene.loci)
                     for gp in gene_pair_list if not gp.is_tandem]

    q_sp = gene_pair_list[0].q_gene.sp_id
    s_sp = gene_pair_list[0].s_gene.sp_id

    q_gene_dict = {gp.q_gene.loci: gp.q_gene for gp in gene_pair_list}
    s_gene_dict = {gp.s_gene.loci: gp.s_gene for gp in gene_pair_list}

    parameter_dict = {
        "min_size": min_size,
        "max_gap": max_gap,
        "max_pvalue": max_pvalue,
        "min_score": min_score,
        "gap_penality": gap_penality
    }

    wgdi_out_list = run_wgdi_collinearity(
        loc_pair_list, min_size, max_gap, max_pvalue, min_score, gap_penality)

    num = 0
    output_dict = OrderedDict()
    for wgdi_out in wgdi_out_list:
        sb_df, p_value, score = wgdi_out

        property_dict = {
            'score': score,
            'p_value': p_value,
            'gene_pair_num': len(sb_df),
        }

        a, b = sb_df['loc2'].head(2).values
        if a < b:
            strand = '+'
        else:
            strand = '-'

        gene_pair_dict = OrderedDict([(i, GenePair(
            q_gene_dict[sb_df.iloc[i].loc1], s_gene_dict[sb_df.iloc[i].loc2])) for i in range(len(sb_df))])

        sb = SyntenyBlock(num, q_sp, s_sp, strand,
                          gene_pair_dict, property_dict, parameter_dict)

        output_dict[num] = sb
        num += 1

    return output_dict


class DotPlotJob(object):
    def __init__(
            self,
            sp1,
            sp2=None,
            synteny_block_dict=None,
            sp1_base_cover_dict=None,
            sp2_base_cover_dict=None,
            sp1_loci_cover_dict=None,
            sp2_loci_cover_dict=None,):

        self.sp1 = sp1
        self.sp2 = sp2
        self.synteny_block_dict = synteny_block_dict
        self.sp1_base_cover_dict = sp1_base_cover_dict
        self.sp2_base_cover_dict = sp2_base_cover_dict
        self.sp1_loci_cover_dict = sp1_loci_cover_dict
        self.sp2_loci_cover_dict = sp2_loci_cover_dict

    def plot(
            self,
            mode='base',
            debug=False,
            highlight_synteny_blocks={},
            **kargs):

        # set parameter
        plot_parameter = {
            "sp1_top": None,
            "sp2_top": None,
            "reverse": False,
            "max_cover_depth": 4,
            "save_file": None,
            "sp1_contig_list": None,
            "sp2_contig_list": None,
            "min_contig_length": 1000000,
            "fig_size": (20, 20),
            "plot_size_tuple": (0.1, 0.65, 0.1, 0.65, 0.02, 0.04),
        }

        if mode == 'base':
            plot_parameter["min_contig_length"] = 1000000
        elif mode == 'loci':
            plot_parameter["min_contig_length"] = 50

        for i in kargs:
            plot_parameter[i] = kargs[i]

        # parameter
        fig_size = plot_parameter["fig_size"]

        # make fig & ax
        left, width, bottom, height, spacing, cover_plot_height = plot_parameter[
            "plot_size_tuple"]

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom - cover_plot_height -
                      spacing, width, cover_plot_height]
        rect_histy = [left + width + spacing * 1.5,
                      bottom, cover_plot_height, height]

        fig = plt.figure(figsize=fig_size)

        ax = fig.add_axes(rect_scatter)
        ax_histx = fig.add_axes(rect_histx, sharex=ax)
        ax_histy = fig.add_axes(rect_histy, sharey=ax)

        # get plot contig list
        sp1_contig_list = plot_parameter["sp1_contig_list"] if plot_parameter["sp1_contig_list"] else self.get_plot_contig_list(
            self.sp1, mode, plot_parameter["min_contig_length"])
        if self.sp2:
            sp2_contig_list = plot_parameter["sp2_contig_list"] if plot_parameter["sp2_contig_list"] else self.get_plot_contig_list(
                self.sp2, mode, plot_parameter["min_contig_length"])
        else:
            sp2_contig_list = sp1_contig_list

        # plot contig grid
        query_contig_coord, subject_contig_coord = self.plot_contig_grids(
            ax, mode, sp1_contig_list, sp2_contig_list, plot_parameter["reverse"])

        # plot synteny blocks
        self.plot_synteny_blocks(
            ax,
            mode,
            self.synteny_block_dict,
            query_contig_coord,
            subject_contig_coord,
            reverse=plot_parameter["reverse"],
            highlight_dict=highlight_synteny_blocks)

        # plot cover hist
        self.add_cover_plots(
            ax_histx,
            ax_histy,
            mode,
            query_contig_coord,
            subject_contig_coord,
            plot_parameter["max_cover_depth"],
            plot_parameter["reverse"])

        # set label
        if self.sp2 is None:
            ax.set_xlabel(self.sp1.id, fontsize=20)
            ax.set_ylabel(self.sp1.id, fontsize=20)
        elif plot_parameter["reverse"]:
            ax.set_xlabel(self.sp1.id, fontsize=20)
            ax.set_ylabel(self.sp2.id, fontsize=20)
        else:
            ax.set_xlabel(self.sp2.id, fontsize=20)
            ax.set_ylabel(self.sp1.id, fontsize=20)

        ax.xaxis.set_label_position('bottom')
        ax.xaxis.set_label_coords(0.5, -0.01)
        ax.yaxis.set_label_position('right')
        ax.yaxis.set_label_coords(1.01, 0.5)

        plt.show()

        if plot_parameter["save_file"]:
            fig.savefig(
                plot_parameter["save_file"],
                format='pdf',
                facecolor='none',
                edgecolor='none',
                bbox_inches='tight')

        if not debug:
            plt.close(fig)
        else:
            self.ax = ax
            self.ax_histx = ax_histx
            self.ax_histy = ax_histy
            self.query_contig_coord = query_contig_coord
            self.subject_contig_coord = subject_contig_coord

    # plot grid
    def get_plot_contig_list(
            self,
            sp,
            mode,
            min_contig_length=None,
            top_n=None):
        if min_contig_length is None:
            min_contig_length = 0

        if top_n is None:
            top_n = len(sp.chr_length_dict)

        if mode == 'base':
            contig_list = [
                i[0] for i in sorted(
                    sp.chr_length_dict.items(),
                    key=lambda x: x[1],
                    reverse=True) if i[1] > min_contig_length][0:top_n]
        elif mode == 'loci':
            contig_list = [
                i[0] for i in sorted(
                    sp.chr_gene_number_dict.items(),
                    key=lambda x: x[1],
                    reverse=True) if i[1] > min_contig_length][0:top_n]
        return contig_list

    def plot_contig_grids(
            self,
            ax,
            mode,
            sp1_contig_list,
            sp2_contig_list,
            reverse=False):
        if mode == 'base':
            if self.sp2 is None:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp1_contig_list, sp2_contig_list, self.sp1.chr_length_dict, self.sp1.chr_length_dict)
            elif reverse:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp2_contig_list, sp1_contig_list, self.sp2.chr_length_dict, self.sp1.chr_length_dict)
            else:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp1_contig_list, sp2_contig_list, self.sp1.chr_length_dict, self.sp2.chr_length_dict)
        elif mode == 'loci':
            if self.sp2 is None:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp1_contig_list, sp2_contig_list, self.sp1.chr_gene_number_dict, self.sp1.chr_gene_number_dict)
            elif reverse:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp2_contig_list, sp1_contig_list, self.sp2.chr_gene_number_dict, self.sp1.chr_gene_number_dict)
            else:
                query_contig_coord, subject_contig_coord = self.add_contig_grid(
                    ax, sp1_contig_list, sp2_contig_list, self.sp1.chr_gene_number_dict, self.sp2.chr_gene_number_dict)
        return query_contig_coord, subject_contig_coord

    def add_contig_grid(
            self,
            ax,
            q_contig_list,
            s_contig_list,
            query_contig_length_dict,
            subject_contig_length_dict,
            grid_colors='k',
            linewidths=0.5,
            rename_chr_map=None):
        query_contig_coord = {}
        subject_contig_coord = {}

        # for query aka y axis h
        q_hline_y_site = []
        q_tick_local = []
        q_tick_label = []
        q_num = 0

        for i in q_contig_list:
            query_contig_coord[i] = q_num
            q_num += query_contig_length_dict[i]
            q_hline_y_site.append(q_num)
            q_tick_local.append(q_num - query_contig_length_dict[i] / 2)
            if rename_chr_map:
                q_tick_label.append(rename_chr_map[i])
            else:
                q_tick_label.append(i)

        q_hline_y_site = q_hline_y_site[:-1]

        ax.hlines(q_hline_y_site, 0, 1, transform=ax.get_yaxis_transform(),
                  colors=grid_colors, linewidths=linewidths)

        # for subject aka x axis v
        s_vline_y_site = []
        s_tick_local = []
        s_tick_label = []
        s_num = 0

        for i in s_contig_list:
            subject_contig_coord[i] = s_num
            s_num += subject_contig_length_dict[i]
            s_vline_y_site.append(s_num)
            s_tick_local.append(s_num - subject_contig_length_dict[i] / 2)
            if rename_chr_map:
                s_tick_label.append(rename_chr_map[i])
            else:
                s_tick_label.append(i)

        s_vline_y_site = s_vline_y_site[:-1]

        ax.vlines(s_vline_y_site, 0, 1, transform=ax.get_xaxis_transform(),
                  colors=grid_colors, linewidths=linewidths)

        ax.invert_yaxis()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.tick_params(axis='both', which='both', bottom=False, top=False,
                       left=False, right=False, labeltop=True, labelleft=True)

        ax.set_xticks(s_tick_local)
        ax.set_xticklabels(s_tick_label)
        ax.set_yticks(q_tick_local)
        ax.set_yticklabels(q_tick_label)

        ax.xaxis.set_tick_params(
            which='major', labelrotation=90, labeltop=True, labelbottom=False)

        x_y_lim = ((0, s_num), (q_num, 0))
        ax.set_xlim(x_y_lim[0])
        ax.set_ylim(x_y_lim[1])

        return query_contig_coord, subject_contig_coord

    # plot synteny blocks
    def plot_synteny_blocks(
            self,
            ax,
            mode,
            synteny_block_dict,
            query_contig_coord,
            subject_contig_coord,
            reverse=False,
            highlight_dict={}):
        if self.sp2 is None:
            self.add_synteny_dot(
                ax,
                query_contig_coord,
                subject_contig_coord,
                synteny_block_dict,
                mode=mode,
                reverse=False,
                highlight_dict=highlight_dict)
            self.add_synteny_dot(
                ax,
                query_contig_coord,
                subject_contig_coord,
                synteny_block_dict,
                mode=mode,
                reverse=True,
                highlight_dict=highlight_dict)
        else:
            self.add_synteny_dot(
                ax,
                query_contig_coord,
                subject_contig_coord,
                synteny_block_dict,
                mode=mode,
                reverse=reverse,
                highlight_dict=highlight_dict)

    def add_synteny_dot(
            self,
            ax,
            query_contig_coord,
            subject_contig_coord,
            synteny_block_dict,
            mode='base',
            reverse=False,
            color='#617a95',
            linewidth=3,
            highlight_dict={}):

        highlight_sb_dict = {}
        for highlight_color in highlight_dict:
            sb_list = highlight_dict[highlight_color]
            for sb_id in sb_list:
                highlight_sb_dict[str(sb_id)] = highlight_color

        # print(highlight_sb_dict)

        for id_tmp in synteny_block_dict:
            sb_tmp = synteny_block_dict[id_tmp]
            strand = sb_tmp.strand

            if not reverse:
                q_id = sb_tmp.q_chr
                s_id = sb_tmp.s_chr
                if mode == 'base':
                    q_f = sb_tmp.query_from
                    q_t = sb_tmp.query_to
                    s_f = sb_tmp.subject_from
                    s_t = sb_tmp.subject_to
                elif mode == 'loci':
                    q_f = sb_tmp.first_q_gene_loci
                    q_t = sb_tmp.last_q_gene_loci
                    s_f = sb_tmp.first_s_gene_loci
                    s_t = sb_tmp.last_s_gene_loci
            else:
                q_id = sb_tmp.s_chr
                s_id = sb_tmp.q_chr
                if mode == 'base':
                    q_f = sb_tmp.subject_from
                    q_t = sb_tmp.subject_to
                    s_f = sb_tmp.query_from
                    s_t = sb_tmp.query_to
                elif mode == 'loci':
                    q_f = sb_tmp.first_s_gene_loci
                    q_t = sb_tmp.last_s_gene_loci
                    s_f = sb_tmp.first_q_gene_loci
                    s_t = sb_tmp.last_q_gene_loci

            if q_id not in query_contig_coord or s_id not in subject_contig_coord:
                continue

            q_f = query_contig_coord[q_id] + q_f
            q_t = query_contig_coord[q_id] + q_t

            s_f = subject_contig_coord[s_id] + s_f
            s_t = subject_contig_coord[s_id] + s_t

            if strand == '+':
                ax.plot((s_f, s_t), (q_f, q_t), color, linewidth=linewidth)
            else:
                ax.plot((s_t, s_f), (q_f, q_t), color, linewidth=linewidth)

            if str(id_tmp) in highlight_sb_dict:
                highlight_color = highlight_sb_dict[str(id_tmp)]
                # print(s_f, s_t, q_f, q_t)
                # print(sb_tmp)
                self.plot_highlight_cross(
                    ax, s_f, s_t, q_f, q_t, highlight_color, 1)

    def plot_highlight_cross(self, ax, x1, x2, y1, y2, color, alpha):
        ax.fill_betweenx(
            ax.get_ylim(),
            x1,
            x2,
            color=color,
            alpha=alpha)
        ax.fill_between(
            ax.get_xlim(),
            y1,
            y2,
            color=color,
            alpha=alpha)

    # add cover plot
    def small_cover_plot(
            self,
            ax,
            orientation,
            base_cover_chr_dict,
            contig_coord,
            max_cover_depth=5,
            facecolor='r'):

        rectangle_list = []
        for chr_id in base_cover_chr_dict:
            for depth in base_cover_chr_dict[chr_id]:
                for s, e in base_cover_chr_dict[chr_id][depth]:
                    if chr_id not in contig_coord:
                        continue
                    contig_coord_base = contig_coord[chr_id]
                    ps, pe = s + contig_coord_base, e + contig_coord_base
                    if orientation == 'h':
                        rect = Patches.Rectangle((ps, 0), pe - ps, depth)
                    elif orientation == 'v':
                        rect = Patches.Rectangle((0, ps), depth, pe - ps)
                    rectangle_list.append(rect)

        pc = PatchCollection(
            rectangle_list, facecolor=facecolor, edgecolor='None')
        ax.add_collection(pc)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if orientation == 'h':
            ax.set_ylim((0, max_cover_depth + 0.5))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1))
            ax.get_xaxis().set_visible(False)

        elif orientation == 'v':
            ax.set_xlim((0, max_cover_depth + 0.5))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
            ax.get_yaxis().set_visible(False)

    def add_cover_plots(
            self,
            ax_histx,
            ax_histy,
            mode,
            query_contig_coord,
            subject_contig_coord,
            max_cover_depth,
            reverse):
        if mode == 'base':
            if self.sp2 is None:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp1_base_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp1_base_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)
            elif reverse:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp1_base_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp2_base_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)
            else:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp2_base_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp1_base_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)
        elif mode == 'loci':
            if self.sp2 is None:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp1_loci_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp1_loci_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)
            elif reverse:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp1_loci_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp2_loci_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)
            else:
                self.small_cover_plot(
                    ax_histx,
                    'h',
                    self.sp2_loci_cover_dict,
                    subject_contig_coord,
                    max_cover_depth=max_cover_depth)
                self.small_cover_plot(
                    ax_histy,
                    'v',
                    self.sp1_loci_cover_dict,
                    query_contig_coord,
                    max_cover_depth=max_cover_depth)


class GenomeSyntenyBlockJob(object):
    def __init__(
            self,
            sp1_id,
            sp1_gff,
            sp2_id=None,
            sp2_gff=None,
            gene_pair_file=None,
            sb_options=None,
            mcscan_output_file=None):
        self.sp1_id = sp1_id
        self.sp1_gff = sp1_gff
        self.sp2_id = sp2_id
        self.sp2_gff = sp2_gff
        self.gene_pair_file = gene_pair_file
        self.mcscan_output_file = mcscan_output_file

        self.sb_options = OrderedDict([
            ("min_size", 5),
            ("max_gap", 25),
            ("max_pvalue", 1),
            ("min_score", 50),
            ("gap_penality", -1),
            ("tandem_repeat_gap", 10)
        ])

        if sb_options:
            for i in sb_options:
                self.sb_options[i] = sb_options[i]

        self.sp1 = Genome(sp1_id, sp1_gff)
        if sp2_gff:
            self.sp2 = Genome(sp2_id, sp2_gff)
        else:
            self.sp2 = None

    def read_gene_pair(self, gene_pair_file, sp1, sp2=None):
        gene_pair_list = []
        with open(gene_pair_file, 'r') as f:
            for l in f:
                gene_id1, gene_id2 = l.strip().split()
                if sp2:
                    gp = GenePair(
                        sp1.gene_dict[gene_id1], sp2.gene_dict[gene_id2])
                    gene_pair_list.append(gp)
                else:
                    gp = GenePair(
                        sp1.gene_dict[gene_id1], sp1.gene_dict[gene_id2])
                    gene_pair_list.append(gp)
        return gene_pair_list

    def build_synteny_blocks(self, threads=8):
        self.gene_pair_list = self.read_gene_pair(
            self.gene_pair_file, self.sp1, self.sp2)

        sp1_chr_list = list(self.sp1.chr_dict.keys())
        if self.sp2:
            sp2_chr_list = list(self.sp2.chr_dict.keys())
            tmp_sp2_id = self.sp2_id
        else:
            sp2_chr_list = sp1_chr_list
            tmp_sp2_id = self.sp1_id

        sb_args = [self.sb_options[i] for i in self.sb_options]

        chr_gene_pair_list_dict = {}
        for q_chr in sp1_chr_list:
            for s_chr in sp2_chr_list:
                chr_gene_pair_list_dict[(q_chr, s_chr)] = []

        for gp in self.gene_pair_list:
            if gp.q_gene.sp_id == self.sp1_id and gp.s_gene.sp_id == tmp_sp2_id:
                chr_gene_pair_list_dict[(
                    gp.q_gene.chr_id, gp.s_gene.chr_id)].append(gp)
            elif gp.s_gene.sp_id == self.sp1_id and gp.q_gene.sp_id == tmp_sp2_id:
                chr_gene_pair_list_dict[(gp.s_gene.chr_id, gp.q_gene.chr_id)].append(
                    gp.reverse_myself())

        args_list = []
        args_id_list = []
        mlt_out = {}
        for q_chr in sp1_chr_list:
            for s_chr in sp2_chr_list:
                chr_gene_pair_list = chr_gene_pair_list_dict[(q_chr, s_chr)]
                # chr_gene_pair_list = []
                # for gp in self.gene_pair_list:
                #     if gp.q_gene.sp_id == self.sp1_id and gp.q_gene.chr_id == q_chr and gp.s_gene.sp_id == tmp_sp2_id and gp.s_gene.chr_id == s_chr:
                #         chr_gene_pair_list.append(gp)
                #     elif gp.s_gene.sp_id == self.sp1_id and gp.s_gene.chr_id == q_chr and gp.q_gene.sp_id == tmp_sp2_id and gp.q_gene.chr_id == s_chr:
                #         chr_gene_pair_list.append(gp.reverse_myself())
                if len(chr_gene_pair_list):
                    if threads == 1:
                        mlt_out[((self.sp1_id, q_chr), (tmp_sp2_id, s_chr))] = {}
                        mlt_out[((self.sp1_id, q_chr), (tmp_sp2_id, s_chr))]['output'] = get_synteny_block(
                            *tuple([chr_gene_pair_list] + sb_args))
                    args_list.append(tuple([chr_gene_pair_list] + sb_args))
                    args_id_list.append(
                        ((self.sp1_id, q_chr), (tmp_sp2_id, s_chr)))

        if threads > 1:
            mlt_out = multiprocess_running(
                get_synteny_block,
                args_list,
                threads,
                silence=False,
                args_id_list=args_id_list,
                timeout=None)
        self.synteny_blocks_dict = {i: mlt_out[i]['output'] for i in mlt_out}

        num = 0
        self.synteny_block_dict = OrderedDict()
        for chr_pair_info in self.synteny_blocks_dict:
            for sb_id in self.synteny_blocks_dict[chr_pair_info]:
                sb = self.synteny_blocks_dict[chr_pair_info][sb_id]
                self.synteny_block_dict[num] = sb
                num += 1

    def get_mcscan_parameter(self, mcscan_output_file):
        gene_in_coll = None
        percentage = None
        all_gene = None

        parameter_dict = OrderedDict()
        with open(mcscan_output_file, 'r') as f:
            for each_line in f:
                # statistics
                mobj = re.match(
                    r"# Number of collinear genes: (\d+), Percentage: (\d+\.\d+)",
                    each_line)
                if mobj:
                    gene_in_coll, percentage = mobj.groups()
                    gene_in_coll, percentage = int(
                        gene_in_coll), float(percentage)

                mobj = re.match(r"# Number of all genes: (\d+)", each_line)
                if mobj:
                    all_gene = mobj.groups()[0]
                    all_gene = int(all_gene)

                # statistics wgdi xyx
                mobj = re.match(
                    r"# Number of collinear gene pairs: (\d+), Percentage: (\d+\.\d+)%",
                    each_line)
                if mobj:
                    gene_in_coll, percentage = mobj.groups()
                    gene_in_coll, percentage = int(
                        gene_in_coll), float(percentage)

                mobj = re.match(
                    r"# Number of all gene pairs: (\d+)", each_line)
                if mobj:
                    all_gene = mobj.groups()[0]
                    all_gene = int(all_gene)

                # Parameters
                mobj = re.findall(r"^# (\S+): (\S+)$", each_line)
                if len(mobj) > 0:
                    p, v = mobj[0]
                    bad_flag = False
                    try:
                        v = float(v)
                    except BaseException:
                        bad_flag = True
                    if bad_flag is False:
                        parameter_dict[p] = v

        parameter_dict["gene_in_coll"] = gene_in_coll
        parameter_dict["percentage"] = percentage
        parameter_dict["all_gene"] = all_gene

        return parameter_dict

    def write_mcscan_output(self, mcscan_output_file):

        sb_gp_num = 0
        for i in self.synteny_block_dict:
            sb = self.synteny_block_dict[i]
            sb_gp_num += sb.property['gene_pair_num']

        with open(mcscan_output_file, 'w') as f:
            f.write(
                "############### Parameters ###############\n# MIN_SIZE: %d\n# MAX_GAP: %d\n# MAX_PVALUE: %.2f\n# MIN_SCORE: %d\n# GAP_PENALITY: %d\n# TANDEM_REPEAT_GAP: %d\n" %
                tuple(
                    [
                        self.sb_options[i] for i in self.sb_options]))

            if hasattr(self, "gene_pair_list"):
                all_gene = len(self.gene_pair_list)
            elif hasattr(self, "mcscan_parameter"):
                all_gene = self.mcscan_parameter['all_gene']
            else:
                all_gene = None

            if all_gene:
                f.write(
                    "############### Statistics ###############\n# Number of collinear gene pairs: %d, Percentage: %.2f%%\n# Number of all gene pairs: %d\n##########################################\n" %
                    (sb_gp_num, sb_gp_num / all_gene * 100, all_gene))

            for num in self.synteny_block_dict:
                sb = self.synteny_block_dict[num]
                s = "## Alignment %d: score=%.1f e_value=%.3e N=%d %s&%s %s" % (int(num), float(sb.property['score']), float(
                    sb.property['p_value']), int(sb.property['gene_pair_num']), sb.q_chr, sb.s_chr, "+" if sb.strand == "+" else "-")
                f.write(s + "\n")
                for gp_id in sb.gene_pair_dict:
                    gp = sb.gene_pair_dict[gp_id]
                    s = "  %s-  %s:\t%s\t%s\t0" % (str(num),
                                                   str(gp_id), gp.q_gene.id, gp.s_gene.id)
                    f.write(s + "\n")

    def read_mcscan_output(self, mcscan_output_file=None):
        if mcscan_output_file is None:
            mcscan_output_file = self.mcscan_output_file

        self.mcscan_parameter = self.get_mcscan_parameter(mcscan_output_file)

        self.synteny_block_dict = OrderedDict()

        with open(mcscan_output_file, 'r') as f:
            for each_line in f:
                # Block title
                mobj = re.match(
                    r"## Alignment (\S+): score=(\S+) e_value=(\S+) N=(\S+) (\S+)&(\S+) (\S+)",
                    each_line)
                if mobj:
                    align_id, score, e_value, gene_pair_num, q_chr, s_chr, strand = mobj.groups()

                    align_id, score, e_value, gene_pair_num, q_chr, s_chr, strand = align_id, float(
                        score), float(e_value), int(gene_pair_num), q_chr, s_chr, strand
                    if strand == 'plus' or strand == '+':
                        strand = "+"
                    elif strand == 'minus' or strand == '-':
                        strand = "-"
                    else:
                        raise

                    property_dict = {
                        'score': score,
                        'e_value': e_value,
                        'p_value': e_value,
                        'gene_pair_num': gene_pair_num,
                    }

                    if self.sp2 is None:
                        self.synteny_block_dict[align_id] = SyntenyBlock(
                            align_id, self.sp1_id, self.sp1_id, strand, {}, property_dict, self.mcscan_parameter)
                    else:
                        self.synteny_block_dict[align_id] = SyntenyBlock(
                            align_id, self.sp1_id, self.sp2_id, strand, {}, property_dict, self.mcscan_parameter)

                # block line
                if re.match("^#", each_line):
                    continue
                else:
                    if align_id not in self.synteny_block_dict:
                        continue

                    align_id = each_line.split("-", 1)[0]
                    pair_id = each_line.split("-", 1)[1].split(":", 1)[0]

                    align_id = re.sub(r'\s+', '', align_id)
                    pair_id = int(re.sub(r'\s+', '', pair_id))

                    q_gene_id, s_gene_id, e_value = each_line.split(
                        "-", 1)[1].split(":", 1)[1].split()
                    align_id, pair_id, q_gene_id, s_gene_id, e_value = align_id, pair_id, q_gene_id, s_gene_id, float(
                        e_value)

                    if self.sp2 is None:
                        q_gene = self.sp1.gene_dict[q_gene_id]
                        s_gene = self.sp1.gene_dict[s_gene_id]
                    else:
                        q_gene = self.sp1.gene_dict[q_gene_id]
                        s_gene = self.sp2.gene_dict[s_gene_id]

                    property_dict = {'e_value': e_value}

                    self.synteny_block_dict[align_id].gene_pair_dict[pair_id] = GenePair(
                        q_gene, s_gene, property_dict)

        for align_id in self.synteny_block_dict:
            if self.sp2 is None:
                self.synteny_block_dict[align_id].get_full_info(
                    self.sp1, self.sp1)
            else:
                self.synteny_block_dict[align_id].get_full_info(
                    self.sp1, self.sp2)

    def get_sb_cover_dict(self):
        # merge block
        if self.sp2 is None:
            merged_synteny_block_dict = merge_blocks(
                self.synteny_block_dict, self.sp1, self.sp1)
        else:
            merged_synteny_block_dict = merge_blocks(
                self.synteny_block_dict, self.sp1, self.sp2)

        # get gene cover dict
        q_gene_covered_dict, q_range_loci_cover_chr_dict, q_range_base_cover_chr_dict = gene_cover_depth_stat(
            merged_synteny_block_dict, 'query', self.sp1)
        if self.sp2 is None:
            s_gene_covered_dict, s_range_loci_cover_chr_dict, s_range_base_cover_chr_dict = q_gene_covered_dict, q_range_loci_cover_chr_dict, q_range_base_cover_chr_dict
        else:
            s_gene_covered_dict, s_range_loci_cover_chr_dict, s_range_base_cover_chr_dict = gene_cover_depth_stat(
                merged_synteny_block_dict, 'subject', self.sp2)

        self.cover_dict = {}
        self.cover_dict[self.sp1_id] = {'gene': q_gene_covered_dict,
                                        'loci': q_range_loci_cover_chr_dict,
                                        'base': q_range_base_cover_chr_dict,
                                        }

        if self.sp2:
            self.cover_dict[self.sp2_id] = {'gene': s_gene_covered_dict,
                                            'loci': s_range_loci_cover_chr_dict,
                                            'base': s_range_base_cover_chr_dict,
                                            }

        self.merged_synteny_block_dict = merged_synteny_block_dict

    def plot(
            self,
            mode='base',
            highlight_synteny_blocks={},
            save_file=None,
            reverse=False,
            debug=False):

        self.get_sb_cover_dict()

        if isinstance(highlight_synteny_blocks, list):
            highlight_synteny_blocks = {'#A3E3FA': [
                each for each in highlight_synteny_blocks]}

        if mode == 'base':
            if self.sp2:
                self.dot_plot = DotPlotJob(self.sp1,
                                           self.sp2,
                                           self.merged_synteny_block_dict,
                                           self.cover_dict[self.sp1_id]['base'],
                                           self.cover_dict[self.sp2_id]['base'],
                                           )
            else:
                self.dot_plot = DotPlotJob(self.sp1,
                                           synteny_block_dict=self.merged_synteny_block_dict,
                                           sp1_base_cover_dict=self.cover_dict[self.sp1_id]['base'],
                                           )

            self.dot_plot.plot(
                save_file=save_file,
                reverse=reverse,
                debug=debug)
        elif mode == 'loci':
            if self.sp2:
                self.dot_plot = DotPlotJob(self.sp1,
                                           self.sp2,
                                           self.merged_synteny_block_dict,
                                           sp1_loci_cover_dict=self.cover_dict[self.sp1_id]['loci'],
                                           sp2_loci_cover_dict=self.cover_dict[self.sp2_id]['loci'],
                                           )
            else:
                self.dot_plot = DotPlotJob(self.sp1,
                                           synteny_block_dict=self.merged_synteny_block_dict,
                                           sp1_loci_cover_dict=self.cover_dict[self.sp1_id]['loci'],
                                           )
            self.dot_plot.plot(
                save_file=save_file,
                mode='loci',
                reverse=reverse, debug=debug,
                highlight_synteny_blocks=highlight_synteny_blocks)

    def get_gene_loci(self, sp, chr_id, gene):
        if gene is None:
            return chr_id, None
        if isinstance(gene, str):
            gene = sp.gene_dict[gene]
            chr_id = gene.chr_id
            gene_loci = gene.loci
            return chr_id, gene_loci
        elif isinstance(gene, int):
            gene_loci = gene
            if chr_id is None:
                raise ValueError(
                    'chr_id is required when gene is int')
            return chr_id, gene_loci

    def search_synteny_blocks(
            self,
            q_sp_id=None,
            q_chr_id=None,
            q_from_gene=None,
            q_to_gene=None,
            s_sp_id=None,
            s_chr_id=None,
            s_from_gene=None,
            s_to_gene=None):


        if q_sp_id == self.sp1.id:
            sp1_id, sp1_chr_id, sp1_from_gene, sp1_to_gene = q_sp_id, q_chr_id, q_from_gene, q_to_gene
            sp2_id, sp2_chr_id, sp2_from_gene, sp2_to_gene = s_sp_id, s_chr_id, s_from_gene, s_to_gene
        else:
            sp1_id, sp1_chr_id, sp1_from_gene, sp1_to_gene = s_sp_id, s_chr_id, s_from_gene, s_to_gene
            sp2_id, sp2_chr_id, sp2_from_gene, sp2_to_gene = q_sp_id, q_chr_id, q_from_gene, q_to_gene

        sp1_chr_id, sp1_from_gene = self.get_gene_loci(
            self.sp1, sp1_chr_id, sp1_from_gene)
        sp1_chr_id, sp1_to_gene = self.get_gene_loci(
            self.sp1, sp1_chr_id, sp1_to_gene)
        if self.sp2:
            sp2_chr_id, sp2_from_gene = self.get_gene_loci(
                self.sp2, sp2_chr_id, sp2_from_gene)
            sp2_chr_id, sp2_to_gene = self.get_gene_loci(
                self.sp2, sp2_chr_id, sp2_to_gene)
        else:
            sp2_chr_id, sp2_from_gene = self.get_gene_loci(
                self.sp1, sp2_chr_id, sp2_from_gene)
            sp2_chr_id, sp2_to_gene = self.get_gene_loci(
                self.sp1, sp2_chr_id, sp2_to_gene)

        # set default values
        sp1_range = None
        sp2_range = None

        # set range
        if sp1_from_gene is not None and sp1_to_gene is not None:
            sp1_range = (sp1_from_gene, sp1_to_gene)
        elif sp1_from_gene is not None and sp1_to_gene is None:
            sp1_range = (sp1_from_gene, sp1_from_gene)

        if sp2_from_gene is not None and sp2_to_gene is not None:
            sp2_range = (sp2_from_gene, sp2_to_gene)
        elif sp2_from_gene is not None and sp2_to_gene is None:
            sp2_range = (sp2_from_gene, sp2_from_gene)

        # print(
        #     "sp1_chr_id is %s, sp2_chr_id is %s, sp1_range is %s, sp2_range is %s" %
        #     (sp1_chr_id, sp2_chr_id, str(sp1_range), str(sp2_range)))
        if hasattr(self, 'merged_synteny_block_dict'):
            synteny_block_dict = self.merged_synteny_block_dict
        else:
            synteny_block_dict = self.synteny_block_dict

        if self.sp2:
            searched_synteny_blocks_dict = search_synteny_blocks(
                synteny_block_dict,
                sp1_chr_id,
                sp1_range,
                sp2_chr_id,
                sp2_range)
        else:
            searched_synteny_blocks_dict_1 = search_synteny_blocks(
                synteny_block_dict,
                sp1_chr_id,
                sp1_range,
                sp2_chr_id,
                sp2_range)
            searched_synteny_blocks_dict_2 = search_synteny_blocks(
                synteny_block_dict,
                sp2_chr_id,
                sp2_range,
                sp1_chr_id,
                sp1_range)
            
            searched_synteny_blocks_dict = {}
            for sb_id in searched_synteny_blocks_dict_1:
                searched_synteny_blocks_dict[sb_id] = searched_synteny_blocks_dict_1[sb_id]
            for sb_id in searched_synteny_blocks_dict_2:
                searched_synteny_blocks_dict[sb_id] = searched_synteny_blocks_dict_2[sb_id]
        
        return searched_synteny_blocks_dict


def search_synteny_blocks(
        synteny_block_dict,
        sp1_chr_id=None,
        sp1_range=None,
        sp2_chr_id=None,
        sp2_range=None):
    report_sb_dict = {}

    for sb_id in synteny_block_dict:
        sb = synteny_block_dict[sb_id]

        if sp1_chr_id:
            if sb.q_chr != sp1_chr_id:
                continue
        if sp2_chr_id:
            if sb.s_chr != sp2_chr_id:
                continue
        if sp1_range:
            if section(
                (sb.first_q_gene_loci,
                 sb.last_q_gene_loci),
                sp1_range,
                    int_flag=True, just_judgement=True) == False:
                continue
        if sp2_range:
            if section(
                (sb.first_s_gene_loci,
                 sb.last_s_gene_loci),
                sp2_range,
                    int_flag=True, just_judgement=True) == False:
                continue

        report_sb_dict[sb_id] = sb

    return report_sb_dict


class SyntenyLinkPlotJob(object):
    def __init__(self, block_dict, block_para_dict, link_dict):
        self.block_dict = block_dict
        self.block_para_dict = block_para_dict
        self.link_dict = link_dict

    def plot(self, figsize=(15, 15), x_lim=(-2000, 2000), y_lim=(-2000, 2000),
             save_file=None, debug=False):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)

        # plot genome blocks
        self.block_transdata_dict = {}
        for gb_id in self.block_dict:
            gb = self.block_dict[gb_id]
            t = self.block_plot(ax, gb, **self.block_para_dict[gb_id])
            self.block_transdata_dict[gb_id] = t

        # plot links
        for gb_id1, gb_id2 in combinations(list(self.block_dict.keys()), 2):
            if (gb_id1, gb_id2) in self.link_dict:
                gp_list = self.link_dict[(gb_id1, gb_id2)]
                self.link_plot(ax, gb_id1, gb_id2, gp_list)
            elif (gb_id2, gb_id1) in self.link_dict:
                gp_list = self.link_dict[(gb_id2, gb_id1)]
                self.link_plot(ax, gb_id2, gb_id1, gp_list)

        if debug:
            plt.grid(True)

            for gb_id in self.block_dict:
                gb = self.block_dict[gb_id]
                plot_str = "%s: %s %s base:%d-%d(%d) gene:%d-%d(%d)" % (gb_id, gb.sp_id, gb.chr_id, gb.start, gb.end, gb.length, gb.first_gene.loci, gb.last_gene.loci, gb.gene_number)

                print(plot_str)

                plot_point = self.reget_ax_point(
                    (gb.start, 20), self.block_transdata_dict[gb_id], ax)

                print(plot_point)

                ax.text(*plot_point, plot_str)

        else:
            plt.axis('off')

        ax.set_xlim(*x_lim)
        ax.set_ylim(*y_lim)

        plt.show()

        if save_file:
            fig.savefig(save_file, format='pdf', facecolor='none',
                        edgecolor='none', bbox_inches='tight')

        plt.close(fig)

    def block_plot(self, ax, gb, **kwargs):
        block_para_dict = {
            'shift_site': (0, 0),
            'strand': '+',
            'plot_length': 100000,
            'rotate_deg': 0,
            'back_color': '#6D6D6D',
            'plus_color': '#19ADD3',
            'minus_color': '#2AAC3F',
            'back_zorder': 10,
            'back_width': 3,
            'gene_box_width': 8,
            'gene_box_ec_width': 1,
            'gene_box_zorder': 20,
        }

        for i in kwargs:
            block_para_dict[i] = kwargs[i]

        gene_list = []
        for g in gb.gene_list:
            if g.chr_id == gb.chr_id and section(
                    g.range, (gb.start, gb.end), True, True):
                gene_list.append(g)

        # trans_base = 150

        affline = mtransforms.Affine2D().translate(-(gb.start - gb.length *
                                                     0.05 + gb.length * 1.1 / 2), 0)

        if block_para_dict['strand'] == '-':
            # affline = affline.rotate_deg_around(0,0,180)
            affline = affline.rotate_deg(180)

        # affline = affline.scale(plot_length/gb.length, 1).translate(shift_site[0], shift_site[1]).translate(0, -(math.sqrt(trans_base**2 + (2*trans_base)**2)))
        affline = affline.scale(
            block_para_dict['plot_length'] /
            gb.length,
            1).translate(
            block_para_dict['shift_site'][0],
            block_para_dict['shift_site'][1]).rotate_deg_around(
            block_para_dict['shift_site'][0],
            block_para_dict['shift_site'][1],
            block_para_dict['rotate_deg'])

        t = affline + ax.transData

        ax.plot([gb.start - gb.length * 0.05,
                 gb.end + gb.length * 0.05],
                [0,
                 0],
                linewidth=block_para_dict['back_width'],
                color=block_para_dict['back_color'],
                zorder=block_para_dict['back_zorder'],
                transform=t)

        for gf in gene_list:
            if (gf.strand == '+' and block_para_dict['strand'] ==
                    '+') or (gf.strand == '-' and block_para_dict['strand'] == '-'):
                color = block_para_dict['plus_color']
            else:
                color = block_para_dict['minus_color']
            rect = self.gene_box(
                gf.start,
                gf.end,
                box_width=block_para_dict['gene_box_width'],
                facecolor=color,
                ec=color,
                linewidth=block_para_dict['gene_box_ec_width'],
                zorder=block_para_dict['gene_box_zorder'],
                transform=t)
            ax.add_patch(rect)

        return t

    def link_plot(self, ax, gb_id1, gb_id2, gp_list, default_color='#DDDDDD'):
        gb1_gene_dict = {g.id: g for g in self.block_dict[gb_id1].gene_list}
        gb2_gene_dict = {g.id: g for g in self.block_dict[gb_id2].gene_list}

        for gp in gp_list:
            g1 = gp[0]
            g2 = gp[1]

            if g1 in gb1_gene_dict and g2 in gb2_gene_dict:
                g1f = gb1_gene_dict[g1]
                g2f = gb2_gene_dict[g2]
            elif g2 in gb1_gene_dict and g1 in gb2_gene_dict:
                g1f = gb2_gene_dict[g1]
                g2f = gb1_gene_dict[g2]
            else:
                raise ValueError(
                    "%s %s can not be found in %s or %s" %
                    (g1, g2, gb_id1, gb_id2))

            plt_1s = self.reget_ax_point(
                (g1f.start, 0), self.block_transdata_dict[gb_id1], ax)
            plt_1e = self.reget_ax_point(
                (g1f.end, 0), self.block_transdata_dict[gb_id1], ax)

            plt_2s = self.reget_ax_point(
                (g2f.start, 0), self.block_transdata_dict[gb_id2], ax)
            plt_2e = self.reget_ax_point(
                (g2f.end, 0), self.block_transdata_dict[gb_id2], ax)

            self.collinear_bar(
                ax, [
                    plt_1s, plt_1e], [
                    plt_2s, plt_2e], facecolor=default_color)

            if len(gp) > 2:
                self.collinear_bar(
                    ax, [
                        plt_1s, plt_1e], [
                        plt_2s, plt_2e], facecolor=gp[2])

    def reget_ax_point(self, point, transData, ax):
        inv = ax.transData.inverted()
        return inv.transform(transData.transform(point))

    def gene_box(self, start, end, chr_line=0, box_width=1, **kwargs):
        if end < start:
            start, end = end, start

        rectangle_anchor_point = start, chr_line - 0.5 * box_width
        rectangle_width = end - start + 1
        rectangle_height = box_width

        return Patches.Rectangle(
            rectangle_anchor_point,
            rectangle_width,
            rectangle_height,
            **kwargs)

    def collinear_bar(
            self,
            ax,
            A_range,
            B_range,
            facecolor='orange',
            alpha=1,
            A_y=2,
            A_y_c=1,
            B_y=-2,
            B_y_c=-1):

        A_start, A_end = A_range
        B_start, B_end = B_range

        if A_start[0] > A_end[0]:
            tmp = A_start
            A_start = A_end
            A_end = tmp

        if B_start[0] > B_end[0]:
            tmp = B_start
            B_start = B_end
            B_end = tmp

        A_sx, A_sy = A_start
        A_ex, A_ey = A_end

        B_sx, B_sy = B_start
        B_ex, B_ey = B_end

        verts = [
            (A_sx, A_sy),
            (A_ex, A_ey),
            (A_ex, (B_ey + A_ey) / 2),
            (B_ex, (B_ey + A_ey) / 2),
            (B_ex, B_ey),
            (B_sx, B_sy),
            (B_sx, (A_sy + B_sy) / 2),
            (A_sx, (A_sy + B_sy) / 2),
            (A_sx, A_sy),
            (A_sx, A_sy),
        ]

        # print(verts)

        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]

        path = Path(verts, codes)

        patch = Patches.PathPatch(
            path,
            facecolor=facecolor,
            alpha=alpha,
            lw=0.5,
            ec=facecolor)
        ax.add_patch(patch)


if __name__ == '__main__':
    # example for synteny blocks and DotPlotJob

    ## input: gff file and gene pair file
    sp1_id = 'Cca'
    sp1_gff = '/lustre/home/xuyuxing/tmp/T49390N0.genome.gff3'
    sp2_id = 'Sly'
    sp2_gff = '/lustre/home/xuyuxing/tmp/T4081N0.genome.gff3'
    gene_pair_file = '/lustre/home/xuyuxing/tmp/mcscanx.homology'

    ## build synteny blocks
    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, sp2_id, sp2_gff, gene_pair_file)
    sb_job.build_synteny_blocks()

    ## write synteny blocks to file
    mcscan_output_file = "/lustre/home/xuyuxing/tmp/mcscanx.collinearity"
    sb_job.write_mcscan_output(mcscan_output_file)

    ## Or you can read synteny blocks from file
    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, sp2_id, sp2_gff)
    sb_job.read_mcscan_output(mcscan_output_file)

    ## You can also work with only one genome
    sb_job = GenomeSyntenyBlockJob(
        sp1_id, sp1_gff, gene_pair_file=gene_pair_file)

    ## plot synteny blocks in dotplot
    sb_job.plot()
    highlight_sb_list = [65, 178, 237, 331]
    sb_job.plot(mode='loci', reverse=True, highlight_synteny_blocks=highlight_sb_list)

    # example for genome blocks and SyntenyLinkPlotJob
    ## load data
    sp1 = 'Ase'
    sp2 = 'Atr'
    sp1_gff = '/lustre/home/xuyuxing/Work/orchidWGD/ocftools/1.prepare/gene_filter/Ase.filter.gff3'
    sp2_gff = '/lustre/home/xuyuxing/Work/orchidWGD/ocftools/1.prepare/gene_filter/Atr.filter.gff3'
    mcscan_output_file = '/lustre/home/xuyuxing/Work/orchidWGD/ocftools/3.OCF_filter_iqtree/Ase_Atr/ocf_filtered_mcscan.txt'

    genome_dict = {
        sp1: Genome(sp1, sp1_gff),
        sp2: Genome(sp2, sp2_gff),
    }

    sb_job = GenomeSyntenyBlockJob(
        sp1, sp1_gff, sp2, sp2_gff)
    sb_job.read_mcscan_output(mcscan_output_file)
    sb_job.get_sb_cover_dict()

    ##
    block_info_dict = {
        'B1': ('Ase', 'T272863N0C001', 2331, 2600),
        'B2': ('Atr', 'T13333N0C0011', 0, 217)
    }

    block_dict = {}
    for b_id in block_info_dict:
        sp_id, chr_id, start, end = block_info_dict[b_id]
        block_dict[b_id] = GenomeBlock(
            b_id, sp_id, chr_id, start, end)
        block_dict[b_id].get_full_info(genome_dict[sp_id])


    link_dict = {}
    for gb_id1, gb_id2 in combinations(list(block_dict.keys()), 2):
        link_dict[(gb_id1, gb_id2)] = []

        gb1 = block_dict[gb_id1]
        gb2 = block_dict[gb_id2]

        if gb1.sp_id == gb2.sp_id:
            continue

        sb_dict = sb_job.search_synteny_blocks(
            q_sp_id=gb1.sp_id,
            q_chr_id=gb1.chr_id,
            q_from_gene=gb1.first_gene.loci,
            q_to_gene=gb1.last_gene.loci,
            s_sp_id=gb2.sp_id,
            s_chr_id=gb2.chr_id,
            s_from_gene=gb2.first_gene.loci,
            s_to_gene=gb2.last_gene.loci)

        for sb_id in sb_dict:
            sb = sb_dict[sb_id]
            for gp_id in sb.gene_pair_dict:
                gp = sb.gene_pair_dict[gp_id]
                link_dict[(gb_id1, gb_id2)].append(
                    (gp.q_gene.id, gp.s_gene.id))

    block_para_dict = {
        'B1': {'strand':'+', 'shift_site': (0, 100), 'plot_length': block_dict['B1'].length / 1000},
        'B2': {'strand':'-', 'shift_site': (0, -100), 'plot_length': block_dict['B2'].length / 1000},
    }

    sl_plot_job = SyntenyLinkPlotJob(
        block_dict=block_dict,
        block_para_dict=block_para_dict,
        link_dict=link_dict)
    sl_plot_job.plot(x_lim=(-5000, 5000), y_lim=(-400, 400),
                    save_file=None, debug=True)

