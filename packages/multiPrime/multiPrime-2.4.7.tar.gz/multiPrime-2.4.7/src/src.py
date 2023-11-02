#!/usr/bin/env python3
import pickle

from .utils import *
from multiprocessing import Manager
from collections import defaultdict
import re
import os
from concurrent.futures import ProcessPoolExecutor
import json
import pandas as pd
from itertools import product, repeat, takewhile
from statistics import mean
from bisect import bisect_left
from pathlib import Path
import multiprocessing


class NN_degenerate(object):
    def __init__(self, seq_file, primer_length=18, coverage=0.8, number_of_dege_bases=18, score_of_dege_bases=1000,
                 product_len=250, position="2,-1", variation=2, raw_entropy_threshold=3.6, distance=4, GC="0.4,0.6",
                 nproc=10, outfile=""):
        self.primer_length = primer_length  # primer length
        self.coverage = coverage  # min coverage
        self.number_of_dege_bases = number_of_dege_bases
        self.score_of_dege_bases = score_of_dege_bases
        self.product = product_len
        self.position = position  # gap position
        self.Y_strict, self.Y_strict_R = self.get_Y()
        self.variation = variation  # coverage of n-nt variation and max_gap_number
        self.distance = distance  # haripin
        self.GC = GC.split(",")
        self.nproc = nproc  # GC content
        self.seq_dict, self.total_sequence_number = self.parse_seq(seq_file)
        self.position_list = self.seq_attribute(self.seq_dict)
        self.start_position = self.position_list[0]
        self.stop_position = self.position_list[1]
        self.length = self.position_list[2]
        self.raw_entropy_threshold = raw_entropy_threshold
        self.entropy_threshold = self.entropy_threshold_adjust(self.length)
        self.outfile = outfile
        self.resQ = Manager().Queue()

    # expand degenerate primer into a list.
    @staticmethod
    def degenerate_seq(primer):
        seq = []
        cs = ""
        for s in primer:
            if s not in degenerate_base:
                cs += s
            else:
                seq.append([cs + i for i in degenerate_base[s]])
                cs = ""
        if cs:
            seq.append([cs])
        return ["".join(i) for i in product(*seq)]

    ##################################################
    ################# pre_filter #####################
    ##################################################

    ################### hairpin ######################
    def hairpin_check(self, primer):
        n = 0
        distance = self.distance
        while n <= len(primer) - 5 - 5 - distance:
            kmer = self.degenerate_seq(primer[n:n + 5])
            left = self.degenerate_seq(primer[n + 5 + distance:])
            for k in kmer:
                for l in left:
                    if re.search(RC(k), l):
                        return True
            n += 1
        return False

    ################# GC content #####################
    def GC_fraction(self, sequence):
        sequence_expand = self.degenerate_seq(sequence)
        GC_list = []
        for seq in sequence_expand:
            GC_list.append(round((list(seq).count("G") + list(seq).count("C")) / len(list(seq)), 3))
        GC_average = round(mean(GC_list), 2)
        return GC_average

    ################# di_nucleotide #####################
    def di_nucleotide(self, primer):
        primers = self.degenerate_seq(primer)
        for m in primers:
            for n in di_nucleotides:
                if re.search(n, m):
                    return True
        return False

    ################## GC Clamp ######################
    def GC_clamp(self, primer, num=4, length=13):
        for i in range(num, (num + length)):
            s = primer[-i:]
            gc_fraction = self.GC_fraction(s)
            if gc_fraction > 0.6:
                return True
        return False

    ################# position of degenerate base #####################
    def dege_filter_in_term_N_bp(self, sequence):
        term = self.position
        if term == 0:
            term_base = ["A"]
        else:
            term_base = sequence[-term:]
        score = score_trans(term_base)
        if score > 1:
            return True
        else:
            return False

    # Import multi-alignment results and return a dict ==> {ID：sequence}
    def parse_seq(self, Input):
        seq_dict = defaultdict(str)
        with open(Input, "r") as f:
            for i in f:
                if i.startswith("#"):
                    pass
                else:
                    if i.startswith(">"):
                        i = i.strip().split(" ")
                        acc_id = i[0]
                    else:
                        # carefully !, make sure that Ns have been replaced!
                        sequence = re.sub("[^ACGTRYMKSWHBVD]", "-", i.strip().upper())
                        seq_dict[acc_id] += sequence
        return seq_dict, len(seq_dict)

    def current_end(self, primer, adaptor="", num=5, length=14):
        primer_extend = adaptor + primer
        end_seq = []
        for i in range(num, (num + length)):
            s = primer_extend[-i:]
            if s:
                end_seq.extend(self.degenerate_seq(s))
        return end_seq

    def deltaG(self, sequence):
        Delta_G_list = []
        Na = 50
        for seq in self.degenerate_seq(sequence):
            Delta_G = 0
            for n in range(len(seq) - 1):
                base_i, base_j = base2bit[seq[n + 1]], base2bit[seq[n]]
                Delta_G += freedom_of_H_37_table[base_i][base_j] * H_bonds_number[base_i][base_j] + \
                           penalty_of_H_37_table[base_i][base_j]
            term5 = sequence[-2:]
            if term5 == "TA":
                Delta_G += adjust_initiation[seq[0]] + adjust_initiation[seq[-1]] + adjust_terminal_TA
            else:
                Delta_G += adjust_initiation[seq[0]] + adjust_initiation[seq[-1]]
            # adjust by concentration of Na+
            Delta_G -= (0.175 * math.log(Na / 1000, math.e) + 0.20) * len(seq)
            if symmetry(seq):
                Delta_G += symmetry_correction
            Delta_G_list.append(Delta_G)
        return round(max(Delta_G_list), 2)

    def dimer_check(self, primer):
        current_end = self.current_end(primer)
        current_end_sort = sorted(current_end, key=lambda i: len(i), reverse=True)
        for end in current_end_sort:
            for p in self.degenerate_seq(primer):
                idx = p.find(RC(end))
                if idx >= 0:
                    end_length = len(end)
                    end_GC = end.count("G") + end.count("C")
                    end_d1 = 0
                    end_d2 = len(p) - len(end) - idx
                    Loss = Penalty_points(
                        end_length, end_GC, end_d1, end_d2)
                    delta_G = self.deltaG(end)
                    if Loss >= 3 or (delta_G < -5 and (end_d1 == end_d2)):
                        return True
        return False

    ####################################################################
    ##### pre-filter by GC content / di-nucleotide / hairpin ###########
    def primer_pre_filter(self, primer):
        information = []
        min_GC, max_GC = self.GC
        primer_GC_content = self.GC_fraction(primer)
        if not float(min_GC) <= primer_GC_content <= float(max_GC):
            information.append("GC_out_of_range (" + str(primer_GC_content) + ")")
        if self.di_nucleotide(primer):
            information.append("di_nucleotide")
        if self.hairpin_check(primer):
            information.append("hairpin")

        if len(information) == 0:
            return primer_GC_content
        else:
            return '|'.join(information)

    ####################################################################
    # if full degenerate primer is ok, we don't need to continue NN-array
    def pre_degenerate_primer_check(self, primer):
        primer_degeneracy = score_trans(primer)
        primer_dege_number = dege_number(primer)
        if primer_degeneracy < self.score_of_dege_bases and primer_dege_number < self.number_of_dege_bases:
            return True
        else:
            return False

    def full_degenerate_primer(self, freq_matrix):
        # degenerate transformation in each position
        max_dege_primers = ''
        for col in freq_matrix.columns.values:
            tmp = freq_matrix[freq_matrix[col] > 0].index.values.tolist()
            max_dege_primers += trans_score_table[round(sum([score_table[x] for x in tmp]), 2)]
        return max_dege_primers

    def state_matrix(self, primers_db):
        pieces = []
        for col in primers_db.columns.values:
            tmp_series = primers_db[col].value_counts()  # (normalize=True)
            tmp_series.name = col
            pieces.append(tmp_series)
        nodes = pd.concat(pieces, axis=1)
        nodes.fillna(0, inplace=True)
        nodes = nodes.sort_index(ascending=True)
        nodes = nodes.astype(int)
        row_names = nodes.index.values.tolist()
        if "-" in row_names:
            nodes.drop("-", inplace=True, axis=0)
        return nodes

    def di_matrix(self, primers):
        primers_trans = []
        for i in primers.keys():
            slice = []
            for j in range(len(i) - 1):
                slice.append(i[j:j + 2])
            primers_trans.extend(repeat(slice, primers[i]))
        return pd.DataFrame(primers_trans)

    def trans_matrix(self, primers):
        primers_di_db = self.di_matrix(primers)
        pieces = []
        for col in primers_di_db.columns.values:
            tmp_list = []
            for i in di_bases:
                # row: A, T, C ,G; column: A, T, C, G
                number = list(primers_di_db[col]).count(i)
                tmp_list.append(number)
            pieces.append(tmp_list)
        a, b = primers_di_db.shape
        trans = np.array(pieces).reshape(b, 4, 4)
        return trans

    def get_optimal_primer_by_viterbi(self, nodes, trans):
        nodes = np.array(nodes.T)
        seq_len, num_labels = len(nodes), len(trans[0])
        labels = np.arange(num_labels).reshape((1, -1))
        scores = nodes[0].reshape((-1, 1))
        primer_index = labels
        for t in range(1, seq_len):
            observe = nodes[t].reshape((1, -1))
            current_trans = trans[t - 1]
            M = scores + current_trans + observe
            scores = np.max(M, axis=0).reshape((-1, 1))
            idxs = np.argmax(M, axis=0)
            primer_index = np.concatenate([primer_index[:, idxs], labels], 0)
        best_primer_index = primer_index[:, scores.argmax()]
        return best_primer_index

    def get_optimal_primer_by_MM(self, cover_for_MM):
        sort_cover = sorted(cover_for_MM.items(), key=lambda x: x[1], reverse=True)
        L_seq = list(sort_cover[0][0])
        best_primer_index = [base2bit[x] for x in L_seq]
        # Return the maximum of an array or maximum along an axis. axis=0 代表列 , axis=1 代表行
        return best_primer_index

    def entropy(self, cover, cover_number, gap_sequence, gap_sequence_number):
        # cBit: entropy of cover sequences
        # tBit: entropy of total sequences
        cBit = 0
        tBit = 0
        for c in cover.keys():
            cBit += (cover[c] / cover_number) * math.log((cover[c] / cover_number), 2)
            tBit += (cover[c] / (cover_number + gap_sequence_number)) * \
                    math.log((cover[c] / (cover_number + gap_sequence_number)), 2)
        for t in gap_sequence.keys():
            tBit += (gap_sequence[t] / (cover_number + gap_sequence_number)) * \
                    math.log((gap_sequence[t] / (cover_number + gap_sequence_number)), 2)
        return round(-cBit, 2), round(-tBit, 2)

    # Sequence processing. Return a list contains sequence length, start and stop position of each sequence.
    def seq_attribute(self, Input_dict):
        start_dict = {}
        stop_dict = {}
        # pattern_start = re.compile('[A-Z]')
        # pattern_stop = re.compile("-*$")
        for acc_id in Input_dict.keys():
            # start_dict[acc_id] = pattern_start.search(Input_dict[acc_id]).span()[0]
            # stop_dict[acc_id] = pattern_stop.search(Input_dict[acc_id]).span()[0] - 1
            t_length = len(Input_dict[acc_id])
            start_dict[acc_id] = t_length - len(Input_dict[acc_id].lstrip("-"))
            stop_dict[acc_id] = len(Input_dict[acc_id].rstrip("-"))
            # start position should contain [coverage] sequences at least.
        start = np.quantile(np.array(list(start_dict.values())).reshape(1, -1), self.coverage, interpolation="higher")
        # for python 3.9.9
        # start = np.quantile(np.array(list(start_dict.values())).reshape(1, -1), self.coverage, method="higher")
        # stop position should contain [coverage] sequences at least.
        stop = np.quantile(np.array(list(stop_dict.values())).reshape(1, -1), self.coverage, interpolation="lower")
        # stop = np.quantile(np.array(list(stop_dict.values())).reshape(1, -1), self.coverage, method="lower")
        if stop - start < int(self.product):
            print("Error: max length of PCR product is shorter than the default min Product length with {} "
                  "coverage! Non candidate primers !!!".format(self.coverage))
            sys.exit(1)
        else:
            return [start, stop, stop - start]

    def entropy_threshold_adjust(self, length):
        if length < 5000:
            return self.raw_entropy_threshold
        else:
            if length < 10000:
                return self.raw_entropy_threshold * 0.95
            else:
                return self.raw_entropy_threshold * 0.9

    def get_primers(self, sequence_dict, primer_start):  # , primer_info, non_cov_primer_out
        # record sequence and acc id
        non_gap_seq_id = defaultdict(list)
        # record sequence (no gap) and number
        cover = defaultdict(int)
        cover_for_MM = defaultdict(int)
        # record total coverage sequence number
        cover_number = 0
        # record sequence (> variation gap) and number
        gap_sequence = defaultdict(int)
        gap_seq_id = defaultdict(list)
        # record total sequence (> variation gap) number
        gap_sequence_number = 0
        primers_db = []
        for seq_id in sequence_dict.keys():
            sequence = sequence_dict[seq_id][primer_start:primer_start + self.primer_length].upper()
            # replace "-" which in start or stop position with nucleotides
            if sequence == "-" * self.primer_length:
                pass
            else:
                if sequence.startswith("-"):
                    sequence_narrow = sequence.lstrip("-")
                    append_base_length = len(sequence) - len(sequence_narrow)
                    left_seq = sequence_dict[seq_id][0:primer_start].replace("-", "")
                    if len(left_seq) >= append_base_length:
                        sequence = left_seq[len(left_seq) - append_base_length:] + sequence_narrow
                if sequence.endswith("-"):
                    sequence_narrow = sequence.rstrip("-")
                    append_base_length = len(sequence) - len(sequence_narrow)
                    right_seq = sequence_dict[seq_id][primer_start + self.primer_length:].replace("-", "")
                    if len(right_seq) >= append_base_length:
                        sequence = sequence_narrow + right_seq[0:append_base_length]
            if len(sequence) < self.primer_length:
                append_base_length = self.primer_length - len(sequence)
                left_seq = sequence_dict[seq_id][0:primer_start].replace("-", "")
                if len(left_seq) >= append_base_length:
                    sequence = left_seq[len(left_seq) - append_base_length:] + sequence
            # gap number. number of gap > 2
            if list(sequence).count("-") > self.variation:
                gap_sequence[sequence] += 1
                gap_sequence_number += 1
                if round(gap_sequence_number / self.total_sequence_number, 2) >= (1 - self.coverage):
                    break
                else:
                    # record acc ID of gap sequences
                    expand_sequence = self.degenerate_seq(sequence)
                    for i in expand_sequence:
                        gap_seq_id[i].append(seq_id)
            # # accepted gap, number of gap <= variation
            else:
                expand_sequence = self.degenerate_seq(sequence)
                cover_number += 1
                for i in expand_sequence:
                    cover[i] += 1
                    primers_db.append(list(i))
                    # record acc ID of non gap sequences, which is potential mis-coverage
                    non_gap_seq_id[i].append(seq_id)
                    if re.search("-", i):
                        pass
                    else:
                        cover_for_MM[i] += 1
        # number of sequences with too many gaps greater than (1 - self.coverage)
        if round(gap_sequence_number / self.total_sequence_number, 2) >= (1 - self.coverage):
            # print("Gap fail")
            self.resQ.put(None)
        elif len(cover) < 1:
            self.resQ.put(None)
            # print("Cover fail")
        else:
            # cBit: entropy of cover sequences
            # tBit: entropy of total sequences
            cBit, tBit = self.entropy(cover, cover_number, gap_sequence, gap_sequence_number)
            if tBit > self.entropy_threshold:
                # print("Entropy fail")
                # This window is not a conserved region, and not proper to design primers
                self.resQ.put(None)
            else:
                primers_db = pd.DataFrame(primers_db)
                # frequency matrix
                freq_matrix = self.state_matrix(primers_db)
                # print(freq_matrix)
                colSum = np.sum(freq_matrix, axis=0)
                a, b = freq_matrix.shape
                # a < 4 means base composition of this region is less than 4 (GC bias).
                # It's not a proper region for primer design.
                if a < 4:
                    self.resQ.put(None)
                elif (colSum == 0).any():
                    # print(colSum)  # if 0 in array; pass
                    self.resQ.put(None)
                else:
                    gap_seq_id_info = [primer_start, gap_seq_id]
                    mismatch_coverage, non_cov_primer_info = \
                        self.degenerate_by_NN_algorithm(primer_start, freq_matrix, cover, non_gap_seq_id,
                                                        cover_for_MM, cover_number, cBit, tBit)
                    # self.resQ.put([mismatch_coverage, non_cov_primer_info, gap_seq_id_info])
                    # F, R = mismatch_coverage[1][6], mismatch_coverage[1][7]
                    sequence = mismatch_coverage[1][2]
                    if self.dimer_check(sequence):
                        # print("Dimer fail")
                        self.resQ.put(None)
                    else:
                        self.resQ.put([mismatch_coverage, non_cov_primer_info, gap_seq_id_info])
                    # if F < cover_number * 0.5 or R < cover_number * 0.5:
                    #     self.resQ.put(None)
                    # else:
                    #     self.resQ.put([mismatch_coverage, non_cov_primer_info, gap_seq_id_info])

    def degenerate_by_NN_algorithm(self, primer_start, freq_matrix, cover, non_gap_seq_id, cover_for_MM,
                                   cover_number, cBit, tBit):
        # full degenerate primer
        # full_degenerate_primer = self.full_degenerate_primer(freq_matrix)
        # unique covered primers, which is used to calculate coverage and
        # mis-coverage in the following step.
        cover_primer_set = set(cover.keys())
        # if full_degenerate_primer is ok, then return full_degenerate_primer
        # mismatch_coverage, non_cov_primer_info = {}, {}
        F_non_cover, R_non_cover = {}, {}
        ######################################################################################################
        ############ need prone. not all primers is proper for primer-F or primer-R ##########################
        # If a primer is located in the start region, there is no need to calculate its coverage for primer-R#
        ## here is a suggestion. we can assert candidate primer as primer-F or primer-R by primer attribute ##
        ######################################################################################################
        NN_matrix = self.trans_matrix(cover)
        if len(cover_for_MM) != 0:
            optimal_primer_index_NM = self.get_optimal_primer_by_viterbi(freq_matrix, NN_matrix)
            optimal_primer_index_MM = self.get_optimal_primer_by_MM(cover_for_MM)
            # print(optimal_primer_index_NM.tolist()) # array
            # print(optimal_primer_index_MM) # list
            #  if (optimal_primer_index_NM == optimal_primer_index_MM).all():
            if optimal_primer_index_NM.tolist() == optimal_primer_index_MM:
                optimal_primer_index = optimal_primer_index_NM
                row_names = np.array(freq_matrix.index.values).reshape(1, -1)
                # build a list to store init base information in each position.
                optimal_primer_list = row_names[:, optimal_primer_index][0].tolist()
                # initiation coverage (optimal primer, used as base coverage)
                optimal_coverage_init = cover["".join(optimal_primer_list)]
                optimal_primer_current, F_mis_cover, R_mis_cover, information, F_non_cover, R_non_cover = \
                    self.coverage_stast(cover, optimal_primer_index, NN_matrix, optimal_coverage_init, cover_number,
                                        optimal_primer_list, cover_primer_set, non_gap_seq_id, F_non_cover,
                                        R_non_cover)
                # print(F_mis_cover)
                # print(R_mis_cover)
            else:
                F_non_cover_NM, R_non_cover_NM, F_non_cover_MM, R_non_cover_MM = {}, {}, {}, {}
                row_names = np.array(freq_matrix.index.values).reshape(1, -1)
                # build a list to store init base information in each position.
                optimal_primer_list_NM = row_names[:, optimal_primer_index_NM][0].tolist()
                # initiation coverage (optimal primer, used as base coverage)
                optimal_coverage_init_NM = cover["".join(optimal_primer_list_NM)]
                NN_matrix_NM = NN_matrix.copy()
                optimal_primer_current_NM, F_mis_cover_NM, R_mis_cover_NM, information_NM, F_non_cover_NM, \
                R_non_cover_NM = self.coverage_stast(cover, optimal_primer_index_NM, NN_matrix_NM,
                                                     optimal_coverage_init_NM, cover_number, optimal_primer_list_NM,
                                                     cover_primer_set, non_gap_seq_id, F_non_cover_NM,
                                                     R_non_cover_NM)
                optimal_primer_list_MM = row_names[:, optimal_primer_index_MM][0].tolist()
                # initiation coverage (optimal primer, used as base coverage)
                optimal_coverage_init_MM = cover["".join(optimal_primer_list_MM)]
                NN_matrix_MM = NN_matrix.copy()
                optimal_primer_current_MM, F_mis_cover_MM, R_mis_cover_MM, information_MM, F_non_cover_MM, \
                R_non_cover_MM = self.coverage_stast(cover, optimal_primer_index_MM, NN_matrix_MM,
                                                     optimal_coverage_init_MM, cover_number,
                                                     optimal_primer_list_MM, cover_primer_set, non_gap_seq_id,
                                                     F_non_cover_MM, R_non_cover_MM)
                if (F_mis_cover_NM + R_mis_cover_NM) > (F_mis_cover_MM + R_mis_cover_MM):
                    optimal_primer_current, F_mis_cover, R_mis_cover, information, optimal_coverage_init, \
                    F_non_cover, R_non_cover, NN_matrix = optimal_primer_current_NM, F_mis_cover_NM, \
                                                          R_mis_cover_NM, information_NM, optimal_coverage_init_NM, \
                                                          F_non_cover_NM, R_non_cover_NM, NN_matrix_NM
                else:
                    optimal_primer_current, F_mis_cover, R_mis_cover, information, optimal_coverage_init, \
                    F_non_cover, R_non_cover, NN_matrix = optimal_primer_current_MM, F_mis_cover_MM, \
                                                          R_mis_cover_MM, information_MM, optimal_coverage_init_MM, \
                                                          F_non_cover_MM, R_non_cover_MM, NN_matrix_MM
                # print(F_mis_cover)
                # print(R_mis_cover)
        else:
            optimal_primer_index_NM = self.get_optimal_primer_by_viterbi(freq_matrix, NN_matrix)
            F_non_cover_NM, R_non_cover_NM, F_non_cover_MM, R_non_cover_MM = {}, {}, {}, {}
            row_names = np.array(freq_matrix.index.values).reshape(1, -1)
            # build a list to store init base information in each position.
            optimal_primer_list_NM = row_names[:, optimal_primer_index_NM][0].tolist()
            # initiation coverage (optimal primer, used as base coverage)
            optimal_coverage_init_NM = cover["".join(optimal_primer_list_NM)]
            NN_matrix_NM = NN_matrix.copy()
            optimal_primer_current_NM, F_mis_cover_NM, R_mis_cover_NM, information_NM, F_non_cover_NM, \
            R_non_cover_NM = self.coverage_stast(cover, optimal_primer_index_NM, NN_matrix_NM,
                                                 optimal_coverage_init_NM, cover_number, optimal_primer_list_NM,
                                                 cover_primer_set, non_gap_seq_id, F_non_cover_NM, R_non_cover_NM)
            optimal_primer_current, F_mis_cover, R_mis_cover, information, optimal_coverage_init, F_non_cover, \
            R_non_cover, NN_matrix = optimal_primer_current_NM, F_mis_cover_NM, R_mis_cover_NM, information_NM, \
                                     optimal_coverage_init_NM, F_non_cover_NM, R_non_cover_NM, NN_matrix_NM
            # print(F_mis_cover)
            # print(R_mis_cover)
        nonsense_primer_number = len(set(self.degenerate_seq(optimal_primer_current)) - set(cover.keys()))
        primer_degenerate_number = dege_number(optimal_primer_current)
        Tm, coverage = [], []
        for seq in self.degenerate_seq(optimal_primer_current):
            Tm.append(Calc_Tm_v2(seq))
            coverage.append(cover[seq])
        Tm_average = round(mean(Tm), 2)
        perfect_coverage = sum(coverage)
        out_mismatch_coverage = [primer_start, [cBit, tBit, optimal_primer_current, primer_degenerate_number,
                                                nonsense_primer_number, perfect_coverage, F_mis_cover,
                                                R_mis_cover, Tm_average, information]]
        non_cov_primer_info = [primer_start, [F_non_cover, R_non_cover]]
        return out_mismatch_coverage, non_cov_primer_info

    def coverage_stast(self, cover, optimal_primer_index, NN_matrix, optimal_coverage_init, cover_number,
                       optimal_primer_list, cover_primer_set, non_gap_seq_id, F_non_cover, R_non_cover):
        # if the coverage is too low, is it necessary to refine?
        # mis-coverage as threshold? if mis-coverage reached to 100% but degeneracy is still very low,
        optimal_NN_index = []
        optimal_NN_coverage = []
        for idx in range(len(optimal_primer_index) - 1):
            # NN index
            optimal_NN_index.append([optimal_primer_index[idx], optimal_primer_index[idx + 1]])
            # NN coverage
            # Is the minimum number in NN coverage = optimal_primer_coverage ? No!
            optimal_NN_coverage.append(
                NN_matrix[idx, optimal_primer_index[idx], optimal_primer_index[idx + 1]])
        # mis-coverage initialization
        F_mis_cover_cover, F_non_cover_in_cover, R_mis_cover_cover, R_non_cover_in_cover = \
            self.mis_primer_check(cover_primer_set, ''.join(optimal_primer_list), cover,
                                  non_gap_seq_id)
        # print(optimal_coverage_init + F_mis_cover_cover)
        # print(optimal_coverage_init + R_mis_cover_cover)
        # print(cover_number)
        # print(optimal_primer_list)
        if optimal_coverage_init + F_mis_cover_cover < cover_number or \
                optimal_coverage_init + R_mis_cover_cover < cover_number:
            while optimal_coverage_init + F_mis_cover_cover < cover_number or \
                    optimal_coverage_init + R_mis_cover_cover < cover_number:
                # optimal_primer_update, coverage_update, NN_coverage_update,
                # NN array_update, degeneracy_update, degenerate_update
                optimal_primer_list, optimal_coverage_init, optimal_NN_coverage_update, \
                NN_matrix, degeneracy, number_of_degenerate = \
                    self.refine_by_NN_array(optimal_primer_list, optimal_coverage_init, cover, optimal_NN_index,
                                            optimal_NN_coverage, NN_matrix)
                F_mis_cover_cover, F_non_cover_in_cover, R_mis_cover_cover, R_non_cover_in_cover = \
                    self.mis_primer_check(cover_primer_set, ''.join(optimal_primer_list), cover,
                                          non_gap_seq_id)
                # If there is no increase in NN_coverage,
                # it suggests the presence of bugs or a mismatch in continuous positions.
                # Is this step necessary? or shall we use DegePrime method? or shall we use machine learning?
                if max(F_mis_cover_cover, R_mis_cover_cover) == cover_number:
                    break
                elif optimal_NN_coverage_update == optimal_NN_coverage:
                    break
                # If the degeneracy exceeds the threshold, the loop will break.
                elif 2 * degeneracy > self.score_of_dege_bases or 3 * degeneracy / 2 > self.score_of_dege_bases \
                        or number_of_degenerate == self.number_of_dege_bases:
                    break
                else:
                    optimal_NN_coverage = optimal_NN_coverage_update
        # If the primer coverage does not increase after degeneration,
        # the process will backtrack and assess the original optimal primer.
        # print(optimal_primer_list)
        optimal_primer_current = ''.join(optimal_primer_list)
        information = self.primer_pre_filter(optimal_primer_current)
        # F_mis_cover_cover, F_non_cover_in_cover, R_mis_cover_cover, R_non_cover_in_cover = \
        #     self.mis_primer_check(cover_primer_set, optimal_primer_current, cover,
        #                           non_gap_seq_id)
        F_non_cover.update(F_non_cover_in_cover)
        R_non_cover.update(R_non_cover_in_cover)
        F_mis_cover = optimal_coverage_init + F_mis_cover_cover
        R_mis_cover = optimal_coverage_init + R_mis_cover_cover
        # print(F_mis_cover)
        return optimal_primer_current, F_mis_cover, R_mis_cover, information, F_non_cover, R_non_cover

    def refine_by_NN_array(self, optimal_primer_list, optimal_coverage_init, cover,
                           optimal_NN_index, optimal_NN_coverage, NN_array):
        # use minimum index of optimal_NN_coverage as the position to refine
        refine_index = np.where(optimal_NN_coverage == np.min(optimal_NN_coverage))[0]  # np.where[0] is a list
        # build dict to record coverage and NN array
        primer_update_list, coverage_update_list, NN_array_update_list, NN_coverage_update = [], [], [], []
        for i in refine_index:
            optimal_NN_coverage_tmp = optimal_NN_coverage.copy()
            NN_array_tmp = NN_array.copy()
            optimal_list = optimal_primer_list.copy()
            # initiation score
            # initiation coverage
            coverage_renew = optimal_coverage_init
            if i == 0:
                # two position need refine
                # position 0 and 1
                # decide which position to choose
                row = optimal_NN_index[i][0]
                column = optimal_NN_index[i][1]
                if len(np.where(NN_array_tmp[0, :, column] > 0)[0]) > 1:
                    init_score = score_table[optimal_list[i]]
                    refine_column = NN_array_tmp[i, :, column]
                    refine_row_arg_sort = np.argsort(refine_column, axis=0)[::-1]
                    new_primer = optimal_list
                    # print(row, refine_column)
                    for idx in refine_row_arg_sort:
                        # init refine,  We must ensure that there are no double counting.
                        # position 0.
                        if idx != row:
                            init_score += score_table[bases[idx]]
                            new_primer[i] = bases[idx]
                            # Calculate coverage after refine
                            for new_primer_update in self.degenerate_seq("".join(new_primer)):
                                if new_primer_update in cover.keys():
                                    coverage_renew += cover["".join(new_primer_update)]
                            new_primer[i] = trans_score_table[round(init_score, 2)]
                            # reset NN_array. row names will update after reset.
                            NN_array_tmp[i, row, :] += NN_array_tmp[i, idx, :]
                            NN_array_tmp[i, idx, :] -= NN_array_tmp[i, idx, :]
                            optimal_NN_coverage_tmp[i] = NN_array_tmp[i, row, column]
                            break
                        # primer update
                    optimal_list_update = optimal_list
                    optimal_list_update[i] = trans_score_table[round(init_score, 2)]
                # position 1
                elif len(np.where(NN_array_tmp[0, row, :] > 0)[0]) > 1:
                    init_score = score_table[optimal_list[i + 1]]
                    next_row = optimal_NN_index[i + 1][0]
                    next_column = optimal_NN_index[i + 1][1]
                    # concat row of layer i and column of layer i+1
                    refine_row = NN_array_tmp[i, row, :].reshape(1, -1)
                    refine_column = NN_array_tmp[i + 1, :, next_column].reshape(1, -1)
                    refine = np.concatenate([refine_row, refine_column], 0)
                    refine_min = np.min(refine, axis=0)
                    refine_row_arg_sort = np.argsort(refine_min, axis=0)[::-1]
                    # Return the minimum of an array or maximum along an axis. axis=0: column , axis=1: row
                    new_primer = optimal_list
                    if len(np.where(refine_min > 0)[0]) > 1:
                        for idx in refine_row_arg_sort:
                            # We must ensure that there are no double counting.
                            # position 1.
                            if idx != column:
                                init_score += score_table[bases[idx]]
                                # Calculate coverage after refine
                                new_primer[i + 1] = bases[idx]
                                for new_primer_update in self.degenerate_seq("".join(new_primer)):
                                    if new_primer_update in cover.keys():
                                        coverage_renew += cover["".join(new_primer_update)]
                                new_primer[i + 1] = trans_score_table[round(init_score, 2)]
                                # reset NN_array. column + (column idx) of layer i and row + (row idx) of layer i+1.
                                NN_array_tmp[i, :, column] += NN_array_tmp[i, :, idx]
                                NN_array_tmp[i, :, idx] -= NN_array_tmp[i, :, idx]
                                NN_array_tmp[i + 1, next_row, :] += NN_array_tmp[i + 1, idx, :]
                                NN_array_tmp[i + 1, idx, :] -= NN_array_tmp[i + 1, idx, :]
                                optimal_NN_coverage_tmp[i] = NN_array_tmp[i, row, column]
                                optimal_NN_coverage_tmp[i + 1] = NN_array_tmp[i + 1, next_row, next_column]
                                break
                    # primer update
                    optimal_list_update = optimal_list
                    optimal_list_update[i + 1] = trans_score_table[round(init_score, 2)]
                else:
                    optimal_list_update = optimal_list
            elif i == len(optimal_NN_index) - 1:
                init_score = score_table[optimal_list[i + 1]]
                row = optimal_NN_index[i][0]
                column = optimal_NN_index[i][1]
                refine_row = NN_array_tmp[i, row, :]
                refine_row_arg_sort = np.argsort(refine_row, axis=0)[::-1]
                # If number of refine_row > 1, then the current position need to refine.
                if len(np.where(refine_row > 0)[0]) > 1:
                    new_primer = optimal_list
                    for idx in refine_row_arg_sort:
                        # We must ensure that there are no double counting.
                        # position -1.
                        if idx != column:
                            init_score += score_table[bases[idx]]
                            # Calculate coverage after refine
                            new_primer[i + 1] = bases[idx]
                            for new_primer_update in self.degenerate_seq("".join(new_primer)):
                                if new_primer_update in cover.keys():
                                    coverage_renew += cover["".join(new_primer_update)]
                            new_primer[i + 1] = trans_score_table[round(init_score, 2)]
                            # reset NN_array. column names will update after reset.
                            NN_array_tmp[i, :, column] += NN_array_tmp[i, :, idx]
                            NN_array_tmp[i, :, idx] -= NN_array_tmp[i, :, idx]
                            optimal_NN_coverage_tmp[i] = NN_array_tmp[i, row, column]
                            break
                # primer update
                optimal_list_update = optimal_list
                optimal_list_update[i + 1] = trans_score_table[round(init_score, 2)]
            else:
                init_score = score_table[optimal_list[i + 1]]
                row = optimal_NN_index[i][0]
                column = optimal_NN_index[i][1]
                next_row = optimal_NN_index[i + 1][0]
                next_column = optimal_NN_index[i + 1][1]
                # concat row of layer i and column of layer i+1
                refine_row = NN_array_tmp[i, row, :].reshape(1, -1)
                refine_column = NN_array_tmp[i + 1, :, next_column].reshape(1, -1)
                refine = np.concatenate([refine_row, refine_column], 0)
                refine_min = np.min(refine, axis=0)
                # Return the minimum of an array or maximum along an axis. axis=0: column , axis=1: row
                refine_min_arg_sort = np.argsort(refine_min, axis=0)[::-1]
                if len(np.where(refine_min > 0)[0]) > 1:
                    new_primer = optimal_list
                    # for idx in np.where(refine_min_sort > 0)[0]:
                    for idx in refine_min_arg_sort:
                        # We must ensure that there are no double counting.
                        # position i+1.
                        if idx != column:
                            # or if idx != next_row
                            # init trans score update
                            init_score += score_table[bases[idx]]
                            # Calculate coverage after refine
                            new_primer[i + 1] = bases[idx]
                            for new_primer_update in self.degenerate_seq("".join(new_primer)):
                                if new_primer_update in cover.keys():
                                    coverage_renew += cover["".join(new_primer_update)]
                            new_primer[i + 1] = trans_score_table[round(init_score, 2)]
                            # reset NN_array. column + (column idx) of layer i and row + (row idx) of layer i+1.
                            NN_array_tmp[i, :, column] += NN_array_tmp[i, :, idx]
                            NN_array_tmp[i, :, idx] -= NN_array_tmp[i, :, idx]
                            NN_array_tmp[i + 1, next_row, :] += NN_array_tmp[i + 1, idx, :]
                            NN_array_tmp[i + 1, idx, :] -= NN_array_tmp[i + 1, idx, :]
                            optimal_NN_coverage_tmp[i] = NN_array_tmp[i, row, column]
                            optimal_NN_coverage_tmp[i + 1] = NN_array_tmp[i + 1, next_row, next_column]

                            break
                # primer update
                optimal_list_update = optimal_list
                optimal_list_update[i + 1] = trans_score_table[round(init_score, 2)]
            # primer_update = "".join(primer_list_update)
            primer_update_list.append(optimal_list_update)
            NN_coverage_update.append(optimal_NN_coverage_tmp)
            # current_primers_set = set(self.degenerate_seq(primer_update))
            # coverage of update primers
            coverage_update_list.append(coverage_renew)
            # new NN_array
            NN_array_update_list.append(NN_array_tmp)
        optimal_idx = coverage_update_list.index(max(coverage_update_list))
        degeneracy_update = score_trans(primer_update_list[optimal_idx])
        degenerate_number_update = sum([math.floor(score_table[x]) > 1 for x in primer_update_list[optimal_idx]])
        # optimal_primer_update, coverage_update,
        # NN_coverage_update, NN array_update,
        # degeneracy_update, degenerate_update
        return primer_update_list[optimal_idx], coverage_update_list[optimal_idx], \
               NN_coverage_update[optimal_idx], NN_array_update_list[optimal_idx], \
               degeneracy_update, degenerate_number_update

    def get_Y(self):
        Y_strict, Y_strict_R = [], []
        for y in self.position.split(","):
            y_index = int(y.strip())
            if y_index > 0:
                Y_strict.append(y_index)
                Y_strict_R.append(self.primer_length - y_index)
            else:
                Y_strict.append(self.primer_length + y_index + 1)
                Y_strict_R.append(-y_index + 1)
        return set(Y_strict), set(Y_strict_R)

    def mis_primer_check(self, all_primers, optimal_primer, cover, non_gap_seq_id):
        # uncoverage sequence in cover dict
        optimal_primer_set = set(self.degenerate_seq(optimal_primer))
        uncover_primer_set = all_primers - optimal_primer_set
        F_non_cover, R_non_cover = {}, {}
        F_mis_cover, R_mis_cover = 0, 0
        for uncover_primer in uncover_primer_set:
            Y_dist = Y_distance(optimal_primer, uncover_primer)
            # print(uncover_primer)
            # print(Y_dist)
            # print(set(Y_dist))
            if len(Y_dist) > self.variation:
                # record sequence and acc_ID which will never mis-coverage. too many mismatch!
                F_non_cover[uncover_primer] = non_gap_seq_id[uncover_primer]
                R_non_cover[uncover_primer] = non_gap_seq_id[uncover_primer]
            # if len(Y_dist) <= self.variation:
            else:
                if len(set(Y_dist).intersection(self.Y_strict)) > 0:
                    F_non_cover[uncover_primer] = non_gap_seq_id[uncover_primer]
                else:
                    F_mis_cover += cover[uncover_primer]
                if len(set(Y_dist).intersection(self.Y_strict_R)) > 0:
                    R_non_cover[uncover_primer] = non_gap_seq_id[uncover_primer]
                else:
                    R_mis_cover += cover[uncover_primer]
        # print(optimal_primer)
        # print(F_mis_cover)
        return F_mis_cover, F_non_cover, R_mis_cover, R_non_cover

    ################# get_primers #####################
    def run(self):
        p = ProcessPoolExecutor(self.nproc)  #
        sequence_dict = self.seq_dict
        start_primer = self.start_position
        stop_primer = self.stop_position
        # primer_info = Manager().list()
        # non_cov_primer_out = Manager().list()
        # for position in range(1245,  stop_primer - self.primer_length):
        for position in range(start_primer, stop_primer - self.primer_length):
            # print(position)
            p.submit(self.get_primers(sequence_dict, position))  # , primer_info, non_cov_primer_out
            # This will submit all tasks to one place without blocking, and then each
            # thread in the thread pool will fetch tasks.
        n = 0
        candidate_list, non_cov_primer_out, gap_seq_id_out = [], [], []
        with open(self.outfile, "w") as fo:
            headers = ["Position", "Entropy of cover (bit)", "Entropy of total (bit)", "Optimal_primer",
                       "primer_degenerate_number",
                       "nonsense_primer_number", "Optimal_coverage", "Mis-F-coverage", "Mis-R-coverage", "Tm",
                       "Information"]
            fo.write("\t".join(map(str, headers)) + "\n")
            while n < stop_primer - start_primer - self.primer_length:
                res = self.resQ.get()
                # The get method can read and delete an element from the queue. Similarly, the get method has two
                # optional parameters: blocked and timeout. If blocked is true (the default value) and timeout is
                # positive, no element is retrieved during the waiting time, and a Queue is thrown Empty exception.
                # If blocked is false, there are two cases. If a value of Queue is available, return the value
                # immediately. Otherwise, if the queue is empty, throw a Queue.Empty exception immediately.
                if res is None:
                    n += 1
                    continue
                candidate_list.append(res[0])
                non_cov_primer_out.append(res[1])
                gap_seq_id_out.append(res[2])
                n += 1
            sorted_candidate_dict = dict(sorted(dict(candidate_list).items(), key=lambda x: x[0], reverse=False))
            for position in sorted_candidate_dict.keys():
                fo.write(str(position) + "\t" + "\t".join(map(str, sorted_candidate_dict[position])) + "\n")
            fo.close()
            with open(self.outfile + '.non_coverage_seq_id_json', "w") as fj:
                json.dump(dict(non_cov_primer_out), fj, indent=4)
            fj.close()
            with open(self.outfile + '.gap_seq_id_json', "w") as fg:
                json.dump(dict(gap_seq_id_out), fg, indent=4)
            fg.close()
            # get results before shutdown. Synchronous call mode: call, wait for the return value, decouple,
            # but slow.
        p.shutdown()



