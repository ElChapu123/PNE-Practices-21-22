from server_class import Client
from seq1 import Seq

print(f"-----| Practice 2, Exercise 1 |------")

IP = "10.3.41.189"
PORT = 20000

s = Seq()
f = "../P0/DNA_SEQ/FRAT1"
s.read_fasta(f)

gene = f.split("/")[3]
s_str = str(s)

c = Client(IP, PORT)
print(c)

print("Gene", gene + ":", str(s))

frag_dict = {1: "", 2: "", 3: "", 4: "", 5: ""}

for k in frag_dict:
    frag_dict[k] = s_str[:10]
    s_str = s_str[10:]

for k in frag_dict:
    print(f"Fragment {k}: {frag_dict[k]}")

c.talk(f"Sending {gene} Gene to the server, in fragments of 10 bases")

for k in frag_dict:
    c.talk(f"Fragment {k}: {frag_dict[k]}")