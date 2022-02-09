import seq0
from pathlib import Path


file = "./DNA_SEQ/U5"

seq = Path(file).read_text()
print("Gene"), file.split("/")[-1]
print("Frag:" + seq0.read_seq_fasta(seq))
print("Rev:", seq0.seq_reverse(seq))