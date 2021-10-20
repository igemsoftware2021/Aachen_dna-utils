# DNA_Coder

A tool to encode Data in DNA.

# Installation
Clone this repository and install pipenv first. Then:
```
pipenv install
```

# Usage

## To Encode a File

`dna_utils.py encode --input <input> --output <output>`

## To Correct a File
`dna_utils.py correct --input <input> --output <output> --config <config>`

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

`python dna_utils.py correct --input original_files/BC23_small.fastq --output generated_files/BC23_corrected.fasta --config example_config.yaml`

## To Decode a File
`dna_utils.py decode --input <input> --output <output>`
