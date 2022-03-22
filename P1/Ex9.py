from seq1 import Seq

print("-----| Practice 1, Exercise 9 |------")
try:
    s1 = Seq()

    s1.read_fasta("../P0/DNA_SEQ/U5")

    b1 = s1.bases()

    print("Sequence 1: (Lenght:", str(s1.len()) + ")", str(s1)[44], "...(not shown)...")
    print("  Bases:", b1)
    print("  Rev:", s1.seq_reverse()[:44], "...(not shown)...")
    print("  Com:", s1.seq_complement()[:44], "...(not shown)...")
except FileNotFoundError:
    print("File not found")