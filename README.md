# DNA_Coder

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
```


# Usage

## To Encode a File

`dna_utils.py encode --input <input> --output <output>`

## To Decode a File
`dna_utils.py decode --input <input> --output <output>`

## To Correct a File
`dna_utils.py correct --input <input> --output <output>`
