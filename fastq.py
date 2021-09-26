from pyfastx import Fastq
from pathlib import Path

class Read():
    def __init__(self, description: str, seq: str, qual: str):
        self.description = description
        self.seq = seq
        self.qual = qual

class FastQ():
    def __init__(self, fastq: Fastq):
        self.reads = []
        for read in fastq:
            self.reads.append(Read(read.description, read.seq, read.qual))

    def __iter__(self):
        return iter(self.reads)

    def __getitem__(self, item):
        return self.reads[item]

    def write(self, path: Path):
        file = open(path, 'w')
        for read in self.reads:
            file.write(read.description + "\n")
            file.write(read.seq + "\n")
            file.write("+\n")
            file.write(read.qual + "\n")

