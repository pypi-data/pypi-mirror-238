#!/usr/bin/env python3
import argparse
import os
import re
from optparse import OptionParser
from pathlib import Path

import numpy as np
import sys
import math
from operator import mul
from math import log10
from functools import reduce
from bisect import bisect_left


# Melting temperature between 55-80◦C reduces the occurrence of hairpins
# Runs of three or more Cs or Gs at the 3'-ends of primers may promote mispriming at G or C-rich sequences
# (because of stability of annealing), and should be avoided.
def DPrime_argsParse():
    parser = argparse.ArgumentParser(description="For degenerate primer design")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Input file: multi-alignment output (muscle or others).", metavar="<file>")
    parser.add_argument("-l", "--plen", type=int, default=18,
                        help='Length of primer. Default: 18.', metavar="<int>")
    parser.add_argument("-n", "--dnum", type=int, default=4,
                        help='Max number of degenerate. Default: 4.', metavar="<int>")
    parser.add_argument("-d", "--degeneracy", type=int, default=10,
                        help='Max degeneracy of primer. Default: 10.', metavar="<int>")
    parser.add_argument("-v", "--variation", type=int, default=1,
                        help='Max mismatch number of primer. Default: 1', metavar="<int>")
    parser.add_argument("-e", "--entropy", type=float, default=3.6,
                        help='Entropy is actually a measure of disorder. This parameter is used to judge whether the '
                             'window is conservation. Entropy of primer-length window. Default: 3.6.',
                        metavar="<float>")
    parser.add_argument("-g", "--gc", type=str, default="0.2,0.7",
                        help='Filter primers by GC content. Default [0.2,0.7].', metavar="<str>")
    parser.add_argument("-s", "--size", type=int, default=100,
                        help='Filter primers by mini PRODUCT size. Default 100.', metavar="<int>")
    parser.add_argument("-f", "--fraction", type=float, default=0.8,
                        help='Filter primers by match fraction. If you set -s lower than 0.8, make sure that'
                             '--entropy greater than 3.6, because disorder region (entropy > 3.6) will not be processed'
                             'in multiPrime. Even these regions can design coverage with error greater than your '
                             'threshold, it wont be processed. Default: 0.8.', metavar="<float>")
    parser.add_argument("-c", "--coordinate", type=str, default="1,2,-1",
                        help='Mismatch index is not allowed to locate in your specific positions.'
                             'otherwise, it wont be regard as the mis-coverage. With this param, '
                             'you can control the index of Y-distance (number=variation and position of mismatch)'
                             'when calculate coverage with error. coordinate>0: 5\'==>3\'; coordinate<0: 3\'==>5\'.'
                             'You can set this param to any value that you prefer. Default: 1,-1. '
                             '1:  I dont want mismatch at the 2nd position, start from 0.'
                             '-1: I dont want mismatch at the -1st position, start fro -1.', metavar="<str>")
    parser.add_argument("-p", "--proc", type=int, default=20,
                        help='Number of process to launch. Default: 20.', metavar="<int>")
    parser.add_argument("-a", "--away", type=int, default=4,
                        help='Filter hairpin structure, which means distance of the minimal paired bases. Default: 4. '
                             'Example:(number of X) AGCT[XXXX]AGCT. '
                             'Primers should not have complementary sequences (no consecutive 4 bp complementarities),'
                             'otherwise the primers themselves will fold into hairpin structure.', metavar="<int>")
    parser.add_argument("-o", "--out", type=str, required=True,
                        help='output file', metavar="<file>")
    return parser.parse_args()

