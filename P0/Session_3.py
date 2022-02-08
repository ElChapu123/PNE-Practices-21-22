#EXERCISE 1
print("Exercise 1")
def g(a, b):
    return a - b

#Zero Division Error when t1 = 0. We can fix it using try and exceot
def f(a, b, c, d):
    t0 = a + b - g(a, 0)
    t1 = g(c, d)
    try:
        t3 = 2 * (t0 / t1)
        return t0 + 2*t1 + t3*t3
    except ZeroDivisionError:
        return "Error"

# -- Main program
print("Result 1: ", f(5, 2, 5, 0))
print("Result 2: ", f(0, 2, 3, 3))
print("Result 3: ", f(1, 3, 2, 3))
print("Result 4: ", f(1, 9, 22.0, 3))

print("\nExercise 2")

#EXERCISE 2:
def get_dna_seq():
    exit = False

    while not exit:
        correct = True
        seq = input("Enter a DNA sequence: ")
        for e in set(seq):
            if e != "A" and e != "G" and e != "C" and e != "T":
                correct = False
        if correct:
            exit = True
        else:
            print("Please enter a valid sequence.")

    return seq

def count_dna_bases(seq):
    count_bases = {"A": 0, "C": 0, "G": 0, "T": 0}

    for e in seq:
        count_bases[e] += 1

    return count_bases

seq = get_dna_seq()
count_dict = count_dna_bases(seq)
for k in count_dict:
    print(k + ":", count_dict[k])

print("\nExercise 3")

#Exercise 3
f = open("dna_seq", "r")
seq_list = f.readlines()

for e in seq_list:
    count_dict = count_dna_bases(e[:-1])
    print("Total length:", len(e) - 1)
    for k in count_dict:
        print(k + ":", count_dict[k])
    print()