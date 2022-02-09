import seq0
from pathlib import Path
print("-----| Exercise 4 |-----")
files = ["./DNA_SEQ/U5", "./DNA_SEQ/ADA", "./DNA_SEQ/FRAT1", "./DNA_SEQ/FXN", "./DNA_SEQ/U5"]

for f in files:
    seq = Path(f).read_text()
    bases = seq0.seq_count(seq)

    print("Gene", f.split("/")[2] + ":", bases)
