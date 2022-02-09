def seq_ping():
    print("Ok")

def read_seq_fasta(seq):
    seq = seq[seq.find("\n") + 1:]
    seq = seq.replace("\n", "")
    return seq[:20]

def seq_len(seq):
    seq = seq[seq.find("\n") + 1:]
    seq = seq.replace("\n", "")
    return len(seq)

def seq_count_base(seq, b):
    seq = seq[seq.find("\n") + 1:]
    seq = seq.replace("\n", "")
    count = 0

    for e in seq:
        if e == b:
            count += 1

    return count

def seq_count(seq):
    seq = seq[seq.find("\n") + 1:]
    seq = seq.replace("\n", "")
    count_bases = {"A": 0, "C": 0, "G": 0, "T": 0}
    for e in seq:
        count_bases[e] += 1

    return count_bases

def seq_reverse(seq):
    new_seq = ""
    for e in seq:
        new_seq = e + new_seq

    return new_seq

def seq_complement(seq):
    complement_dict = {"A": "C", "C": "A", "T": "G", "G": "T"}
    new_seq = ""

    for e in seq:
        for b in complement_dict:
            if e == b:
                new_seq += complement_dict[b]

    return new_seq

def most_common_base(seq):
    count_dict = seq_count(seq)
    most_common = ""
    for b in count_dict:
        if most_common == "":
            most_common = b
        elif int(count_dict[b]) > count_dict[most_common]:
            most_common = b

    return most_common