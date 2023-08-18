import csv
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from typing import Iterable
import argparse


def import_consensus(path: str):
    with open(path) as handler:
        raw_records: Iterable[SeqRecord] = SeqIO.parse(handler, "fasta")

        records: dict[str, SeqRecord] = {}
        for record in raw_records:
            records[record.id] = record

        return records


def compare_two_seqs(seq1: SeqRecord, seq2: SeqRecord) -> int:
    differences = 0
    for f, s in zip(seq1.seq, seq2.seq):
        if f != s:
            differences += 1
    return differences


def main():
    parser = argparse.ArgumentParser(
        description='Check the differences between 2 fasta files.')
    parser.add_argument('--f1', dest='fasta_1',
                        required=True, help='The first fasta file')
    parser.add_argument('--f2', dest='fasta_2',
                        required=True, help='The second fasta file')
    parser.add_argument('--output', dest='output',
                        help='File to save number of differences')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    first_records = import_consensus(args.fasta_1)
    second_records = import_consensus(args.fasta_2)

    id_analyzed: dict[str, int] = {}
    id_not_found: set[str] = set(
        first_records).symmetric_difference(set(second_records))
    for id in first_records:
        f_record = first_records.get(id)
        s_record = second_records.get(id)
        if f_record and s_record:
            differences = compare_two_seqs(f_record, s_record)
            id_analyzed[id] = differences
    if args.verbose:
        print("Identifiers:")
        print(f"\tFasta 1: {len(first_records)} ids")
        print(f"\tFasta 2: {len(second_records)} ids")
        print(f"Number of equal ids: {list(id_analyzed.values()).count(0)}")
        print(
            f"Number of ids not found in both: {len(id_not_found)}")
    if args.output:
        with open(args.output, "w") as handler:
            writer = csv.writer(handler)
            writer.writerow(["Identifier", "Differences"])
            for k, v in id_analyzed.items():
                writer.writerow([k, v])
        if len(id_not_found):
            with open("not_found_" + args.output, "w") as handler:
                writer = csv.writer(handler)
                writer.writerow(["Identifier"])
                for id in id_not_found:
                    writer.writerow([id])


if __name__ == "__main__":
    main()
