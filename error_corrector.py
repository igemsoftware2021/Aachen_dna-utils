from pyfaidx import Fasta
from pyfastx import Fastq, Sequence
from pathlib import Path
from fastq import FastQ
from itertools import combinations
import Levenshtein

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
        for read in self.fastq:
            sequence = read.seq
            subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
                            if len(sequence[x:y]) == max_length]

            min_dist = max_length
            position = -1
            for i, subsequence in enumerate(subsequences):
                dist = Levenshtein.distance(subsequence, primer)
                if dist < min_dist:
                    min_dist = dist
                    position = i
                    if min_dist == 0:
                        break

            if min_dist <= 3*distance:
                sequence = subsequences[position]
                subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
                                if len(sequence[x:y]) >= min_length]

                for i, subsequence in enumerate(subsequences):
                    dist = Levenshtein.distance(subsequence, primer)
                    if dist <= min_dist and dist <= distance:
                        min_dist = dist
                        position = i
                        if min_dist == 0:
                            break

                if position >= 0:
                    print(subsequences[position])