def Ppair_argsParse():
    parser = argparse.ArgumentParser(description="For degenerate primer design")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Input file: multiPrime out.", metavar="<file>")
    parser.add_argument("-r", "--ref", type=str, required=True,
                        help='Reference sequence file: all the sequence in 1 fasta, for example: (Cluster_96_171.tfa).',
                        metavar="<str>")
    parser.add_argument("-g", "--gc", type=str, default="0.2,0.7",
                        help='Filter primers by GC content. Default [0.2,0.7].', metavar="<str>")
    parser.add_argument("-f", "--fraction", type=float, default=0.6,
                        help='Filter primers by match fraction.Sometimes you need a small fraction to get output.'
                             'Default: 0.6.', metavar="<float>")
    parser.add_argument("-e", "--end", type=int, default=4,
                        help='Filter primers by degenerate base position. e.g. [-t 4] means I dont want degenerate base'
                             'appear at the end four bases when primer pre-filter. Default: 4.', metavar="<int>")
    parser.add_argument("-p", "--proc", type=int, default=20,
                        help='Number of process to launch. Default: 20.', metavar="<int>")
    parser.add_argument("-s", "--size", type=str, default="250,500",
                        help='Filter primers by PRODUCT size. Default [250,500].', metavar="<str>")
    parser.add_argument("-d", "--dist", type=int, default=4,
                        help='Filter param of hairpin, which means distance of the minimal paired bases. Default: 4.'
                             'Example:(number of X) AGCT[XXXX]AGCT.', metavar="<int>")
    parser.add_argument("-t", "--Tm", type=int, default=4,
                        help='Difference of Tm between primer-F and primer-R. Default: 4.', metavar="<int>")
    parser.add_argument("-a", "--adaptor", type=str, default="TCTTTCCCTACACGACGCTCTTCCGATCT,"
                                                             "TCTTTCCCTACACGACGCTCTTCCGATCT",
                        help='Adaptor sequence, which is used for NGS next. Hairpin or dimer detection for ['
                             'adaptor--primer]. For example: TCTTTCCCTACACGACGCTCTTCCGATCT,'
                             'TCTTTCCCTACACGACGCTCTTCCGATCT (Default). If you dont want adaptor, use [","]',
                        metavar="<str>")
    parser.add_argument("-m", "--maxseq", type=int, default=0,
                        help='Limit of sequence number. Default: 0. If 0, then all sequence will take into account.\n'
                             'This param should consistent with [max_seq] in multi-alignment [muscle].',
                        metavar="<int>")
    parser.add_argument("-o", "--out", type=str, required=True,
                        help='Output file: candidate primers. e.g. [*].candidate.primers.txt.'
                             'Header of output: Primer_F_seq, Primer_R_seq, Product length:Tm:coverage_percentage,'
                             'coverage_number, Primer_start_end', metavar="<file>")
    return parser.parse_args()

def Perfect_argsParse():
    parser = OptionParser('Usage: %prog Perfect -r [reference] -i [input] -p [10] -f [format] -o [output] '
                          '-s [Coverage.xls]', version="%prog 0.0.2")
    parser.add_option('-r', '--ref',
                      dest='ref',
                      help='reference file: all the input sequences in 1 fasta.')

    parser.add_option('-i', '--input',
                      dest='input',
                      help='Primer file. One of the followed three types:\n '
                           'final_maxprimers_set.xls \n primer.fa \n primer_F,primer_R.')

    parser.add_option('-f', '--format',
                      dest='format',
                      help='Format of primer file: xls or fa or seq; default: xls. \n '
                           'xls: final_primer_set.xls, output of multiPrime. \n'
                           'fa: fasta format. \n'
                           'seq: sequence format, comma seperate. e.g. primer_F,Primer_R.')

    parser.add_option('-o', '--out',
                      dest='out',
                      default="PCR_product",
                      help='Output_dir. default: PCR_product.')

    parser.add_option('-p', '--process',
                      dest='process',
                      default="10",
                      type="int",
                      help='Number of process to launch.  default: 10.')

    parser.add_option('-s', '--stast',
                      dest='stast',
                      default="Coverage.xls",
                      help='Stast information: number of coverage and total. Default: Coverage.xls')
    (options, args) = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)
    elif options.ref is None:
        parser.print_help()
        print("Input (reference) file must be specified !!!")
        sys.exit(1)
    elif options.input is None:
        parser.print_help()
        print("Primer file or sequence must be specified !!!")
        sys.exit(1)
    elif options.format is None:
        parser.print_help()
        print("Primer file format must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()

def Errors_argsParse():
    parser = argparse.ArgumentParser(description="For mismatch coverage stastic.")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="input file: primer.fa.", metavar="<file>")
    parser.add_argument("-r", "--ref", type=str, required=True,
                        help='Reference sequence file: Reference file. The program will first search for Bowtie index '
                             'files using the parameter you provided as the prefix. If the files are not found, '
                             'it will build an index using the prefix you provided. Otherwise, '
                             'the program will use the Bowtie index prefix you provided.',
                        metavar="<str>")
    parser.add_argument("-l", "--len", type=int, default=0,
                        help='Length of primer, which is used for mapping. If the length of the primer used for '
                             'mapping is set to 0, the entire length of the primer will be utilized. Default: 0',
                        metavar="<int>")
    parser.add_argument("-t", "--term", type=int, default=4,
                        help='Position of mismatch is not allowed in the 3 term of primer. Default: 4', metavar="<int>")
    parser.add_argument("-s", "--size", type=str, default="100,1500",
                        help='Length of PCR product, default: 100,1500.', metavar="<str>")
    parser.add_argument("-p", "--proc", type=int, default=20,
                        help='Number of process to launch. Default: 20.', metavar="<int>")

    parser.add_argument("-b", "--bowtie", type=str, default="bowtie2",
                        help='bowtie/ABS_path(bowtie) or bowtie2/ABS_path(bowtie2) was employed for mapping. '
                             'Default: bowtie2', metavar="<str>")
    parser.add_argument("-m", "--seedmms", type=int, default=1,
                        help='Bowtie: Mismatches in seed (can be 0 - 3, default: -n 1).'
                             'Bowtie2: Gap or mismatches in seed (can be 0 - 1, default: -n 1)',
                        metavar="<int>")
    parser.add_argument("-d", "--dict", type=str, default="None",
                        help='Dictionary of targets sequences, binary format. '
                             'It can be obtained from prepare_fa_pickle.py.', metavar="<str>")
    parser.add_argument("-o", "--out", type=str, required=True,
                        help='Output file: Prodcut of PCR product with primers.', metavar="<file>")
    return parser.parse_args()


