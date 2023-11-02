#!/usr/bin/env python3

from .src import *
import time
import sys


def main():
    if len(sys.argv) < 2:
        main_Usage()
    elif sys.argv[1] == "DPrime":
        args = DPrime_argsParse()
        NN_APP = NN_degenerate(seq_file=args.input, primer_length=args.plen, coverage=args.fraction,
                               number_of_dege_bases=args.dnum, score_of_dege_bases=args.degeneracy,
                               raw_entropy_threshold=args.entropy, product_len=args.size, position=args.coordinate,
                               variation=args.variation, distance=args.away, GC=args.gc,
                               nproc=args.proc, outfile=args.out)
        NN_APP.run()


    elif sys.argv[1] == "Ppair":
        args = Ppair_argsParse()
        primer_pairs = Primers_filter(ref_file=args.ref, primer_file=args.input, adaptor=args.adaptor,
                                      rep_seq_number=args.maxseq, distance=args.dist, outfile=args.out,
                                      size=args.size, position=args.end, fraction=args.fraction,
                                      diff_Tm=args.Tm, nproc=args.proc)
        primer_pairs.run()

    elif sys.argv[1] == "Perfect":
        (options, args) = Perfect_argsParse()
        results = Product_perfect(primer_file=options.input, output_file=options.out, ref_file=options.ref,
                                  file_format=options.format, coverage=options.stast, nproc=options.process)
        results.run()

    elif sys.argv[1] == "Errors":
        args = Errors_argsParse()
        ref_index = Bowtie_index(args.ref, args.bowtie)
        prediction = Errors(primer_file=args.input, term_length=args.len, reference_file=ref_index,
                            PCR_product_size=args.size, mismatch_num=args.seedmms, outfile=args.out,
                            term_threshold=args.term, bowtie=args.bowtie, nproc=args.proc,
                            targets=args.dict)
        prediction.run()
    else:
        print("No subprocess!")
        sys.exit(1)


if __name__ == "__main__":
    e1 = time.time()
    main()
    e2 = time.time()
    print("INFO {} Total times: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                           round(float(e2 - e1), 2)))
