from seq1 import Seq

print("-----| Practice 1, Exercise 1 |------")

my_seq = Seq("ACTGA")

if my_seq.valid_sequence():
    print("Sequence 1: (Length:", str(my_seq.len()) + ")", str(my_seq))
else:
    print("ERROR")