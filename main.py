from dna_coder import *

if __name__ == '__main__':
    coder = DNACoder(byte_length=8, tryte_length=6)
    coder.read_file(Path("original_files/igem_aachen.txt"))
    coder.encode()
    coder.write_dna_file(Path("generated_files/igem_aachen.dna"))

    secondCoder = DNACoder(byte_length=8, tryte_length=6)
    secondCoder.read_dna_file(Path("generated_files/igem_aachen.dna"))
    secondCoder.decode()
    secondCoder.write_file(Path("original_files/ew_igem_aachen.txt"))
