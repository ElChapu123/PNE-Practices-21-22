import seq0
from pathlib import Path

print("-----| Exercise 6 |-----")

file = "./DNA_SEQ/U5"

seq = Path(file).read_text()
seq_20 = seq0.read_seq_fasta(seq)

print("Gene", file.split("/")[-1] + ":")
print("Frag:", seq_20)
print("Rev:", seq0.seq_reverse(seq_20))