import seq0
from pathlib import Path
print("-----| Exercise 3 |-----")
files = ["./DNA_SEQ/U5", "./DNA_SEQ/ADA", "./DNA_SEQ/FRAT1", "./DNA_SEQ/FXN"]

for f in files:
    seq = Path(f).read_text()
    lenght = seq0.seq_len(seq)
    print("Gene", f.split("/")[2], "----> Lenght:", lenght )
