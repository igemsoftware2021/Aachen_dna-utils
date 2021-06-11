from dna_coder import *

if __name__ == '__main__':
    secondCoder = DNACoder(byte_length=8, tryte_length=6)
    secondCoder.read_dna_file("igem_aachen.dna")
    secondCoder.decode()
    secondCoder.write_file("igema_aachen.txt")