def main_Usage():
    print('Usage (version 2.4.6): \n'
          'multiPrime DPrime:  Degenerate primer design through MD-DPD or MD-EDPD.\n'
          'multiPrime Ppair:   Primer pair selection from the result of multiPrime DPrime.\n'
          'multiPrime Perfect: Extract primer-contained sequences with non-mismatches.\n'
          'multiPrime Errors:  Extract primer-contained sequences with errors.\n')


degenerate_base = {"-": ["-"], "A": ["A"], "G": ["G"], "C": ["C"], "T": ["T"], "R": ["A", "G"], "Y": ["C", "T"],
                   "M": ["A", "C"], "K": ["G", "T"], "S": ["G", "C"], "W": ["A", "T"], "H": ["A", "T", "C"],
                   "B": ["G", "T", "C"], "V": ["G", "A", "C"], "D": ["G", "A", "T"], "N": ["A", "T", "G", "C"]}

score_table = {"-": 100, "#": 0, "A": 1, "G": 1.11, "C": 1.21, "T": 1.4, "R": 2.11, "Y": 2.61, "M": 2.21,
               "K": 2.51, "S": 2.32, "W": 2.4, "H": 3.61, "B": 3.72, "V": 3.32, "D": 3.51, "N": 4.72}

trans_score_table = {v: k for k, v in score_table.items()}

##############################################################################################
############################# Calculate free energy ##########################################
##############################################################################################
freedom_of_H_37_table = [[-0.7, -0.81, -0.65, -0.65],
                         [-0.67, -0.72, -0.8, -0.65],
                         [-0.69, -0.87, -0.72, -0.81],
                         [-0.61, -0.69, -0.67, -0.7]]

penalty_of_H_37_table = [[0.4, 0.575, 0.33, 0.73],
                         [0.23, 0.32, 0.17, 0.33],
                         [0.41, 0.45, 0.32, 0.575],
                         [0.33, 0.41, 0.23, 0.4]]

H_bonds_number = [[2, 2.5, 2.5, 2],
                  [2.5, 3, 3, 2.5],
                  [2.5, 3, 3, 2.5],
                  [2, 2.5, 2.5, 2]]
adjust_initiation = {"A": 0.98, "T": 0.98, "C": 1.03, "G": 1.03}
adjust_terminal_TA = 0.4
# Symmetry correction applies only to self-complementary sequences.
# symmetry_correction = 0.4
symmetry_correction = 0.4

##############################################################################################
base2bit = {"A": 0, "C": 1, "G": 2, "T": 3, "#": 4}
TRANS = str.maketrans("ATCG", "TAGC")


##############################################################################################
# 37°C and 1 M NaCl
Htable2 = [[-7.9, -8.5, -8.2, -7.2, 0],
           [-8.4, -8, -9.8, -8.2, 0],
           [-7.8, -10.6, -8, -8.5, 0],
           [-7.2, -7.8, -8.4, -7.9, 0],
           [0, 0, 0, 0, 0]]
Stable2 = [[-22.2, -22.7, -22.2, -21.3, 0],
           [-22.4, -19.9, -24.4, -22.2, 0],
           [-21, -27.2, -19.9, -22.7, 0],
           [-20.4, -21, -22.4, -22.2, 0],
           [0, 0, 0, 0, 0]]
