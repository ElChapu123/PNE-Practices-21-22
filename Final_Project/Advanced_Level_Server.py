import http.server
import http
import socketserver
import termcolor as t
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import commands
from seq1 import Seq
import json

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

                    if cmd_dict != {}:
                        limit = int(cmd_dict["limit"][0])

                    else:
                        limit = len(species_dict["species"])

                    if limit > len(species_dict["species"]) or 0 > limit:
                        contents = {"error": "Please, enter a valid value for the limit, between 0 and " + str(len(species_dict["species"]))}
                        contents = commands.create_response("error.html", contents, cmd_dict)

                    else:
                        for n in range(0, int(limit)):
                            species.append(species_dict["species"][n]["name"])

                        contents = {"length": str(len(species_dict["species"])), "limit": limit, "species": species}
                        contents = commands.create_response(path[1:] + ".html", contents, cmd_dict)

                except ValueError:
                    contents = {"error": "Please, enter a valid value for the limit, between 0 and " + str(len(species_dict["species"]))}
                    contents = commands.create_response("error.html", contents, cmd_dict)

            elif path == "/karyotype":
                ENDPOINT = "/info/assembly/" + cmd_dict["species"][0].strip().replace(" ", "_")
                PARAMS = "?content-type=application/json"

                karyotype_dict = commands.make_ensembl_request(ENDPOINT, PARAMS)

                try:
                    chromosomes = []
                    for e in karyotype_dict["karyotype"]:
                        chromosomes.append(e)

                    if chromosomes == []:
                        contents = {"karyotype": "Karyotype for this species was empty"}
                        contents = commands.create_response(path[1:] + ".html", contents, cmd_dict)

                    else:
                        contents = {"Species": cmd_dict["species"][0], "karyotype": chromosomes}
                        contents = commands.create_response(path[1:] + ".html", contents, cmd_dict)

                except KeyError:
                    contents = {"error": "Species not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)

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

                    print(chromosome)
                    print(correct)

                    if correct:
                        contents = {"chromosome": chromosome["name"], "length": chromosome["length"]}
                        contents = commands.create_response(path[1:] +".html", contents, cmd_dict)

                    else:
                        contents = {"error": "Chromosome " + chosen_chromosome + " not found"}
                        contents = commands.create_response("error.html", contents, cmd_dict)

                except IndexError:
                    contents = {"error": "Chromosome " + chosen_chromosome + " not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)
                except KeyError:
                    contents = {"error": "Karyotype for " + cmd_dict["species"][0] + " not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)

            elif path == "/geneseq":
                try:
                    ENDPOINT = "/sequence/id/"
                    PARAMS = "?content-type=application/json"
                    wanted_gene = cmd_dict["identifier"][0]

                    gene_dict = commands.make_ensembl_request(ENDPOINT + wanted_gene, PARAMS)

                    seq = Seq(gene_dict["seq"])

                    if seq.valid_sequence():
                        contents = {"seq": str(seq), "gene": wanted_gene}
                        contents = commands.create_response("geneseq.html", contents, cmd_dict)

                    else:
                        contents = {"error":"Incorrect sequence, please enter a correct sequence"}
                        contents = commands.create_response("error.html", contents, cmd_dict)

                except KeyError:
                    contents = {"error": "Gene with identifier " + wanted_gene + " not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)

            elif path == "/genecalc":
                try:
                    ENDPOINT = "/sequence/id/"
                    PARAMS = "?content-type=application/json"
                    wanted_gene = cmd_dict["identifier"][0]

                    gene_dict = commands.make_ensembl_request(ENDPOINT + wanted_gene, PARAMS)
                    seq = Seq(gene_dict["seq"])

                    percentages = seq.base_percentage()
                    seq_len = seq.len()

                    contents = {"seq": str(seq), "length": seq_len, "percentages": percentages}
                    contents = commands.create_response(path[1:] + ".html", contents, cmd_dict)

                except KeyError:
                    contents = {"error": "Gene with identifier " + wanted_gene + " not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)

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


                    if gene_list == []:
                        contents = {"error": "No genes found in region " + region}
                        contents = commands.create_response("error.html", contents, cmd_dict)
                    else:
                        contents = {"region": region, "genes": gene_list}
                        contents = commands.create_response(path[1:] + ".html", contents, cmd_dict)

                except KeyError:
                    contents = {"error": "Region not found"}
                    contents = commands.create_response("error.html", contents, cmd_dict)

        except KeyError:
            contents = {"error": "Please enter a valid argument"}
            contents = commands.create_response("error.html", contents, cmd_dict)

        except http.client.InvalidURL:
            contents = {"error": "Please enter a valid statement"}
            contents = commands.create_response("error.html", contents, cmd_dict)

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
            contents = {"error": "Page not found"}
            contents = commands.create_response("error.html", contents, cmd_dict)

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