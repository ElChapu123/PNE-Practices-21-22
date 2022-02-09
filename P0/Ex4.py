import seq0
from pathlib import Path
print("-----| Exercise 4 |-----")
files = ["./DNA_SEQ/U5", "./DNA_SEQ/ADA", "./DNA_SEQ/FRAT1", "./DNA_SEQ/FXN"]

for f in files:
    seq = Path(f).read_text()
    bases = ["A", "T", "C", "G"]
    print("Gene", f.split("/")[2] + ":")

    for b in bases:
        print(" " + b + ":", seq0.seq_count_base(seq, b))

    print()
