![dna_four_colors](https://user-images.githubusercontent.com/44715237/138370519-df86295f-6074-44ae-a577-572d7c8b625b.png)
# DNA Utils


A tool to encode Data in DNA.
From the 2021 iGEM Team Aachen.

It encodes bytes into 6-trit trytes.
Then it encodes this sequence of trytes in to a string of bases in the following way:

We encode only the transitions between bases, so Homonucleotides don't matter for the encoding.

As A and G are both purin bases and C and T are pyrimidinbases and A/T, C/G are both compatible.
There are certain groups between the different bases.
There is no "group change" between C/T, A/G so it is a 0.
From A/T, G/C there is one group change so its a 1.
From A/C, G/T there are two changes so its a 2.



```
A --0-- G
| \   / |
1   2   1
| /   \ |
T --0-- C
```

# Installation
Clone this repository and install pipenv first. Then:
```
pipenv install
pipenv shell
```

# Usage

This tool knows three commands: `encode`, `correct`, and `decode`.
They are described in more detail below.
If you want to learn more about how the DNA Utils work, visit the [iGEM Aachen 2021 wiki](2021.igem.org/Team:Aachen/Software).
In the folder `assets`, example files are provided that you can use to test the different commands.

## To Encode a File

`python dna_utils.py encode --input <input> --output <output>`

This command takes an arbitrary file as input and generates a file in the `fasta` format as output.
The details about the encoding are described above.

### Example

This command takes a text file and encodes it into DNA.

`python dna_utils.py encode --input assets/example.txt --output assets/example.fasta`

## To Correct a File

`python dna_utils.py correct --input <input> --output <output> --config <config>`

This command takes a `fastq` file as input and generates a `fasta` file with a single DNA sequence as output.
It also takes a `yaml` file with additional parameters.

The command does the following:

- Scan all sequences for the given primer.
  - If the primer is in the sequence, remove the primer and everything before it.
  - If the primer is not found, remove the sequence from the file.
- Scan all sequences for the given reverse primer.
  - If the reverse primer is in the sequence, remove it and everything behind it.
  - If it is not found, remove the sequence.
- Compare all remaining sequences and "merge" them, meaning that the tool creates one sequence that represents the average of all sequences.

The config file should look something like this:

```buildoutcfg
primer:
  sequence: ACAATTCAT...TCCATGTTGAT
  max_distance: 7
reverse_primer:
  sequence: TACCA
  max_distance: 2
support: 70
```

For primer and reverse_primer, `max_distance` is the error with which a subsequence is still recognized as the primer.
Technically, the Levenshtein distance is used for this.
It describes how many insertions, deletions and substitutions need to be made to match two given strings.

The parameter `support` is used for the merging step.
It determines how long the merged sequence should be.
To do so, the tool first compares the lengths of all sequences.
It then sets teh length to the minimum that `support`% of the sequences have.

### Example

This command takes an actual file generated with nanopore sequencing, removes its primers and merges the remaining sequences to recreate the original sequence.

`python dna_utils.py correct --input assets/example_sequence.fastq --output assets/example_corrected.fasta --config assets/example_config.yaml`

## To Decode a File

`python dna_utils.py decode --input <input> --output <output>`

This command is the counterpart to the `encode` command.
It takes a `fasta` file as input and generates and arbitrary file.

### Example

To execute this, first execute the example command to encode a file.
This command takes the output from the encode command and recreates the original textfile from it.

`python dna_utils.py decode --input assets/example.fasta --output assets/example_decoded.txt`
