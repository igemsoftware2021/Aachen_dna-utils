from bitstring import *
from pathlib import Path
from pyfaidx import Fasta, Sequence

class DNACoder:
    def __init__(self, byte_length: int, tryte_length: int):
        self.byte_length = byte_length
        self.tryte_length = tryte_length
        self.bitstring = None
        self.dna_string = None

    def read_file(self, filepath: Path):
        file = open(filepath)
        self.bitstring = Bits(file)
        file.close()

    def write_file(self, filepath: Path):
        write_file = open(filepath, 'wb')
        Bits(f'0b{self.bitstring}').tofile(write_file)
        write_file.close()

    def read_dna_file(self, filepath: Path):
        # file = open(filepath)
        # self.dna_string = file.read()
        # file.close()
        file = Fasta(filepath.__str__())
        self.dna_string = file[0].__str__()
        file.close()

    def write_dna_file(self, filepath: Path):
        write_file = open(filepath, "w")
        title = ">dna sequence for encoding information, iGEM Aachen 2021"
        write_file.write(title + "\n")

        chunk_size = 80
        dna_chunks = [self.dna_string[i:i+chunk_size] for i in range(0, len(self.dna_string), chunk_size)]
        print(dna_chunks)
        write_file.writelines(chunk + "\n" for chunk in dna_chunks)
        write_file.close()

    def encode(self):
        tryte_string = ''

        for i in range(0, len(self.bitstring) - 1, self.byte_length):
            slice = self.bitstring[i:i + self.byte_length].uint

            tryte = self.byte_to_tryte(slice, self.tryte_length)
            tryte_string += tryte

        DNA_string = self.tryte_to_dna(tryte_string)

        self.dna_string = DNA_string

    def decode(self):
        if not self.dna_string:
            return "There is no dna string to decode"

        decoded_trit_string = self.dna_to_tryte(self.dna_string)

        decoded_bitstring = ''
        for i in range(0, len(decoded_trit_string) - 1, self.tryte_length):
            slice = decoded_trit_string[i: i + self.tryte_length]

            byte = self.tryte_to_byte(slice, self.byte_length)

            decoded_bitstring += byte.bin

        self.bitstring = decoded_bitstring

    base_map = {('A', '0'): 'G',
                ('A', '1'): 'T',
                ('A', '2'): 'C',
                ('C', '0'): 'T',
                ('C', '1'): 'G',
                ('C', '2'): 'A',
                ('G', '0'): 'A',
                ('G', '1'): 'C',
                ('G', '2'): 'T',
                ('T', '0'): 'C',
                ('T', '1'): 'A',
                ('T', '2'): 'G'}

    tryte_map = {('A', 'G'): '0',
                 ('A', 'T'): '1',
                 ('A', 'C'): '2',
                 ('C', 'T'): '0',
                 ('C', 'G'): '1',
                 ('C', 'A'): '2',
                 ('G', 'A'): '0',
                 ('G', 'C'): '1',
                 ('G', 'T'): '2',
                 ('T', 'C'): '0',
                 ('T', 'A'): '1',
                 ('T', 'G'): '2'}

    def byte_to_tryte(self, byte, tryte_length):
        print(byte)
        tryte = ''

        for j in range(0, tryte_length):
            byte, trit = divmod(byte, 3)
            tryte = str(trit) + tryte

        return tryte

    def tryte_to_byte(self, tryte, byte_length):
        byte = 0

        for j in range(1, len(tryte)+1):
            trit = int(tryte[-j])
            byte += trit * pow(3, j-1)

        return Bits(uint=byte, length=byte_length)

    def tryte_to_dna(self, tryte: str):
        dna = 'A'
        for j in range(0, len(tryte)):
            trit = tryte[j]
            dna += self.next_base(dna[-1], trit)
        return dna

    def next_base(self, current_base: str, trit: str):
        return self.base_map[(current_base, trit)]

    def dna_to_tryte(self, dna: str):
        tryte_string = ''
        for j in range(0, len(dna)-1):
            base1 = dna[j]
            base2 = dna[j+1]
            tryte_string += self.next_tryte(base1, base2)
        return tryte_string

    def next_tryte(self, first_base: str, second_base: str):
        return self.tryte_map[(first_base, second_base)]

    def save_to_file(self, string: str, filename):
        file = open(f'generated_files/{filename}', 'w')
        file.write(string)
        file.close()

#
# def byte_to_DNA_to_byte():
#     byte_length = 8
#     tryte_length = 6
#     file_name = "igem_aachen"
#     file_ending = 'txt'
#
#     file = open(f"original_files/{file_name}.{file_ending}")
#
#     bitstring = Bits(file)
#
#     tryte_string = ''
#
#     for i in range(0, len(bitstring) - 1, byte_length):
#         slice = bitstring[i:i + byte_length].uint
#
#         tryte = byte_to_tryte(slice, tryte_length)
#         tryte_string += tryte
#
#     DNA_string = tryte_to_dna(tryte_string)
#
#     save_to_file(DNA_string, file_name)
#
#     decoded_trit_string = dna_to_tryte(DNA_string)
#
#     decoded_bitstring = ''
#     for i in range(0, len(decoded_trit_string) - 1, tryte_length):
#         slice = decoded_trit_string[i: i + tryte_length]
#
#         byte = tryte_to_byte(slice, byte_length)
#
#         decoded_bitstring += byte.bin
#
#     write_file = open(f"generated_files/{file_name}_{byte_length}_{tryte_length}.{file_ending}", 'wb')
#     Bits(f'0b{decoded_bitstring}').tofile(write_file)