Gtable2 = [[-1, -1.45, -1.3, -0.58, 0],
           [-1.44, -1.84, -2.24, -1.3, 0],
           [-1.28, -2.17, -1.84, -1.45, 0],
           [-0.88, -1.28, -1.44, -1, 0],
           [0, 0, 0, 0, 0]]
H_adjust_initiation = {"A": 2.3, "T": 2.3, "C": 0.1, "G": 0.1}
S_adjust_initiation = {"A": 4.1, "T": 4.1, "C": -2.8, "G": -2.8}
G_adjust_initiation = {"A": 1.03, "T": 1.03, "C": 0.98, "G": 0.98}
H_symmetry_correction = 0
S_symmetry_correction = -1.4
G_symmetry_correction = 0.4
##############################################################################################
# ng/ul
primer_concentration = 100
Mo_concentration = 50
Di_concentration = 1.5
dNTP_concentration = 0.25
Kelvin = 273.15
# reference (Owczarzy et al.,2008)
crossover_point = 0.22

bases = np.array(["A", "C", "G", "T"])
di_bases = []
for i in bases:
    for j in bases:
        di_bases.append(i + j)


def Penalty_points(length, GC, d1, d2):
    return log10((2 ** length * 2 ** GC) / ((d1 + 0.1) * (d2 + 0.1)))

def nan_removing(pre_list):
    while np.nan in pre_list:
        pre_list.remove(np.nan)
    return pre_list

di_nucleotides = set()
for i in base2bit.keys():
    single = i * 4
    di_nucleotides.add(single)
    for j in base2bit.keys():
        if i != j:
            di = (i + j) * 4
            di_nucleotides.add(di)
        for k in base2bit.keys():
            if i != j != k:
                tri = (i + j + k) * 3
                di_nucleotides.add(tri)

TRANS = str.maketrans("ATGCRYMKSWHBVDN", "TACGYRKMSWDVBHN")


def score_trans(sequence):
    return reduce(mul, [math.floor(score_table[x]) for x in list(sequence)])


def dege_number(sequence):
    return sum(math.floor(score_table[x]) > 1 for x in list(sequence))


def RC(seq):
    return seq.translate(TRANS)[::-1]

def Penalty_points(length, GC, d1, d2):
    return log10((2 ** length * 2 ** GC) / ((2 ** d1 - 0.9) * (2 ** d2 - 0.9)))

##############################################################################################
############## m_distance which is used to calculate (n)-nt variation coverage ###############
# Caution: this function only works when degeneracy of seq2 < 2 (no degenerate in seq2).
##############################################################################################
def Y_distance(seq1, seq2):
    seq_diff = list(np.array([score_table[x] for x in list(seq1)]) - np.array([score_table[x] for x in list(seq2)]))
    m_dist = [idx for idx in range(len(seq_diff)) if seq_diff[idx] not in score_table.values()]
    return m_dist


##############################################################################################
def symmetry(seq):
    if len(seq) % 2 == 1:
        return False
    else:
        F = seq[:int(len(seq) / 2)]
        R = RC(seq[int(len(seq) / 2):][::-1])
        if F == R:
            return True
        else:
            return False


def closest(my_list, my_number1, my_number2):
    index_left = bisect_left(my_list, my_number1)
    # find the first element index in my_list which greater than my_number.
    if my_number2 > my_list[-1]:
        index_right = len(my_list) - 1  # This is index.
    else:
        index_right = bisect_left(my_list, my_number2) - 1
    return index_left, index_right


def Calc_deltaH_deltaS(seq):
    Delta_H = 0
    Delta_S = 0
    for n in range(len(seq) - 1):
        i, j = base2bit[seq[n + 1]], base2bit[seq[n]]
        Delta_H += Htable2[i][j]
        Delta_S += Stable2[i][j]
    seq = seq.replace("#", '')
    Delta_H += H_adjust_initiation[seq[0]] + H_adjust_initiation[seq[-1]]
    Delta_S += S_adjust_initiation[seq[0]] + S_adjust_initiation[seq[-1]]
    if symmetry(seq):
        Delta_S += S_symmetry_correction
    return Delta_H * 1000, Delta_S