class Primers_filter(object):
    def __init__(self, ref_file, primer_file, adaptor, rep_seq_number=500, distance=4, outfile="", diff_Tm=5,
                 size="300,700", position=9, GC="0.4,0.6", nproc=10, fraction=0.6):
        self.nproc = nproc
        self.primer_file = primer_file
        self.adaptor = adaptor
        self.size = size
        self.outfile = os.path.abspath(outfile)
        self.distance = distance
        self.Input_file = ref_file
        self.fraction = fraction
        self.GC = GC
        self.diff_Tm = diff_Tm
        self.rep_seq_number = rep_seq_number
        self.number = self.get_number()
        self.position = position
        self.primers, self.gap_id, self.non_cover_id = self.parse_primers()
        self.resQ = Manager().Queue()
        self.pre_filter_primers = self.pre_filter()

    def parse_primers(self):
        primer_dict = {}
        with open(self.primer_file) as f:
            for i in f:
                if i.startswith("Pos"):
                    pass
                else:
                    i = i.strip().split("\t")
                    position = int(i[0])
                    primer_seq = i[3]
                    F_coverage = int(i[7])
                    R_coverage = int(i[8])
                    fraction = round(int(i[6]) / self.number, 2)
                    Tm = round(float(i[9]), 2)
                    primer_dict[position] = [primer_seq, fraction, F_coverage, R_coverage, Tm]
        # print(primer_dict)
        with open(self.primer_file + ".gap_seq_id_json") as g:
            gap_dict = json.load(g)
            g.close()
        with open(self.primer_file + ".non_coverage_seq_id_json") as n:
            non_cover_dict = json.load(n)
            g.close()
        return primer_dict, gap_dict, non_cover_dict

    ################# get_number #####################
    def get_number(self):
        from itertools import (takewhile, repeat)
        buffer = 1024 * 1024
        with open(self.Input_file, encoding="utf-8") as f:
            buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
            seq_number = int(sum(buf.count("\n") for buf in buf_gen) / 2)
            if seq_number > self.rep_seq_number != 0:
                return self.rep_seq_number
            else:
                return seq_number

    ################# degenerate_seq #####################
    @staticmethod
    def degenerate_seq(sequence):
        seq = []
        cs = ""
        for s in sequence:
            if s not in degenerate_base:
                cs += s
            else:
                seq.append([cs + i for i in degenerate_base[s]])
                cs = ""
        if cs:
            seq.append([cs])
        return ("".join(i) for i in product(*seq))

    ################# Hairpin #####################
    def hairpin_check(self, primer):
        n = 0
        distance = self.distance
        while n <= len(primer) - 5 - 5 - distance:
            kmer = self.degenerate_seq(primer[n:n + 5])
            left = self.degenerate_seq(primer[n + 5 + distance:])
            for k in kmer:
                for l in left:
                    if re.search(RC(k), l):
                        return True
            n += 1
        return False

    ################# current_end #####################
    def current_end(self, primer, adaptor="", num=5, length=14):
        primer_extend = adaptor + primer
        end_seq = []
        for i in range(num, (num + length)):
            s = primer_extend[-i:]
            if s:
                end_seq.extend(self.degenerate_seq(s))
        return end_seq

    ################# Free energy #####################
    def deltaG(self, sequence):
        Delta_G_list = []
        Na = 50
        for seq in self.degenerate_seq(sequence):
            Delta_G = 0
            for n in range(len(seq) - 1):
                i, j = base2bit[seq[n + 1]], base2bit[seq[n]]
                Delta_G += freedom_of_H_37_table[i][j] * H_bonds_number[i][j] + penalty_of_H_37_table[i][j]
            term5 = sequence[-2:]
            if term5 == "TA":
                Delta_G += adjust_initiation[seq[0]] + adjust_terminal_TA
            else:
                Delta_G += adjust_initiation[seq[0]]
            Delta_G -= (0.175 * math.log(Na / 1000, math.e) + 0.20) * len(seq)
            if symmetry(seq):
                Delta_G += symmetry_correction
            Delta_G_list.append(Delta_G)
        return round(max(Delta_G_list), 2)

    ################# Dimer #####################
    def dimer_check(self, primer_F, primer_R):
        current_end_set = set(self.current_end(primer_F)).union(set(self.current_end(primer_R)))
        primer_pairs = [primer_F, primer_R]
        for pp in primer_pairs:
            for end in current_end_set:
                for p in self.degenerate_seq(pp):
                    idx = p.find(RC(end))
                    if idx >= 0:
                        end_length = len(end)
                        end_GC = end.count("G") + end.count("C")
                        end_d1 = 0
                        end_d2 = len(p) - len(end) - idx
                        Loss = Penalty_points(
                            end_length, end_GC, end_d1, end_d2)
                        delta_G = self.deltaG(end)
                        # threshold = 3 or 3.6 or 3.96
                        if Loss > 3.6 or (delta_G < -5 and (end_d1 == end_d2)):
                            return True
        return False

    ################# position of degenerate base #####################
    def dege_filter_in_term_N_bp(self, sequence):
        term = self.position
        if term == 0:
            term_base = ["A"]
        else:
            term_base = sequence[-term:]
        score = score_trans(term_base)
        if score > 1:
            return True
        else:
            return False

    ################# GC content #####################
    def GC_fraction(self, sequence):
        sequence_expand = self.degenerate_seq(sequence)
        GC_list = []
        for seq in sequence_expand:
            GC_list.append(round((list(seq).count("G") + list(seq).count("C")) / len(list(seq)), 3))
        GC_average = mean(GC_list)
        return GC_average

    ################# di_nucleotide #####################
    def di_nucleotide(self, primer):
        primers = self.degenerate_seq(primer)
        for m in primers:
            for n in di_nucleotides:
                if re.search(n, m):
                    return True
        return False

    ################# di_nucleotide #####################
    def GC_clamp(self, primer, num=4, length=13):
        for i in range(num, (num + length)):
            s = primer[-i:]
            gc_fraction = self.GC_fraction(s)
            if gc_fraction > 0.6:
                return True
        return False

    def pre_filter(self):
        limits = self.GC.split(",")
        min = float(limits[0])
        max = float(limits[1])
        # min_cov = self.fraction
        candidate_primers_position = []
        primer_info = self.primers
        for primer_position in primer_info.keys():
            primer = primer_info[primer_position][0]
            # coverage = primer_info[primer_position][1]
            if self.hairpin_check(primer):
                pass
            elif self.GC_fraction(primer) > max or self.GC_fraction(primer) < min:
                pass
            elif self.di_nucleotide(primer):
                pass
            else:
                candidate_primers_position.append(primer_position)
        return sorted(candidate_primers_position)

    @staticmethod
    def closest(my_list, my_number1, my_number2):
        index_left = bisect_left(my_list, my_number1)
        # find the first element index in my_list which greater than my_number.
        if my_number2 > my_list[-1]:
            index_right = len(my_list) - 1  # This is index.
        else:
            index_right = bisect_left(my_list, my_number2) - 1
        return index_left, index_right

    def primer_pairs(self, start, adaptor, min_len, max_len, candidate_position, primer_pairs, threshold):
        primerF_extend = adaptor[0] + self.primers[candidate_position[start]][0]
        if self.hairpin_check(primerF_extend):
            # print("hairpin!")
            pass
        elif self.dege_filter_in_term_N_bp(self.primers[candidate_position[start]][0]):
            # print("term N!")
            pass
        elif self.GC_clamp(self.primers[candidate_position[start]][0]):
            # print("GC_clamp!")
            pass
        else:
            start_index, stop_index = self.closest(candidate_position, candidate_position[start] + min_len,
                                                   candidate_position[start] + max_len)
            if start_index > stop_index:
                pass
            else:
                for stop in range(start_index, stop_index + 1):
                    primerR_extend = adaptor[1] + RC(self.primers[candidate_position[stop]][0])
                    if self.hairpin_check(primerR_extend):
                        # print("self hairpin!")
                        pass
                    elif self.dege_filter_in_term_N_bp(
                            RC(self.primers[candidate_position[stop]][0])):
                        pass
                    elif self.GC_clamp(RC(self.primers[candidate_position[stop]][0])):
                        pass
                    else:
                        distance = int(candidate_position[stop]) - int(candidate_position[start]) + 1
                        if distance > int(max_len):
                            print("Error! PCR product greater than max length !")
                            break
                        elif int(min_len) <= distance <= int(max_len):
                            # print(self.primers[candidate_position[start]][0],
                            #                     RC(self.primers[candidate_position[stop]][0]))
                            if self.dimer_check(self.primers[candidate_position[start]][0],
                                                RC(self.primers[candidate_position[stop]][0])):
                                print("Dimer detection between Primer-F and Primer-R!")
                                pass
                            else:
                                # primer_pairs.append((candidate_position[start], candidate_position[stop]))
                                difference_Tm = self.primers[candidate_position[start]][4] - \
                                                self.primers[candidate_position[stop]][4]
                                # difference of Tm between primer-F and primer-R  should less than threshold
                                if abs(difference_Tm) > self.diff_Tm:
                                    pass
                                else:
                                    start_pos = str(candidate_position[start])
                                    # print(start_pos)
                                    stop_pos = str(candidate_position[stop])
                                    # print(stop_pos)
                                    un_cover_list = []
                                    for o in list(dict(self.gap_id[start_pos]).values()):
                                        un_cover_list.extend(set(o))
                                    for p in list(dict(self.non_cover_id[start_pos][0]).values()):
                                        un_cover_list.extend(set(p))
                                    for m in list(dict(self.gap_id[stop_pos]).values()):
                                        un_cover_list.extend(set(m))
                                    for n in list(dict(self.non_cover_id[stop_pos][1]).values()):
                                        un_cover_list.extend(set(n))
                                    all_non_cover_number = len(set(un_cover_list))
                                    if all_non_cover_number / self.number > threshold:
                                        pass
                                    else:
                                        all_coverage = self.number - all_non_cover_number
                                        cover_percentage = round(all_coverage / self.number, 4)
                                        average_Tm = str(round(mean([self.primers[candidate_position[start]][4],
                                                                     self.primers[candidate_position[stop]][4]]), 2))
                                        line = (self.primers[candidate_position[start]][0],
                                                RC(self.primers[candidate_position[stop]][0]),
                                                str(distance) + ":" + average_Tm + ":" + str(cover_percentage),
                                                all_coverage,
                                                str(candidate_position[start]) + ":" + str(candidate_position[stop]))
                                        primer_pairs.append(line)

    #                                 self.resQ.put(line)
    # self.resQ.put(None)

    #  The queue in multiprocessing cannot be used for pool process pool, but there is a manager in multiprocessing.
    #  Inter process communication in the pool uses the queue in the manager. Manager().Queue().
    #  Queue. qsize(): returns the number of messages contained in the current queue;
    #  Queue. Empty(): returns True if the queue is empty, otherwise False;
    #  Queue. full(): returns True if the queue is full, otherwise False;
    #  Queue. get(): get a message in the queue, and then remove it from the queue,
    #                which can pass the parameter timeout.
    #  Queue.get_Nowait(): equivalent to Queue. get (False).
    #                If the value cannot be obtained, an exception will be triggered: Empty;
    #  Queue. put(): add a value to the data sequence to transfer the parameter timeout duration.
    #  Queue.put_Nowait(): equivalent to Queue. get (False). When the queue is full, an error is reported: Full.

    def run(self):
        p = ProcessPoolExecutor(self.nproc)  #
        size_list = self.size.split(",")
        min_len = int(size_list[0])
        max_len = int(size_list[1])
        candidate_position = self.pre_filter_primers
        adaptor = self.adaptor.split(",")
        primer_pairs = Manager().list()
        # print(candidate_position)
        coverage_threshold = 1 - self.fraction
        if int(candidate_position[-1]) - int(candidate_position[0]) < min_len:
            print("Max PCR product legnth < min len!")
            ID = str(self.outfile)
            with open(self.outfile, "w") as fo:
                # headers = ["Primer_F_seq", "Primer_R_seq", "Product length:Tm:coverage_percentage",
                # "Target number", "Primer_start_end"]
                # fo.write(ID + "\t" + "\t".join(headers) + "\t")
                fo.write(ID + "\n")
        else:
            for start in range(len(candidate_position)):
                print(start)
                p.submit(self.primer_pairs(start, adaptor, min_len, max_len, candidate_position, primer_pairs,
                                           coverage_threshold))
                # This will submit all tasks to one place without blocking, and then each
                # thread in the thread pool will fetch tasks.
            p.shutdown()
            # After I run the main, I don't care whether the sub thread is alive or dead. With this parameter,
            # after all the sub threads are executed, the main function is executed get results after shutdown.
            # Asynchronous call mode: only call, unequal return values, coupling may exist, but the speed is fast.
            if len(primer_pairs) < 10:
                new_p = ProcessPoolExecutor(self.nproc)
                coverage_threshold += 0.1
                for start in range(len(candidate_position)):
                    new_p.submit(self.primer_pairs(start, adaptor, min_len, max_len, candidate_position, primer_pairs,
                                                   coverage_threshold))
                    # This will submit all tasks to one place without blocking, and then each
                    # thread in the thread pool will fetch tasks.
                new_p.shutdown()
            ID = str(self.outfile)
            primer_ID = str(self.outfile).split("/")[-1].rstrip(".txt")
            with open(self.outfile, "w") as fo:
                # headers = ["Primer_F_seq", "Primer_R_seq", "Product length:Tm:coverage_percentage",
                # "Target number", "Primer_start_end"]
                # fo.write(ID + "\t" + "\t".join(headers) + "\t")
                with open(self.outfile + ".fa", "w") as fa:
                    fo.write(ID + "\t")
                    primer_pairs_sort = sorted(primer_pairs, key=lambda k: k[3], reverse=True)
                    for i in primer_pairs_sort:
                        fo.write("\t".join(map(str, i)) + "\t")
                        start_stop = i[4].split(":")
                        fa.write(
                            ">" + primer_ID + "_" + start_stop[0] + "F\n" + i[0] + "\n>" + primer_ID + "_" + start_stop[
                                1]
                            + "R\n" + i[1] + "\n")
                    # get results before shutdown. Synchronous call mode: call, wait for the return value, decouple,
                    # but slow.
                    fo.write("\n")
                    fo.close()
                    fa.close()


