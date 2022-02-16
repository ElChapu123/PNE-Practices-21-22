from seq1 import Seq

print("-----| Practice 1, Exercise 5 |------")

s1 = Seq()
s2 = Seq("ACTTG")
s3 = Seq("ACXG")

bases = ["A", "C", "T", "G"]

print("Sequence 1: (Lenght:", str(s1.len()) + ")", s1)
for b in bases:
    print(b + ":", s1.count_base(b), end= ", ")
print()

print("Sequence 2: (Lenght:", str(s2.len()) + ")", s2)
for b in bases:
    print(b + ":", s2.count_base(b), end= ", ")
print()

print("Sequence 3: (Lenght:", str(s3.len()) + ")", s3)
for b in bases:
    print(b + ":", s3.count_base(b), end= ", ")
print()