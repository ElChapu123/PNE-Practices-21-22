#constant: Value that never changes. We use capital letters to denote them
N = 11

seq = [0,1]
for i in range(N - 2):
    seq.append(seq[-1] + seq[-2])

seq = str(seq)[1:-1].replace(",", "")
print(seq)

for e in seq:
    print(e, end= "")
print()

#This function does the same
def fibbonacci(n):
    seq = [0,1]
    for i in range(n - 2):
        seq.append(seq[-1] + seq[-2])
    return seq