class Product_perfect(object):
    def __init__(self, primer_file="", output_file="", ref_file="", file_format="fa", coverage="", nproc=10):
        self.nproc = nproc
        self.primers_file = primer_file
        self.ref_file = ref_file
        self.output_file = Path(output_file)
        self.file_format = file_format
        self.primers = self.parse_primers()
        self.coverage = coverage
        self.resQ = Manager().Queue()

    def md_out_File(self):
        if self.output_file.exists():
            pass
        else:
            os.system("mkdir -p {}".format(self.output_file))

    def parse_primers(self):
        res = {}
        if self.file_format == "seq":
            primers = self.primers_file.split(",")
            res["PCR_info"] = [primers[0], primers[1]]
        else:
            with open(self.primers_file, "r") as f:
                if self.file_format == "xls":
                    for i in f:
                        if i.startswith("#"):
                            pass
                        else:
                            i = i.strip().split("\t")
                            cluster_id = i[0].split("/")[-1].split(".")[0]
                            primer_F = i[2]
                            primer_R = i[3]
                            start = i[6].split(":")[0]
                            stop = i[6].split(":")[1]
                            key = cluster_id + "_" + str(start) + "_F_" + cluster_id + "_" + str(stop)
                            res[key] = [primer_F, primer_R]
                elif self.file_format == "fa":
                    primer_info = pd.read_table(f, header=None)
                    for idx, row in primer_info.iterrows():
                        if idx % 4 == 0:
                            primer_F_info = row[0].lstrip(">")
                        elif idx % 4 == 1:
                            primer_F = row[0]
                        elif idx % 4 == 2:
                            key = primer_F_info + "_" + row[0].lstrip(">")
                        elif idx % 4 == 3:
                            primer_R = row[0]
                            res[key] = [primer_F, primer_R]
        return res

    @staticmethod
    def degenerate_seq(primer):
        seq = []
        cs = ""
        for s in primer:
            if s not in degenerate_base:
                cs += s
            else:
                seq.append([cs + i for i in degenerate_base[s]])
                cs = ""
        if cs:
            seq.append([cs])
        # return ("".join(i) for i in product(*seq)) # This is a generator, just once when iteration
        # d = [x for x in range(12)]
        # g = (x for i in range(12))
        # The result of list derivation returns a list, and the tuple derivation returns a generator
        return ["".join(i) for i in product(*seq)]

    def get_PCR_PRODUCT(self, primerinfo, F, R, ref):
        Fseq = self.degenerate_seq(F)
        Rseq = self.degenerate_seq(R)
        product_dict = {}
        Non_targets_dict = {}
        with open(ref, "r") as r:
            for i in r:
                if i.startswith(">"):
                    key = i.strip()
                else:
                    value = ''
                    for sequence in Fseq:
                        if re.search(sequence, i):
                            line = i.split(sequence)
                            Product = sequence + line[1]
                            for sequence2 in Rseq:
                                if re.search(RC(sequence2), Product):
                                    Product = Product.split(RC(sequence2))
                                    value = Product[0].strip() + RC(sequence2)
                                    break
                            if value:
                                break
                    if value:
                        product_dict[key] = value
                    else:
                        Non_targets_dict[key] = i.strip()
        self.resQ.put([primerinfo, product_dict, Non_targets_dict, F, R])
        self.resQ.put(None)

    def run(self):
        self.md_out_File()
        proc = ProcessPoolExecutor(self.nproc)
        for primer in self.primers.keys():
            proc.submit(self.get_PCR_PRODUCT, primer, self.primers[primer][0], self.primers[primer][1], self.ref_file)
            #  This will submit all tasks to one place without blocking, and then each
            #  thread in the thread pool will fetch tasks
        n = 0
        Product_seq_id = set()
        non_Product_seq_id = set()
        while n < len(self.primers):
            res = self.resQ.get()
            if res is None:
                n += 1
                continue
            PCR_product = Path(self.output_file).joinpath(res[0]).with_suffix(".PCR.product.fa")
            PCR_non_product = Path(self.output_file).joinpath(res[0]).with_suffix(
                ".non_PCR.product.fa")
            with open(self.coverage, "a+") as c:
                c.write(
                    "Number of Product/non_Product, primer-F and primer-R: {}"
                    "\t{}\t{}\t{}\t{}\n".format(res[0], len(res[1].keys()), len(res[2].keys()), res[3], res[4]))
                with open(PCR_product, "w") as p:
                    for result in res[1].keys():
                        Product_seq_id.add(result)
                        p.write(result + "\n" + res[1][result] + "\n")
                with open(PCR_non_product, "w") as np:
                    for result2 in res[2].keys():
                        non_Product_seq_id.add(result2)
                        np.write(result2 + "\n" + res[2][result2] + "\n")
        proc.shutdown()
        # After I run the main, I don't care whether the sub thread is alive or dead. With this parameter, after all
        # the sub threads are executed, the main function is executed.
        # get results after shutdown. Asynchronous call mode: only call, unequal return values, coupling may exist,
        # but the speed is fast.
        buffer = 1024 * 1024
        with open(self.ref_file, encoding="utf-8") as f:
            buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
            seq_number = int(sum(buf.count("\n") for buf in buf_gen) / 2)
        with open(self.coverage, "a+") as c:
            c.write(
                "Total number of sequences:\t{}\n"
                "Coveraged number of sequence:\t{}\n"
                "Rate of coverage:\t> {}\n".format(seq_number, len(Product_seq_id),
                                                   round(float(len(Product_seq_id)) / seq_number, 2)))
        c.close()


