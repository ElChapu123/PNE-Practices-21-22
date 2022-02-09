def fibbonacci(n):
    if n > 1:
        seq = [0,1]
        for i in range(n - 2):
            seq.append(seq[-1] + seq[-2])
        return seq
    else:
        return [0]


def fibbonacci_n(n):
    seq = fibbonacci(n)
    return seq[-1]

print("The 1st number of fibbonnacci sequence is", fibbonacci_n(5))
print("The 11th number of fibbonnacci sequence is", fibbonacci_n(11))
print("The 55th number of fibbonnacci sequence is", fibbonacci_n(55))

