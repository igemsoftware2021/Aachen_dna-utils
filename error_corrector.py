from pyfaidx import Fasta
from pyfastx import Fastq, Sequence
from pathlib import Path
from fastq import FastQ

class ErrorCorrector:
    def __init__(self, filepath: Path):
        self.fastq = FastQ(Fastq(filepath.__str__()))

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