class Errors(object):
    def __init__(self, primer_file, term_length=int, reference_file=str, mismatch_num=1, term_threshold=4,
                 bowtie="",
                 PCR_product_size="150,2000", outfile="", nproc=10, targets="None"):
        #  If an attribute in a Python class does not want to be accessed externally,
        #  we can start with a double underscore (__) when naming the attribute,
        #  Then the attribute cannot be accessed with the original variable name, making it private.
        #  If an attribute is marked with "__xxxx_" Is defined, then it can be accessed externally.
        self.bowtie = bowtie
        self.term_threshold = term_threshold
        self.nproc = nproc
        self.term_len = term_length
        self.primer_file = primer_file
        self.reference_file = reference_file
        self.outfile = outfile
        self.PCR_size = PCR_product_size
        self.resQ = Manager().Queue()
        self.mismatch_num = mismatch_num
        self.targets = targets

    @staticmethod
    def degenerate_seq(primer):
        seq = []
        cs = ""
        for s in primer:
            if s not in degenerate_base:
                cs += s
            else:
                seq.append([cs + i for i in degenerate_base[s]])
                cs = ""
        if cs:
            seq.append([cs])
        return ["".join(i) for i in product(*seq)]

    def get_term(self):
        Output = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".term.fa")
        Input = self.primer_file
        l = self.term_len
        term_list = defaultdict(list)
        seq_ID = defaultdict(list)
        with open(Input, "r") as f:
            for i in f:
                if i.startswith(">"):
                    value = i.strip().lstrip(">")
                else:
                    if l == 0:
                        key = i.strip()
                        term_list[key].append(value)
                    else:
                        key = i.strip()[-l:]
                        term_list[key].append(value)

        for k in term_list.keys():
            sequence = k
            term_set = set(term_list[k])
            Id = "_".join(list(term_set))
            expand_seq = self.degenerate_seq(sequence)
            if len(expand_seq) > 1:
                for j in range(len(expand_seq)):
                    ID = Id + "_" + str(j)
                    seq_ID[expand_seq[j]].append(ID)
            else:
                ID = Id + "_0"
                seq_ID[sequence].append(ID)
        with open(Output, "w") as fo:
            for seq in seq_ID.keys():
                # print(">" + '_'.join(seq_ID[seq]))
                # print(seq)
                fo.write(">" + '_'.join(seq_ID[seq]) + "\n" + seq + "\n")
        return seq_ID

    def build_dict(self, Input):
        Input_dict = defaultdict(list)
        threshold = self.term_threshold
        with open(Input, "r") as f:
            position_pattern_1 = re.compile('MD:Z:(\w+)')
            position_pattern = re.compile("[A-Z]?(\d+)")
            for i in f:
                i = i.strip().split("\t")
                primer = re.split("_\d+$", i[0])[0]
                gene = i[2]
                primer_match_start = int(i[3]) - 1
                candidate_MD = nan_removing(i[11:])
                string = str('\t'.join(candidate_MD))
                if re.search("MD", string):
                    position_1 = position_pattern_1.search(string).group(1)
                    position = position_pattern.search(position_1[-2:]).group(1)
                    if int(position) < threshold:
                        pass
                    else:
                        Input_dict[gene].append([primer_match_start, primer])
        return Input_dict

    def bowtie_map(self):
        fa = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".term.fa")
        ref_index = self.reference_file
        out = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".sam")
        for_out = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".for.sam")
        rev_out = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".rev.sam")
        nproc = self.nproc
        if for_out.exists() and rev_out.exists():
            pass
        else:
            if re.search('bowtie2', self.bowtie):
                os.system("{} -p {} -N {} -L 8 -a -x {} -f -U {} -S {}".format(self.bowtie, self.nproc,
                                                                               self.mismatch_num, ref_index, fa,
                                                                               out))
            elif re.search('bowtie', self.bowtie):
                os.system(
                    "{} -p {} -f -n {} -l 8 -a --best --strata {} {} -S {}".format(self.bowtie, self.nproc,
                                                                                   self.mismatch_num, ref_index, fa,
                                                                                   out))
            else:
                print("mapping software must be bowtie or bowtie2 !")
                sys.exit(1)
            os.system("samtools view -@ {} -F 16 {} > {}".format(nproc, out, for_out))
            os.system("samtools view -@ {} -f 16 {} > {}".format(nproc, out, rev_out))

    def build_dict_run(self):
        sam_for_file = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".for.sam")
        sam_rev_file = Path(self.primer_file).parent.joinpath(Path(self.primer_file).stem).with_suffix(".rev.sam")
        pool = multiprocessing.Pool()
        # pool.apply_async(build_dict, kwds={sam_for_file, sam_rev_file})
        forward_dict, reverse_dict = pool.map_async(self.build_dict, (sam_for_file, sam_rev_file)).get()
        pool.close()
        pool.join()
        print("Number of genes with candidate primers: forward ==> {}; reverse ==> {}.".format(len(forward_dict),
                                                                                               len(reverse_dict)))
        target_gene = list(set(forward_dict.keys()).intersection(reverse_dict.keys()))
        print("Number of genes with candidate primer pairs: {}.".format(
            len(set(forward_dict.keys()).intersection(reverse_dict.keys()))))
        return target_gene, forward_dict, reverse_dict

    def PCR_product(self, gene, F_dict, R_dict):
        product_len = self.PCR_size.split(",")
        primer_F = dict(F_dict[gene])
        position_start = sorted(primer_F.keys())
        primer_R = dict(R_dict[gene])
        position_stop = sorted(primer_R.keys())
        if int(position_stop[0]) - int(position_start[-1]) > int(product_len[1]):
            pass
        elif int(position_stop[-1]) - int(position_start[0]) < int(product_len[0]):
            pass
        else:
            for start in range(len(position_start)):
                stop_index_start, stop_index_stop = closest(position_stop,
                                                            position_start[start] + int(product_len[0]),
                                                            position_start[start] + int(product_len[1]))
                if stop_index_start > stop_index_stop:  # caution: all(var) > stop_index_start in bisect_left,
                    # you need to stop immediately when stop_index_start > Product length
                    break
                else:
                    for stop in range(stop_index_start, stop_index_stop + 1):
                        distance = int(position_stop[stop]) - int(position_start[start]) + 1
                        if distance > int(product_len[1]):
                            break
                        elif int(product_len[0]) < distance < int(product_len[1]):
                            line = (gene, int(position_start[start]), int(position_stop[stop]),
                                    primer_F[position_start[start]], primer_R[position_stop[stop]], distance)
                            # off_target = {"Chrom (or Genes)": gene,
                            #               "Start": int(position_start[start]),
                            #               "Stop": int(position_stop[stop]),
                            #               "Primer_F": primer_F[position_start[start]],
                            #               "Primer_R": primer_R[position_stop[stop]],
                            #               "Product length": distance}
                            # out.append(off_target)
                            self.resQ.put(line)
                            # In multiple processes, each process has its own variable copy, so a variable in the
                            # main process is transferred to other processes for modification, and the result is
                            # still stored in that process. In fact, this variable in the main process is equivalent
                            # to not being modified. In order to synchronize the changes of other processes to the
                            # main process, you need to create variables that can be shared among multiple processes.
        self.resQ.put(None)

    def run(self):
        self.get_term()
        self.bowtie_map()
        target_gene, forward_dict, reverse_dict = self.build_dict_run()
        p = ProcessPoolExecutor(self.nproc)
        for gene in target_gene:
            p.submit(self.PCR_product(gene, forward_dict, reverse_dict))
        # This will submit all tasks to one place without blocking, and then each
        # thread in the thread pool will fetch tasks.
        n = 0
        primer_pair_id = defaultdict(int)
        primer_pair_acc = defaultdict(list)
        acc_id = set()
        # primer_reverse_id = defaultdict(int)
        with open(self.outfile, "w") as fo:
            headers = ["Chrom (or Genes)", "Start", "Stop", "Primer_F", "Primer_R", "Product length"]
            fo.write("\t".join(headers) + "\n")
            while n < len(target_gene):
                res = self.resQ.get()
                # The get method can read and delete an element from the queue. Similarly, the get method has two
                # optional parameters: blocked and timeout. If blocked is true (the default value) and timeout is
                # positive, no element is retrieved during the waiting time, and a Queue is thrown Empty exception.
                # If blocked is false, there are two cases. If a value of Queue is available, return the value
                # immediately. Otherwise, if the queue is empty, throw a Queue.Empty exception immediately.
                if res is None:
                    n += 1
                    continue
                primer_pair_id[res[3] + "\t" + res[4]] += 1
                primer_pair_acc[res[3] + "\t" + res[4]].append(res[0])
                acc_id.add(res[0])
                fo.write("\t".join(map(str, res)) + "\n")
                # get results before shutdown. Synchronous call mode: call, wait for the return value, decouple,
                # but slow.
        p.shutdown()
        primer_pair_id_sort = sorted(primer_pair_id.items(), key=lambda x: x[1], reverse=True)
        target_seq = set()
        with open(self.outfile + ".pair.num", "w") as fo:
            fo.write("Primer_F\tPrimer_R\tPair_num\ttarget accession number\n")
            for k in primer_pair_id_sort:
                primer_pair_acc_set = set(primer_pair_acc[k[0]])
                target_seq = target_seq.union(primer_pair_acc_set)
                fo.write(k[0] + "\t" + str(k[1]) + "\t" + str(len(primer_pair_acc_set)) + "\n")
        with open(self.outfile + ".total.acc.num", "w") as fo2:
            fo2.write("total coverage of primer set (PS) is: {}\n".format(len(acc_id)))
        if self.targets != "None":
            with open(self.outfile + ".unmatched.fa", "w") as out:
                raw_total_seq_dict = open(self.targets, "rb")
                total_dict = pickle.load(raw_total_seq_dict)
                print(len(set(total_dict.keys())), len(target_seq))
                unmatched_seq_set = set(total_dict.keys()) - target_seq
                with open(self.outfile + ".total.acc.num", "a+") as fo3:
                    fo3.write("total target number is: {}\n".format(len(total_dict.keys())))
                for unmatch in unmatched_seq_set:
                    out.write(total_dict[unmatch])

def Bowtie_index(Input, method):
    Bowtie_file = Path(Input).parent.joinpath("Bowtie_DB")
    Bowtie_prefix = Path(Bowtie_file).joinpath(Path(Input).stem)
    bowtie_cmd = method + "-build"
    if re.search("bowtie2", method):
        ref_index = Path(Bowtie_file).joinpath(Path(Input).name).with_suffix(".1.bt2")
        Bowtie_index = Path(Input).parent.joinpath(Path(Input).name).with_suffix(".1.bt2")
    elif re.search("bowtie", method):
        ref_index = Path(Bowtie_file).joinpath(Path(Input).name).with_suffix(".1.ebwt")
        Bowtie_index = Path(Input).parent.joinpath(Path(Input).name).with_suffix(".1.ebwt")
    else:
        print("bowtie1 or bowtie2 must be specified !!!")
        sys.exit(1)
    if ref_index.exists():
        return Bowtie_prefix
    else:
        if Bowtie_index.exists():
            return Input
        else:
            if Bowtie_file.exists():
                print("No Bowtie index found, start building ...")
            else:
                os.mkdir(Bowtie_file)
            os.system("{} {} {}".format(bowtie_cmd, Input, Bowtie_prefix))
            return Bowtie_prefix

