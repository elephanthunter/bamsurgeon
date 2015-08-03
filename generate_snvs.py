
import argparse
import pysam

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--varfile', dest='varFileName', required=True, help='Target regions to try and add a SNV, as BED')
    parser.add_argument('-r', '--reference', dest='refFasta', required=True, help='reference genome, fasta indexed with bwa index -a stdsw _and_ samtools faidx')
    parser.add_argument('-i', '--intervals', dest='intervals', required=True, help='reference genome, fasta indexed with bwa index -a stdsw _and_ samtools faidx')
    args = parser.parse_args()

    # Determine the location of C's and G's in the genome
    reffile = pysam.Fastafile(args.refFasta)
    refbases = None
    with open(args.intervals, "r") as f:
        chrom = None
        for row in f.readlines():
            tokens = row.split()
            if chrom is None:
                chrom = tokens[0]
                refbases = reffile.fetch(chrom, 1, 1000000000)
            elif chrom != tokens[0]:
                chrom = tokens[0]
                refbases = reffile.fetch(chrom, 1, 1000000000)

            start = int(tokens[1])
            end = int(tokens[2])

            # hack
            start += 10
            end -= 10
            if end - start < 0:
                continue

            if refbases is not None:
                for position, refbase in enumerate(refbases[start:end]):
                    position = str(position+start)
                    if refbase == "G":
                        print "\t".join([chrom, position, position,  "0.95", "A"])
                    elif refbase == "C":
                        print "\t".join([chrom, position, position, "0.95", "T"])


if __name__ == '__main__':
    main()