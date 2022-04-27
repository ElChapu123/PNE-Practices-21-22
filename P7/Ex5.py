# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client
import json
import termcolor as t
from seq1 import Seq


gene_dict = {"FRAT1": "ENSG00000165879",
             "ADA": "ENSG00000196839",
             "FXN": "ENSG00000165060",
             "RNU6_269P": "ENSG00000212379",
             "MIR633": "ENSG00000207552",
            "TTTY4C": "ENSG00000228296",
            "RBMY2YP": "ENSG00000227633",
            "FGFR3": "ENSG00000068078",
            "KDR": "ENSG00000128052",
            "ANK2": "ENSG00000145362"}

SERVER = 'rest.ensembl.org'
ENDPOINT = "/sequence/id/"
PARAMS = "?content-type=application/json"
URL = SERVER + ENDPOINT + PARAMS


print(f"\nConnecting to server: {SERVER}\n")

# Connect with the server
conn = http.client.HTTPConnection(SERVER)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
for gene in gene_dict:
    try:
        conn.request("GET", ENDPOINT + gene_dict[gene] + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    # -- Read the response message from the server
    r1 = conn.getresponse()

    # -- Print the status line
    print(f"Response received!: {r1.status} {r1.reason}\n")

    # -- Read the response's body
    data1 = r1.read().decode("utf-8")
    data1 = json.loads(data1)
    # -- Print the received data

    t.cprint("Gene", "green", end=": ")
    print(gene)

    t.cprint("Description", "green", end=": ")
    print(data1["desc"])

    seq = Seq(data1["seq"])

    t.cprint("Total length", "green", end=": ")
    print(str(seq.len()))

    seq_per = seq.base_percentage()
    seq_count = seq.bases()

    for k in seq_count:
        t.cprint(k, "blue", end= ": ")
        print(str(seq_count[k]), end= " ")
        print("(" + str(seq_per[k]) + "%)")

    t.cprint("Most Frequent Base", "green", end=": ")
    print(seq.most_common_base())

    print()