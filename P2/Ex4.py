from server_class import Client
from seq1 import Seq

print(f"-----| Practice 2, Exercise 1 |------")

IP = "127.0.0.1"
PORT = 21000

s = Seq()
f = "../P0/DNA_SEQ/FRAT1"
s.read_fasta(f)

c = Client(IP, PORT)
print(c)

gene = f.split("/")[3]

c.talk(f"Sending {gene} to the server...")

print(f"Sending {gene} to the server...")
response = c.talk(str(s))
print(f"Response:\n {response}")