from seq1 import Seq

print("-----| Practice 1, Exercise 7 |------")

s1 = Seq()
s2 = Seq("ACTTG")
s3 = Seq("ACXG")

b1 = s1.bases()
b2 = s2.bases()
b3 = s3.bases()

print("Sequence 1: (Lenght:", str(s1.len()) + ")", s1)
print("  Bases:", b1)
print("  Rev:", s1.seq_reverse())
print("  Com:", s1.seq_complement())

print("Sequence 2: (Lenght:", str(s2.len()) + ")", s2)
print("  Bases:", b2)
print("  Rev:",s2.seq_reverse())
print("  Com:", s2.seq_complement())

print("Sequence 3: (Lenght:", str(s3.len()) + ")", s3)
print("  Bases:", b3)
print("  Rev:", s3.seq_reverse())
print("  Com:", s3.seq_complement())
