"""
usage:
    dna_utils.py encode --input <input> --output <output>
    dna_utils.py decode --input <input> --output <output>

"""

from dna_coder import *
from docopt import docopt

def encode(args):
    input = Path(args["<input>"])
    output = Path(args["<output>"])

    coder = DNACoder(byte_length=8, tryte_length=6)
    coder.read_file(input)
    coder.encode()
    coder.write_dna_file(output)


def decode(args):
    input = Path(args["<input>"])
    output = Path(args["<output>"])

    secondCoder = DNACoder(byte_length=8, tryte_length=6)
    secondCoder.read_dna_file(input)
    secondCoder.decode()
    secondCoder.write_file(output)

if __name__ == '__main__':
    args = docopt(__doc__, version='0.0.1')

    if args['encode']:
        encode(args)
    if args['decode']:
        decode(args)
