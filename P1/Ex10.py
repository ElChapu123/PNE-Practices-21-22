from seq1 import Seq

print("-----| Practice 1, Exercise 10 |------")

files = ["../P0/DNA_SEQ/U5", "../P0/DNA_SEQ/ADA", "../P0/DNA_SEQ/FRAT1", "../P0/DNA_SEQ/FXN", "../P0/DNA_SEQ/U5"]

for f in files:
    try:
        s1 = Seq()
        seq = s1.read_fasta(f)
        print("Gene", f.split("/")[3] + ":", "Most frequent Base:", s1.most_common_base())
    except FileNotFoundError:
        print("File not found")