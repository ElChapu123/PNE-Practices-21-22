from pathlib import Path
import jinja2 as j
import http.client
import json

def read_html_file(filename):
    HTML_FOLDER = "./html/"
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents

def make_ensembl_request(ENDPOINT, PARAMS):
    SERVER = 'rest.ensembl.org'

    URL = SERVER + ENDPOINT + PARAMS

    print(f"\nConnecting to server: {URL}\n")

    # Connect with the server
    conn = http.client.HTTPConnection(SERVER)

    # -- Send the request message, using the GET method. We are
    # -- requesting the main page (/)
    try:
        conn.request("GET", ENDPOINT + PARAMS)
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

    return data1

def create_response(html_file, context_dict, cmd_dict):
    if not "json" in cmd_dict:
        contents = read_html_file(html_file) \
            .render(context=context_dict)
    else:
        contents = context_dict

    return contents

def make_server_request(ENDPOINT, PARAMS):
    SERVER = "127.0.0.1:8080"

    URL = SERVER + ENDPOINT + PARAMS
    print(f"\nConnecting to server: {URL}\n")

    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", ENDPOINT + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()

    print(f"Response received!: {r1.status} {r1.reason}\n")

    data1 = r1.read().decode("utf-8")
    data1 = json.loads(data1)

    return data1