# salt_adjust = math.log(Tm_Na_adjust / 1000.0, math.e)
# def S_adjust(seq):
#     n = len(seq) - 1
#     # S_Na_adjust = 0.847 * n * salt_adjust
#     # Oligonucleotide Melting Temperatures under PCR Conditions: Nearest-Neighbor Corrections for
#     # Mg2+ , Deoxynucleotide Triphosphate, and Dimethyl Sulfoxide Concentrations with
#     # Comparison to Alternative Empirical Formulas
#     S_Na_adjust = 0.368 * n * salt_adjust
#     # A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics
#     return S_Na_adjust
# where n is the total number of phosphates in the duplex divided by 2,
# This is equal to the oligonucleotide length minus 1.

def GC_fraction(seq):
    return round((list(seq).count("G") + list(seq).count("C")) / len(list(seq)), 3)


# different salt corrections for monovalent (Owczarzy et al.,2004) and divalent cations (Owczarzy et al.,2008)
def Calc_Tm_v2(seq):
    delta_H, delta_S = Calc_deltaH_deltaS(seq)
    # Note that the concentrations in the following Eq is mmol/L, In all other equations,concentration are mol/L
    # Monovalent cations are typically present as K+ and Tris+ in PCR buffer,
    # K+ is similar to Na+ in regard to duplex stabilization
    # if Di_concentration > dNTP_concentration:
    #     Tm_Na_adjust = Mo_concentration + 120 * math.sqrt(Di_concentration - dNTP_concentration)
    # else:
    #     Tm_Na_adjust = Mo_concentration
    Tm_Na_adjust = Mo_concentration

    if dNTP_concentration >= Di_concentration:
        free_divalent = 0.00000000001
    else:
        free_divalent = (Di_concentration - dNTP_concentration) / 1000.0
    R_div_monov_ratio = (math.sqrt(free_divalent)) / (Mo_concentration / 1000)

    if R_div_monov_ratio < crossover_point:
        # use only monovalent salt correction, [equation 22] (Owczarzy et al., 2004)
        correction = (((4.29 * GC_fraction(seq)) - 3.95) * pow(10, -5) * math.log(Tm_Na_adjust / 1000.0, math.e)) \
                     + (9.40 * pow(10, -6) * (pow(math.log(Tm_Na_adjust / 1000.0, math.e), 2)))
    else:
        # magnesium effects are dominant, [equation 16] (Owczarzy et al., 2008) is used
        # Table 2
        a = 3.92 * pow(10, -5)
        b = - 9.11 * pow(10, -6)
        c = 6.26 * pow(10, -5)
        d = 1.42 * pow(10, -5)
        e = - 4.82 * pow(10, -4)
        f = 5.25 * pow(10, -4)
        g = 8.31 * pow(10, -5)
        if R_div_monov_ratio < 6.0:
            a = 3.92 * pow(10, -5) * (
                    0.843 - (0.352 * math.sqrt(Tm_Na_adjust / 1000.0) * math.log(Tm_Na_adjust / 1000.0, math.e)))
            d = 1.42 * pow(10, -5) * (
                    1.279 - 4.03 * pow(10, -3) * math.log(Tm_Na_adjust / 1000.0, math.e) - 8.03 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 2))
            g = 8.31 * pow(10, -5) * (
                    0.486 - 0.258 * math.log(Tm_Na_adjust / 1000.0, math.e) + 5.25 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 3))
        # Eq 16
        correction = a + (b * math.log(free_divalent, math.e))
        + GC_fraction(seq) * (c + (d * math.log(free_divalent, math.e)))
        + (1 / (2 * (len(seq) - 1))) * (e + (f * math.log(free_divalent, math.e))
                                        + g * (pow((math.log(free_divalent, math.e)), 2)))

    if symmetry(seq):
        # Equation A
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (1 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    else:
        # Equation B
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (4 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    return Tm


##############################################################################################

def Bowtie_index(Input, method):
    Bowtie_file = Path(Input).parent.joinpath("Bowtie_DB")
    Bowtie_prefix = Path(Bowtie_file).joinpath(Path(Input).stem)
    bowtie_cmd = method + "-build"
    if re.search("bowtie2", method):
        ref_index = Path(Bowtie_file).joinpath(Path(Input).name).with_suffix(".1.bt2")
    elif re.search("bowtie", method):
        ref_index = Path(Bowtie_file).joinpath(Path(Input).name).with_suffix(".1.ebwt")
    else:
        print("bowtie1 or bowtie2 must be specified !!!")
        sys.exit(1)
    if ref_index.exists():
        return Bowtie_prefix
    else:
        if Bowtie_file.exists():
            print("No Bowtie index found, start building ...")
        else:
            os.mkdir(Bowtie_file)
        os.system("{} {} {}".format(bowtie_cmd, Input, Bowtie_prefix))
        return Bowtie_prefix