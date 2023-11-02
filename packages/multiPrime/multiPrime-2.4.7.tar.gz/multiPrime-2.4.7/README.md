# multiPrime

`multiPrime (version=2.4.7) is an error-tolerant primer design tool for broad-spectrum pathogens detection. 
It proposes a solution for the maximal coverage degenerate primer design with error (MD-EDPD).
pipeline links: https://github.com/joybio/multiPrime.` 

## 1. Install

> pip

```
pip3 install multiPrime
```

+ `pip` `python >=3.9`



## 2. Usage

```
$ multiPrime -h 
```
Parameters：

| Parameters    | Description                                                 |
|---------------|-------------------------------------------------------------|
| DPrime        | Degenerate primer design through MD-EDPD or MD-DPD.         |
| Ppair         | Primer pair selection from the result of multiPrime DPrime. |
| Perfect       | Extract primer-contained sequences with non-mismatches.     |
| Errors        | Extract primer-contained sequences with errors.             |
```
multiPrime DPrime -i input -o output
           Options: { -l [18] -n [4] -d [10] -v [1] -g [0.2,0.7] -f [0.8] -c [4] -p [10] -a [4] }
```
Parameters：

| Parameters      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i/--input      | Input file: Result of multi-alignment. (muscle, mafft or others)                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -l/--plen       | Length of primer. Default: 18                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -n/--dnum       | Number of degenerate. Default: 4.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -v/--variation  | Max mismatch number of primer. Default: 1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -e/--entropy    | Entropy is actually a measure of disorder. This parameter is used to judge whether the window is conservation. Entropy of primer-length window. Default: 3.6.                                                                                                                                                                                                                                                                                                                                                |
| -g/--gc         | Filter primers by GC content. Default [0.2,0.7].                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -s/--size       | Number of degenerate. Default: 4.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -f/--fraction   | Filter primers by match fraction (Coverage with errors). Default: 0.8.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -c/--coordinate | Mismatch index is not allowed to locate in your specific positions. otherwise, it won't be regard as the mis-coverage. With this param, you can control the index of Y-distance (number=variation and position of mismatch). when calculate coverage with error. coordinate>0: 5'==>3'; coordinate<0: 3'==>5'. You can set this param to any value that you prefer. Default: 1,-1. 1:  I dont want mismatch at the 2nd position, start from 0. -1: I dont want mismatch at the -1st position, start from -1. |
| -p/--proc       | Number of process to launch. Default: 20.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -a/--away       | Filter hairpin structure, which means distance of the minimal paired bases. Default: 4. Example:(number of X) AGCT[XXXX]AGCT. Primers should not have complementary sequences (no consecutive 4 bp complementarities),otherwise the primers themselves will fold into hairpin structure.                                                                                                                                                                                                                     |
| -o/--out        | Output file: candidate primers. e.g.  [*].candidate.primers.out.                                                                                                                                                                                                                                                                                                                                                                                                                                             |
```
multiPrime Ppair -i input -r reference -o output
           Options: {-f [0.6] -m [500] -n [200] -e [4] -p [9] -s [250,500] -g [0.4,0.6] -d [4] -a ","}
```
Parameters：

| Parameters    | Description                                                                                                                                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i/--input    | Input file: output of multiPrime DPrime.                                                                                                                                                                            |
| -r/--ref      | Reference sequence file: all the sequence in 1 fasta, for example: (Cluster_96_171.tfa).                                                                                                                            |
| -g/--gc       | Filter primers by GC content. Default [0.2,0.7].                                                                                                                                                                    |
| -f/--fraction | Filter primers by match fraction. Default: 0.6. Sometimes you need a small fraction to get output.                                                                                                                  |
| -e/--end      | Filter primers by degenerate base position. e.g. [-e 4] means I dont want degenerate base appear at the end four bases when primer pre-filter. Default: 4.                                                          |
| -s/--size     | Filter primers by PRODUCT size. Default [250,500].                                                                                                                                                                  |
| -d/--dist     | Filter param of hairpin, which means distance of the minimal paired bases. Default: 4. Example:(number of X) AGCT[XXXX]AGCT.                                                                                        |
| -t/--tm       | Difference of Tm between primer-F and primer-R. Default: 5.                                                                                                                                                         |
| -p/--proc     | Number of process to launch. Default: 20.                                                                                                                                                                           |
| -a/--adaptor  | Adaptor sequence, which is used for NGS next. Hairpin or dimer detection for [adaptor--primer]. example: TCTTTCCCTACACGACGCTCTTCCGATCT,TCTTTCCCTACACGACGCTCTTCCGATCT (Default). If you dont want adaptor, use [","] |
| -m/--maxseq   | Limit of sequence number. Default: 0. If 0, then all sequence will take into account. This param should consistent with [max_seq] in multi-alignment.                                                               |
| -o/--out      | Output file: candidate primer pairs. e.g.  [*].candidate.primers.txt.                                                                                                                                               |
```
multiPrime Perfect -i [input] -p [10] -f [format] -o [output] -s [Coverage.xls]
```
Parameters：

