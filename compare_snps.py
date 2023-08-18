import csv
import argparse


def get_snps(file_name):
    with open(file_name) as handler:
        reader = list(csv.reader(handler))[1:]
    my_set = set()

    for e in reader:
        my_set.add((e[0], e[1], e[2], e[4], e[5]))
    return my_set


def get_snps_tsv(file_name):
    with open(file_name) as handler:
        reader = list(csv.reader(handler, delimiter="\t"))[1:]
    my_set = set()

    for e in reader:
        my_set.add((e[0], e[1], e[2], e[4], e[5]))
    return my_set


def main():
    parser = argparse.ArgumentParser(
        description='Check the differences between 2 VCFs.')
    parser.add_argument('--f1', dest='file_1',
                        required=True, help='The snakemake vcf file (csv)')
    parser.add_argument('--f2', dest='file_2',
                        required=True, help='The insaflu vcf file (tsv)')
    parser.add_argument('--output', dest='output',
                        help='File to save number of differences')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    s_set = get_snps(args.file_1)
    i_set = get_snps_tsv(args.file_2)

    if args.verbose:
        print("Snakemake Entries: ", len(s_set))
        print("Website Entries: ", len(i_set))

        print("Intersection: ", len(s_set.intersection(i_set)))
        print("Symmetric Difference: ", len(s_set.symmetric_difference(i_set)))
    if args.output:
        with open(args.output, "w") as handler:
            writer = csv.writer(handler)
            for x in s_set.symmetric_difference(i_set):
                writer.writerow(x)


if __name__ == "__main__":
    main()
