import bitstring
from error_corrector import *
from dna_coder import *

bitstring.BitString

# corrector2 = ErrorCorrector(Path("original_files/BC24.fastq"))
# primer = "ACAATTCATCTTAGTGCCAGACTACTGTACTGTCCCAGAGAATAGACTTGCTTCGTGCGCACCCGTATGCCGCTCGATATGCGTAGCCGTCCATGTTGAT"
# corrector2.remove_subsequence(primer=primer, distance=5, remove_other=True, remove_before=True, remove_after=False)
#
# endsequence = "TACCA"
# corrector2.remove_subsequence(primer=endsequence, distance=2, remove_other=True, remove_before=False, remove_after=True)
#
# corrector2.write(Path("generated_files/BC24_corrected.fastq"))

corrector2 = ErrorCorrector(Path("generated_files/BC24_corrected.fastq"))

print(corrector2.merge_reads())
