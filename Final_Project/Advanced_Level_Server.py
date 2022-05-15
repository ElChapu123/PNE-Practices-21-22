import http.server
import http
import socketserver
import termcolor as t
from pathlib import Path
import jinja2 as j
from urllib.parse import urlparse, parse_qs
import commands
from seq1 import Seq
import json

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

        try:
            url_path = urlparse(self.path)
            path = url_path.path
            query = url_path.query

            cmd_dict = parse_qs(query)

            t.cprint(path, 'yellow')
            t.cprint(query, "green")
            t.cprint(cmd_dict, "blue")

            if path == "/":
                contents = Path("./html/index.html").read_text()

            elif path == "/favicon.ico":
                contents = Path("./html/index.html").read_text()

            elif path == "/list":
                try:
                    ENDPOINT = "/info/species"
                    PARAMS = "?content-type=application/json"

                    species_dict = commands.make_ensembl_request(ENDPOINT, PARAMS)
                    species = []
                    limit = int(cmd_dict["limit"][0])

                    if limit > len(species_dict["species"]) or 0 > limit:
                        contents = read_html_file("error.html") \
                            .render(context={"error": "Please, enter a valid value for the limit, between 0 and " + str(len(species_dict["species"]))})
                    else:
                        for n in range(0, int(limit)):
                            species.append(species_dict["species"][n]["name"])

                        if not "json" in cmd_dict:
                            contents = read_html_file(path[1:] + ".html") \
                                .render(context={"length": str(len(species_dict["species"])), "limit": limit, "species": species})
                        else:
                            contents = {"length": str(len(species_dict["species"])), "limit": limit, "species": species}


                except ValueError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Please, enter a valid value for the limit, between 0 and " + str(len(species_dict["species"]))})

            elif path == "/karyotype":
                ENDPOINT = "/info/assembly/" + cmd_dict["species"][0].strip().replace(" ", "_")
                PARAMS = "?content-type=application/json"

                karyotype_dict = commands.make_ensembl_request(ENDPOINT, PARAMS)

                try:
                    chromosomes = []
                    for e in karyotype_dict["karyotype"]:
                        chromosomes.append(e)

                    if chromosomes == []:
                        contents = read_html_file(path[1:] + ".html") \
                            .render(context={"karyotype": "Karyotype for this species was empty"})

                    else:
                        if not "json" in cmd_dict:
                            contents = read_html_file(path[1:] + ".html") \
                                .render(context={"karyotype": chromosomes})
                        else:
                            contents = {"Species": cmd_dict["species"][0], "karyotype": chromosomes}

                except KeyError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Karyotype for " + cmd_dict["species"][0] + " not found"})

            elif path == "/chromosome":
                ENDPOINT = "/info/assembly/" + cmd_dict["species"][0].strip().replace(" ", "_")
                PARAMS = "?content-type=application/json"

                species_dict = commands.make_ensembl_request(ENDPOINT, PARAMS)
                try:
                    chromosome_dict_list = species_dict["top_level_region"]
                    correct = False
                    i = 0
                    chosen_chromosome = cmd_dict["chromosome"][0]

                    while not correct and i < len(chromosome_dict_list):
                        chromosome = chromosome_dict_list[i]

                        if chromosome["name"] == chosen_chromosome:
                            correct = True

                        i += 1

                    chromosome_length = chromosome["length"]
                    if "json" not in cmd_dict:
                        contents = read_html_file(path[1:] + ".html") \
                            .render(context={"chromosome": chromosome["name"], "chromosome_length": chromosome_length})
                    else:
                        contents = {"chromosome": chromosome["name"], "chromosome_lenght": chromosome_length}
                except IndexError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Chromosome " + chosen_chromosome + " not found"})
                except KeyError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Karyotype for " + cmd_dict["species"][0] + " not found"})

            elif path == "/geneseq":
                try:
                    ENDPOINT = "/sequence/id/"
                    PARAMS = "?content-type=application/json"
                    wanted_gene = cmd_dict["identifier"][0]

                    gene_dict = commands.make_ensembl_request(ENDPOINT + wanted_gene, PARAMS)

                    seq = Seq(gene_dict["seq"])

                    if seq.valid_sequence():
                        if "json" not in cmd_dict:
                            contents = read_html_file("geneseq.html") \
                                .render(context={"seq": str(seq), "gene": wanted_gene})
                        else:
                            contents = {"seq": str(seq), "gene": wanted_gene}
                    else:
                        contents = "Incorrect sequence, please enter a correct sequence"

                except KeyError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Gene with identifier " + wanted_gene + " not found"})

            elif path == "/genecalc":
                try:
                    ENDPOINT = "/sequence/id/"
                    PARAMS = "?content-type=application/json"
                    wanted_gene = cmd_dict["identifier"][0]

                    gene_dict = commands.make_ensembl_request(ENDPOINT + wanted_gene, PARAMS)
                    seq = Seq(gene_dict["seq"])

                    if not seq.valid_sequence():
                        contents = read_html_file("error.html") \
                            .render(context={"error": "Incorrect sequence, please enter a correct sequence"})
                    else:
                        n_bases = seq.bases()
                        percentages = seq.base_percentage()
                        seq_len = seq.len()


                        contents = "\nTotal lenght: " + str(seq_len) + "\n"

                        for k in percentages:
                            contents = contents + str(k) + ": " + str(n_bases[k]) + " (" + str(percentages[k]) + "%)\n"

                        contents = contents.replace("\n", "<p><p>")
                        if "json" not in cmd_dict:
                            contents = read_html_file(path[1:] + ".html") \
                                .render(context={"result": contents, "seq": seq})
                        else:
                            contents = {"seq": str(seq), "length": seq_len, "percentages": percentages}

                except KeyError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Gene with identifier " + wanted_gene + " not found"})

            elif path == "/genelist":
                try:
                    ENDPOINT = "/phenotype/region/homo_sapiens/"
                    PARAMS = "?content-type=application/json"

                    chromosome = cmd_dict["chromosome"][0]
                    startpoint = cmd_dict["startpoint"][0]
                    endpoint = cmd_dict["endpoint"][0]

                    region = chromosome + ":" + startpoint + "-" + endpoint

                    region_dict = commands.make_ensembl_request(ENDPOINT + region, PARAMS)

                    gene_list = []

                    for e in region_dict:
                        gene_dict = e
                        if "phenotype_associations" in gene_dict:
                            for e in gene_dict["phenotype_associations"]:
                                if "attributes" in e:
                                    if "associated_gene" in e["attributes"]:
                                        gene_list.append(e["attributes"]["associated_gene"])

                    genes = []
                    for e in gene_list:
                        genes.append(e)


                    if genes == []:
                        if "json" not in cmd_dict:
                            contents = read_html_file("error.html") \
                                .render(context={"error": "No genes found"})
                        else:
                            contents = {"region": region, "genes": "No genes found"}

                    else:
                        if "json" not in cmd_dict:
                            contents = read_html_file(path[1:] + ".html") \
                                .render(context={"region": region, "genes": genes})
                        else:
                            contents = {"region": region, "genes": genes}

                except KeyError:
                    contents = read_html_file("error.html") \
                        .render(context={"error": "Chromosome not found"})

        except KeyError:
            contents = read_html_file("error.html") \
                .render(context={"error": "Please enter a valid argument"})
        except http.client.InvalidURL:
            contents = read_html_file("error.html") \
                .render(context={"error": "Please enter a valid statement"})

        try:

            # Generating the response message
            self.send_response(200)  # -- Status line: OK!

            # Define the content-type header:
            if not "json" in cmd_dict:
                self.send_header('Content-Type', 'text/html')
            else:
                contents = json.dumps(contents)
                self.send_header('Content-Type', 'application/json')

            self.send_header('Content-Length', len(str.encode(contents)))

        except UnboundLocalError:
            contents = read_html_file("error.html") \
                .render(context={"error": "Page not found"})

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