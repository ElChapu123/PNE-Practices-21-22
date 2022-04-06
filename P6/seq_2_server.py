import http.server
import socketserver
import termcolor
from pathlib import Path
from seq1 import Seq

# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        seq_list = ["ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA","AAAAACATTAATCTGTGGCCTTTCTTTGCCATTTCCAACTCTGCCACCTCCATCGAACGA","CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCCTAATCTCCGTACAAAT","CCCTAGCCTGACTCCCTTTCCTTTCCATCCTCACCAGACGCCCGCATGCCGGACCTCAAA","AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"]

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        try:
            route = self.requestline.split(" ")[1]
            filename = route[1:]
            print("FILENAME", filename)
        except IndexError:
            route = "/"

        try:
            filename = filename.split("?")[1]
            filename = filename.split("&")

            cmd_dict = {}

            for e in filename:
                e = e.split("=")
                cmd_dict[e[0]] = e[1]
            print(cmd_dict)

        except IndexError:
            pass



        termcolor.cprint(filename, "blue")



        if route == "/":
            contents = Path("./html/index.html").read_text()
        elif route == "/favicon.ico":
            contents = Path("./html/index.html").read_text()

        elif route.startswith("/ping"):
            contents = Path("./html/PING.html").read_text()

        elif route.startswith("/get?"):
            n = int(cmd_dict["number"])
            seq = seq_list[int(cmd_dict["number"])]
            contents = Path("./html/GET.html").read_text().format(n=n, seq=seq)

        else:
            contents = Path("html/error.html").read_text()

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