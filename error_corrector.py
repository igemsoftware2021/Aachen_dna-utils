from pathlib import Path
from fastq import FastQ
from itertools import combinations
import Levenshtein
import statistics
import numpy as np

class ErrorCorrector:
    def __init__(self, filepath: Path):
        self.fastq = FastQ(filepath)

    def write(self, path: Path):
        self.fastq.write(path)

    def remove_homonucleotides(self):
        print(len(self.fastq.reads))
        for i, read in enumerate(self.fastq):
            new_seq = ""
            prev = ""
            for base in read.seq:
                if not base == prev:
                    prev = base
                    new_seq += base
            self.fastq[i].seq = new_seq

    def remove_subsequence(self, primer: str, distance: int, remove_other: bool, remove_before: bool,
                           remove_after: bool):

        iter_new = 0
        new_reads = []
        max_length = len(primer) + distance
        min_length = len(primer) - distance
        for read_iter, read in enumerate(self.fastq):
            sequence = read.seq
            # subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
            #                 if len(sequence[x:y]) == max_length]

            subsequences = [sequence[x:y] for x, y in combinations(range(len(sequence) + 1), r=2)
                            if min_length <= len(sequence[x:y]) <= max_length]

            min_found_dist = max_length
            subsequence_position = -1
            for subsequence_iter, subsequence in enumerate(subsequences):
                found_dist = Levenshtein.distance(subsequence, primer)
                if found_dist < min_found_dist:
                    subsequence_position = subsequence_iter
                    min_found_dist = found_dist
                    if min_found_dist == 0:
                        break

            if subsequence_position >= 0 and min_found_dist <= distance:
                # Subsequence found, remove it
                iter_new += 1
                new_seq = ""
                print(subsequences[subsequence_position])
                subsequence_start = sequence.find(subsequences[subsequence_position])
                subsequence_length = len(subsequences[subsequence_position])
                if remove_before:
                    first_base_behind = subsequence_start + subsequence_length
                    new_seq = self.fastq.reads[read_iter].seq[first_base_behind:]
                elif remove_after:
                    new_seq = self.fastq.reads[read_iter].seq[:subsequence_start] + "\n"
                else:
                    first_base_behind = subsequence_start + subsequence_length
                    new_seq = self.fastq.reads[read_iter].seq[:subsequence_start] \
                                                      + self.fastq.reads[read_iter].seq[first_base_behind:]

                new_read = read
                new_read.seq = new_seq
                new_reads.append(new_read)

            else:
                # Subsequence not found, remove whole sequence
                if remove_other:
                    pass
                    # self.fastq.reads.remove(read)
                else:
                    new_reads.append(read)

        self.fastq.reads = new_reads

    def merge_reads(self, support: int):
        lengths = np.fromiter((len(x) for x in self.fastq.homo_reads), dtype=int)
        common_length = np.percentile(lengths, support)

        print("sequences left: " + str(len(self.fastq.reads)))

        last = ""
        sequence = ""

        for iter in range(int(common_length)):
            last = self.get_next_base(iter, last)
            sequence += last

        return sequence

    def get_next_base(self, number: int, last: str):
        quality_votes = {
            "A": 0,
            "C": 0,
            "G": 0,
            "T": 0
        }
        length_votes = {
            "A": 0,
            "C": 0,
            "G": 0,
            "T": 0
        }
        for read in self.fastq.homo_reads:
            if len(read.homonucleotides) > number:
                next = read.homonucleotides[number]
                if next.nucleotide == "A":
                    quality_votes["A"] += next.quality
                    length_votes["A"] += next.length
                elif next.nucleotide == "C":
                    quality_votes["C"] += next.quality
                    length_votes["C"] += next.length
                elif next.nucleotide == "G":
                    quality_votes["G"] += next.quality
                    length_votes["G"] += next.length
                elif next.nucleotide == "T":
                    quality_votes["T"] += next.quality
                    length_votes["T"] += next.length


        max_length = length_votes.get(max(length_votes, key=length_votes.get))
        normed_length = {key: length_votes[key]/max_length for key in length_votes}

        max_quality = quality_votes.get(max(quality_votes, key=quality_votes.get))
        normed_quality = {key: quality_votes[key]/max_quality for key in quality_votes}

        normed_vote = {
            "A": (normed_quality.get("A") + normed_length.get("A")) / 2,
            "C": (normed_quality.get("C") + normed_length.get("C")) / 2,
            "G": (normed_quality.get("G") + normed_length.get("G")) / 2,
            "T": (normed_quality.get("T") + normed_length.get("T")) / 2
        }

        max_base = max(normed_vote, key=normed_vote.get)
        if max_base != last:
            return max_base
        else:
            normed_vote.pop(max_base)
            return max(normed_vote, key=normed_vote.get)
