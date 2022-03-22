import socket
from seq1 import Seq
from colorama import Fore
try:
    #SERVER CONFIGURATION

    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    PORT = 21000
    IP = "127.0.0.1"

    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind((IP, PORT))
    ls.listen()

    print(Fore.LIGHTWHITE_EX + "The server is configured!")

    #OTHER INFO
    seq_list = ["ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA","AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA","CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT","CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA","AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"]



    #SERVER MAIN LOOP

    while True:
        print("Waiting for Clients to connect")
        (cs, client_ip_port) = ls.accept()

        print("A client has connected to the server!")

        msg_raw = cs.recv(2048)

        msg = msg_raw.decode()

        msg_split = msg.split()
        cmd = msg_split[0]

        if len(msg_split) > 1:
            arg = msg_split[1]

        print(Fore.GREEN + f"{cmd}" +  Fore.LIGHTWHITE_EX)
        if cmd == "PING":
            response = "OK!\n"

        elif cmd == "GET":
            try:
                response = seq_list[int(arg)] + "\n"
            except IndexError:
                response = "Please enter a value between 0 and 4\n"

        elif cmd == "INFO":
            new_seq = Seq(arg)
            n_bases = new_seq.bases()
            percentages = new_seq.base_percentage()
            seq_len = new_seq.len()

            response = "Sequence: " + arg

            response = response + "\nTotal lenght: " + str(seq_len) + "\n"

            for k in percentages:
                response = response + str(k) + ": " + str(n_bases[k]) + " (" + str(percentages[k]) + "%)\n"
                response = response

        elif cmd == "COMP":
            response = Seq(arg).seq_complement() + "\n"

        elif cmd == "REV":
            response = Seq(arg).seq_reverse() + "\n"

        elif cmd == "GENE":
            try:
                filename = "../P0/DNA_SEQ/" + arg
                print(filename)
                response = Seq()
                response.read_fasta(filename)
                response = str(response)

            except FileNotFoundError:
                response = "File not found\n"

        else:
            response = "Command not available in this server\n"

        print(response)

        cs.send(response.encode())

        cs.close()
except KeyboardInterrupt:
    print("Server closed")