| Parameters   | Description                                                                                                                                                                                                    |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i/--input   | Input file: Primer file. One of the followed three types: final_maxprimers_set.xls (see output of multiPrime in github (https://github.com/joybio/multiPrime)); primer.fa (primer fasta) or primer_F,primer_R. |
| -r/--ref     | Sequence file: all the input sequences in 1 fasta.                                                                                                                                                             |
| -f/--format  | Format of primer file: xls or fa or seq; default: xls, indicate final_maxprimers_set.xls. xls: final_primer_set.xls; fa:fasta format or seq: sequence format, comma seperate. e.g. primer_F,Primer_R.          |
| -p/--process | Number of process to launch. Default: 20.                                                                                                                                                                      |
| -o/--out     | Output_dir. default: PCR_product.                                                                                                                                                                              |
| -s/--stast   | Stast information: number of coverage and total. Default: Coverage.xls.                                                                                                                                        |
```
multiPrime Errors -i [input] -r [bowtie index] -l [150,2000] -p [10]-o [output]
```
Parameters：

| Parameters   | Description                                                                                                                                                                                    |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i/--input   | input file: primer.fa.                                                                                                                                                                         |
| -r/--ref     | reference file: the fasta of raw input.                                                                                                                                                        |
| -l/--len     | Length of primer, which is used for mapping. If the length of the primer used for mapping is set to 0, the entire length of the primer will be utilized. Default: 0                            |
| -d/--dict    | It is used to extract non-coverd sequences and can be obtained from prepare_fa_pickle.py (https://github.com/joybio/multiPrime). Dictionary of targets sequences, binary format. Default: None |
| -t/--term    | Position of mismatch is not allowed in the 3 term of primer. Default: 4                                                                                                                        |
| -b/--bowtie  | bowtie/ABS_path(bowtie) or bowtie2/ABS_path(bowtie2) was employed for mapping. Default: bowtie2                                                                                                |
| -m/--seedmms | Bowtie: Mismatches in seed (can be 0 - 3, default: -n 1).Bowtie2: Gap or mismatches in seed (can be 0 - 1, default: -n 1).                                                                     |
| -p/--process | Number of process to launch. Default: 20.                                                                                                                                                      |
| -o/--out     | Output file: PCR product with primers.                                                                                                                                                         |


## 3. Results

multiPrime DPrime
+ `output`：Information of primer.
+ `output.gap_seq_id_json`: Positions and non-contained sequences caused by errors (number of errors are greater than threshold).
+ `output.non_coverage_seq_id_json`: Positions and non-contained sequences.

multiPrime Ppair 
+ `output`：*.candidate.primers.txt

multiPrime Perfect 
+ `output`：PCR_product
+ `Coverage.xls`：Total coverage for all primers.

multiPrime Errors 
+ `output`：PCR product with primer pairs.
+ `output.pair.num`：Target amplicon number with primer pairs.
+ `others`：Temp files.
+ `unmatched.fa`: the sequences that were not captured by the core primer set with setting mismatches.

## 4. test dir


multiPrime/example


## 5. Contact


Please send comments, suggestions, bug reports and bug fixes to 1806389316@pku.edu.cn
