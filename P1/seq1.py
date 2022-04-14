from pathlib import Path
class Seq:
    def __init__(self, strbases = "NULL"):
        # Initialize the sequence with the value
        # passed as argument when creating the object
        self.strbases = strbases
        if strbases == "NULL":
            print("NULL sequence created!")
        elif not self.valid_sequence():
            print("INVALID Seq!")
            self.strbases = "ERROR"
        else:
            print("New sequence created!")

    def valid_sequence(self):
        valid = True
        i = 0
        bases = ["A", "C", "G", "T"]
        while i < len(self.strbases) and valid:
            c = self.strbases[i]
            if c not in bases:
                valid = False
            i += 1
        return valid

    def __str__(self):
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        else:
            return len(self.strbases)

    def count_base(self, base):
        count = 0
        if self.strbases == "NULL" or self.strbases == "ERROR":
            pass
        else:
            for e in self.strbases:
                if e == base:
                    count += 1
        return count

    def bases(self):
        count_bases = {"A": 0, "C": 0, "G": 0, "T": 0}

        if self.strbases == "NULL" or self.strbases == "ERROR":
            pass
        else:
            for e in self.strbases:
                count_bases[e] += 1

        return count_bases

    def seq_reverse(self):
        new_seq = ""
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            for e in self.strbases:
                new_seq = e + new_seq
            return new_seq

    def seq_complement(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        else:
            complement_dict = {"A": "C", "C": "A", "T": "G", "G": "T"}
            new_seq = ""

            for e in self.strbases:
                for b in complement_dict:
                    if e == b:
                        new_seq += complement_dict[b]

            return new_seq

    def read_fasta(self, filename):
        seq = Path(filename).read_text()
        seq = seq[seq.find("\n") + 1:]
        seq = seq.replace("\n", "")

        self.strbases = seq

    def most_common_base(self):
        count_dict = self.bases()
        most_common = ""
        for b in count_dict:
            if most_common == "":
                most_common = b
            elif int(count_dict[b]) > count_dict[most_common]:
                most_common = b

        return most_common

    def base_percentage(self):
        base_dict = self.bases()
        t_lenght = len(self.strbases)
        for k in base_dict:
            base_dict[k] = round(base_dict[k] / t_lenght * 100, 2)

        return base_dict

    def format_txt(self):
        i = 0
        new_seq = ""
        for e in self.strbases:
            new_seq += e
            i += 1
            if i == 50:
                new_seq += "\n"
                i = 0

        return new_seq