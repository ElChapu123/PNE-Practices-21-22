def fibbonacci(n):
    if n > 1:
        seq = [0,1]
        for i in range(n - 2):
            seq.append(seq[-1] + seq[-2])
        return seq
    else:
        return [0]

def fibosum(n):
    total = fibbonacci(n)
    return sum(total)

print("Sum of the first 5 terms of fibbonacci sequence:", fibosum(5))
print("Sum of the first 10 terms of fibbonacci sequence:", fibosum(10))