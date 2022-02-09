import seq0
from pathlib import Path

print("-----| Exercise 7 |-----")


file = "./DNA_SEQ/U5"

seq = Path(file).read_text()
seq_20 = seq0.read_seq_fasta(seq)

print("Gene", file.split("/")[-1] + ":")
print("Frag:", seq_20)
print("Comp:", seq0.seq_complement(seq_20))