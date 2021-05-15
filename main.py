from bitstring import *

base_map = {('A', '0'): 'C',
            ('A', '1'): 'G',
            ('A', '2'): 'T',
            ('C', '0'): 'G',
            ('C', '1'): 'T',
            ('C', '2'): 'A',
            ('G', '0'): 'T',
            ('G', '1'): 'A',
            ('G', '2'): 'C',
            ('T', '0'): 'A',
            ('T', '1'): 'C',
            ('T', '2'): 'G'}

tryte_map = {('A', 'C'): '0',
             ('A', 'G'): '1',
             ('A', 'T'): '2',
             ('C', 'G'): '0',
             ('C', 'T'): '1',
             ('C', 'A'): '2',
             ('G', 'T'): '0',
             ('G', 'A'): '1',
             ('G', 'C'): '2',
             ('T', 'A'): '0',
             ('T', 'C'): '1',
             ('T', 'G'): '2'}


def byte_to_tryte(byte, tryte_length):
    tryte = ''
    print(byte)

    for j in range(0, tryte_length):
        byte, trit = divmod(byte, 3)
        tryte = str(trit) + tryte

    return tryte


def tryte_to_byte(tryte, byte_length):
    byte = 0

    for j in range(1, len(tryte)+1):
        trit = int(tryte[-j])
        byte += trit * pow(3, j-1)

    return Bits(uint=byte, length=byte_length)


def tryte_to_dna(tryte: str):
    dna = 'A'
    for j in range(0, len(tryte)):
        trit = tryte[j]
        dna += next_base(dna[-1], trit)
    return dna


def next_base(current_base: str, trit: str):
    return base_map[(current_base, trit)]


def dna_to_tryte(dna: str):
    tryte_string = ''
    for j in range(0, len(dna)-1):
        base1 = dna[j]
        base2 = dna[j+1]
        tryte_string += next_tryte(base1, base2)
    return tryte_string


def next_tryte(first_base: str, second_base: str):
    return tryte_map[(first_base, second_base)]


if __name__ == '__main__':

    byte_length = 8
    tryte_length = 6
    file_name = "DNA_raw.svg"

    file = open(f"original_files/{file_name}")

    bitstring = Bits(file)

    tryte_string = ''

    for i in range(0, len(bitstring)-1, byte_length):
        slice = bitstring[i:i + byte_length].int

        tryte = byte_to_tryte(slice, tryte_length)
        tryte_string += tryte

    DNA_string = tryte_to_dna(tryte_string)

    decoded_trit_string = dna_to_tryte(DNA_string)

    decoded_bitstring = ''
    for i in range(0, len(decoded_trit_string)-1, tryte_length):
        slice = decoded_trit_string[i: i + tryte_length]

        byte = tryte_to_byte(slice, byte_length)

        decoded_bitstring += byte.bin

    write_file = open(f"generated_files/{file_name}", 'wb')
    Bits(f'0b{decoded_bitstring}').tofile(write_file)
