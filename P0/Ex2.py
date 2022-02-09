import seq0
from pathlib import Path

file = input("Enter file name: ")
file = "./DNA_SEQ/" + file

seq = Path(file).read_text()
print("The first 20 bases are:\n" + seq0.read_seq_fasta(seq))
