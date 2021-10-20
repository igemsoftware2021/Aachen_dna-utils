"""
usage:
    dna_utils.py encode --input <input> --output <output>
    dna_utils.py decode --input <input> --output <output>
    dna_utils.py correct --input <input> --output <output> --config <config>

"""

from dna_coder import *
from error_corrector import *
from docopt import docopt
import yaml

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

    coder = DNACoder(byte_length=8, tryte_length=6)
    coder.read_dna_file(input)
    coder.decode()
    coder.write_file(output)

def correct(args):
    input_path = Path(args["<input>"])
    output_path = Path(args["<output>"])
    config_path = Path(args["<config>"])

    config = yaml.safe_load(open(config_path))

    corrector = ErrorCorrector(input_path)

    print(str(len(corrector.fastq.reads)) + " reads found.")
    print("Remove primer now.")

    primer = config["primer"]["sequence"]
    primer_dist = config["primer"]["max_distance"]

    reverse_primer = config["reverse_primer"]["sequence"]
    reverse_primer_dist = config["reverse_primer"]["max_distance"]

    support = config["support"]

    corrector.remove_subsequence(
        primer=primer,
        distance=primer_dist,
        remove_other=True,
        remove_before=True,
        remove_after=False,
    )

    print("Primer removed, " + str(len(corrector.fastq.reads)) + " reads left.")
    print("Remove reverse primer now.")

    corrector.remove_subsequence(
        primer=reverse_primer,
        distance=reverse_primer_dist,
        remove_other=True,
        remove_before=False,
        remove_after=True,
    )

    print("Reverse primer removed, " + str(len(corrector.fastq.reads)) + " reads left.")

    print("Merge sequences now.")

    merged_sequence = corrector.merge_reads(support)

    print("Sequences merged, write to output file now.")

    write_fasta(
        filepath=output_path,
        description="Error-corrected DNA sequence, dna_utils",
        sequence=merged_sequence
    )

    print("Done.")

def write_fasta(filepath: Path, description: str, sequence: str):
    write_file = open(filepath, "w")
    write_file.write(description + "\n")

    chunk_size = 80
    dna_chunks = [sequence[i:i+chunk_size] for i in range(0, len(sequence), chunk_size)]
    write_file.writelines(chunk + "\n" for chunk in dna_chunks)
    write_file.close()

if __name__ == '__main__':
    args = docopt(__doc__, version='0.0.1')

    if args['encode']:
        encode(args)
    if args['decode']:
        decode(args)
    if args['correct']:
        correct(args)
