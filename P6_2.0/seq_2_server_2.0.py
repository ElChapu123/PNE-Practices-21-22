import http.server
import socketserver
import termcolor as t
from pathlib import Path
from seq1 import Seq
import jinja2 as j
from urllib.parse import urlparse, parse_qs

# Define the Server's port
PORT = 8080

HTML_FOLDER = "./html/"

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        print()

        seq_list = ["ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA","AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA","CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT","CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA","AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"]


        url_path = urlparse(self.path)
        path = url_path.path
        query = url_path.query

        cmd_dict = parse_qs(query)

        t.cprint(path, 'yellow')
        t.cprint(query, "green")
        t.cprint(cmd_dict, "blue")

        if self.path == "/":
            contents = read_html_file("index.html")\
                .render(context={"n_sequences": len(seq_list)})

        elif path == "/favicon.ico":
            contents = read_html_file("index.html")\
                .render(context={"n_sequences": len(seq_list)})

        elif path == "/ping":
            contents = read_html_file(path[1:] + ".html").render()

        elif path == "/get":
            n = int(cmd_dict["number"][0])
            seq = seq_list[int(cmd_dict["number"][0])]

            contents = read_html_file(path[1:] + ".html")\
                .render(context={"n":n, "seq":seq})

        elif path == "/gene":
            gene_name = cmd_dict["gene"][0]
            gene_seq = Seq()
            file = "../P0/DNA_SEQ/" + gene_name
            gene_seq.read_fasta(file)


            contents = read_html_file(path[1:] + ".html") \
                .render(context={"n":gene_name, "seq":gene_seq})

        elif path == "/operation":
            cmd = cmd_dict["operation"][0]
            arg = cmd_dict["seq"][0]

            if not Seq(arg).valid_sequence():
                contents = "Incorrect sequence, please enter a correct sequence"

            elif cmd == "INFO":
                new_seq = Seq(arg)
                n_bases = new_seq.bases()
                percentages = new_seq.base_percentage()
                seq_len = new_seq.len()

                contents = "Sequence: " + arg

                contents = contents + "\nTotal lenght: " + str(seq_len) + "\n"

                for k in percentages:
                    contents = contents + str(k) + ": " + str(n_bases[k]) + " (" + str(percentages[k]) + "%)\n"

            elif cmd == "COMP":
                contents = Seq(arg).seq_complement() + "\n"

            elif cmd == "REV":
                contents = Seq(arg).seq_reverse() + "\n"

            contents = contents.replace("\n", "<p><p>")

            contents = read_html_file(path[1:] + ".html") \
                .render(context={"op":cmd, "result":contents, "seq":arg})

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()