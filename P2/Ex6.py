from server_class import Client
from seq1 import Seq

print(f"-----| Practice 2, Exercise 1 |------")

IP = "127.0.0.1"
PORT = 21000
PORT2 = 20000

s = Seq()
f = "../P0/DNA_SEQ/FRAT1"
s.read_fasta(f)

gene = f.split("/")[3]
s_str = str(s)

c = Client(IP, PORT)
print(c)

c2 = Client(IP, PORT2)
print(c2)

print("Gene", gene + ":", str(s))

frag_dict = {}
for n in range(1,11):
    frag_dict[n] = ""


for k in frag_dict:
    frag_dict[k] = s_str[:10]
    s_str = s_str[10:]

for k in frag_dict:
    print(f"Fragment {k}: {frag_dict[k]}")

c.talk(f"Sending {gene} Gene to the server, in fragments of 10 bases")

for k in frag_dict:
    if k % 2 != 0:
        c.talk(f"Fragment {k}: {frag_dict[k]}")
    else:
        c2.talk(f"Fragment {k}: {frag_dict[k]}")
