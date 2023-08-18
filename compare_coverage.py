import argparse
import csv


def get_coverage_dictionary(filename, locus_number) -> dict[str, list[str]]:
    d = {}
    with open(filename) as handler:
        for line in handler.readlines()[4:]:
            line = line.strip().split(",")
            coverage = line[-locus_number:]
            sample_name = line[0]
            d[sample_name] = coverage
    return d


def get_coverage_dictionary_tsv(filename, locus_number) -> dict[str, list[str]]:
    d = {}
    with open(filename) as handler:
        for line in handler.readlines()[8:]:
            line = list(map(lambda x: x.replace(
                '"', ""), line.strip().split("\t")))
            coverage = line[-locus_number:]
            sample_name = line[0]
            d[sample_name] = coverage
    return d


def main():
    parser = argparse.ArgumentParser(
        description='Check the differences between 2 coverage files.')
    parser.add_argument('--f1', dest='coverage_1',
                        required=True, help='The snakemake coverage file (csv)')
    parser.add_argument('--f2', dest='coverage_2',
                        required=True, help='The insaflu coverage file (tsv)')
    parser.add_argument('--output', dest='output',
                        help='File to save number of differences')
    parser.add_argument('--n_locus', dest="locus_number", required=True,
                        help="Number of segments in the genome")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    locus_number = int(args.locus_number)
    first_file = args.coverage_1
    second_file = args.coverage_2

    d_first = get_coverage_dictionary(first_file, locus_number)
    d_second = get_coverage_dictionary_tsv(second_file, locus_number)
    id_not_fount: set[str] = set(
        d_first).symmetric_difference(set(d_second))

    id_analyzed = {}
    for key in d_first:
        coverage = d_second.get(key, False)
        if coverage:
            if d_first[key] == coverage:
                id_analyzed[key] = 0
            else:
                id_analyzed[key] = 0
                for i, j in zip(d_first[key], d_second[key]):
                    if i != j:
                        id_analyzed[key] += 1

    if args.verbose:
        print("Identifiers:")
        print(f"\tFasta 1: {len(d_first)} ids")
        print(f"\tFasta 2: {len(d_second)} ids")
        print(f"Number of equal ids: {list(id_analyzed.values()).count(0)}")
        print(
            f"Number of ids not found in both: {len(id_not_fount)}")
    if args.output:
        with open(args.output, "w") as handler:
            writer = csv.writer(handler)
            writer.writerow(["Identifier", "Differences"])
            for k, v in id_analyzed.items():
                writer.writerow([k, v])
        if len(id_not_fount):
            with open("not_found_" + args.output, "w") as handler:
                writer = csv.writer(handler)
                writer.writerow(["Identifier"])
                for id in id_not_fount:
                    writer.writerow([id])


if __name__ == "__main__":
    main()
