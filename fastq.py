from pyfastx import Fastq
from pathlib import Path
from read import Read
from homonucleotide import Homonucleotide, Homonucleotides

class FastQ():
    def __init__(self, path: Path):
        file = open(path)
        length = len(file.readlines())
        file.close()
        file = open(path)
        self.reads = []
        self.homo_reads = []
        for i in range(0, length, 4):
            description = file.readline()
            sequence = file.readline()
            _ = file.readline()
            quality = file.readline()
            self.read = Read(description, sequence, quality)
            self.homo_reads.append(Homonucleotides(self.read))
        file.close()

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

