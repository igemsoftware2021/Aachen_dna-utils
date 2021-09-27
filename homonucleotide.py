from read import Read

class Homonucleotide():
    def __init__(self, read: Read):
        self.nucleotide = read.seq[0]
        self.length = len(read.seq)
        self.quality = 0

    def __str__(self):
        return "Nucleotide: " + self.nucleotide + ", Length: " + str(self.length) + ", Quality: " + str(self.quality)

class Homonucleotides():
    def __init__(self, read: Read):
        self.homonucleotides = []
        prev = ""  # read.seq[0]
        length = 0
        for i, base in enumerate(read.seq):
            if base == prev:
                length += 1
            else:
                if not length == 0:
                    self.homonucleotides.append(Homonucleotide(Read(
                        description=read.description,
                        seq=read.seq[i-length:i],
                        qual=read.qual[i-length:i]
                    )))
                length = 1
                prev = base

    def __iter__(self):
        return iter(self.homonucleotides)
