from pyfaidx import Fasta
from pyfastx import Fastq, Sequence
from pathlib import Path
from fastq import FastQ
from itertools import combinations
import Levenshtein
from typing import List

class ErrorCorrector:
    def __init__(self, filepath: Path):
        self.fastq = FastQ(filepath)

    def write(self, path: Path):
        self.fastq.write(path)

    def remove_homonucleotides(self):
        for i, read in enumerate(self.fastq):
            new_seq = ""
            prev = ""
            for base in read.seq:
                if not base == prev:
                    prev = base
                    new_seq += base
            self.fastq[i].seq = new_seq

    def remove_subsequence(self, primer: str, distance: int, remove_other: bool):
        max_length = len(primer)+2*distance
        min_length = len(primer)-2*distance

        print("before: " + str(len(self.fastq.reads)) + " reads")
        # Iterate over Reads
        for read_index, read in enumerate(self.fastq):
            sequence = read.seq
            subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
                            if len(sequence[x:y]) == max_length]

            min_dist = distance+1
            position = -1

            # Iterate over all subsequences of length max_length in read
            for i, subsequence in enumerate(subsequences):
                actual_distance = Levenshtein.distance(subsequence, primer)
                if actual_distance < min_dist:
                    min_dist = actual_distance
                    position = i
                    if min_dist == 0:
                        break

            if min_dist <= 3*distance:
                sequence = subsequences[position]
                subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
                                if len(sequence[x:y]) >= min_length]

                # Iterate over subsequences of length equal or greater than min_length
                for i, subsequence in enumerate(subsequences):
                    actual_distance = Levenshtein.distance(subsequence, primer)
                    if actual_distance <= min_dist and actual_distance <= distance:
                        min_dist = actual_distance
                        position = i
                        if min_dist == 0:
                            break

                if position >= 0:
                    read.seq = read.seq.replace(subsequences[position], "")

            print(position)
            if remove_other and position < 0:
                self.fastq.reads.remove(read)

        print("after: " + str(len(self.fastq.reads)) + " reads")

    def __find_best_fit__(self, sequence: str, subsequences: List[str]):
        min_dist = max(max(len(sub) for sub in subsequences), len(sequence))
        position = -1
        for i, subsequence in enumerate(subsequences):
            actual_distance = Levenshtein.distance(subsequence, sequence)
            if actual_distance <= min_dist:
                min_dist = actual_distance
                position = i
                if min_dist == 0:
                    break
        return position
