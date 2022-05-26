from pathlib import Path
import jinja2 as j
import json

def read_html_file(filename):
    HTML_FOLDER = "./html/"
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = j.Template(contents)
    return contents


def make_server_request(conn, ENDPOINT, PARAMS):
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

def format_list(my_list):
    new_list = []
    not_numbers = []

    for e in my_list:
        if e.isdigit():
            new_list.append(int(e))
        else:
            not_numbers.append(e)

    new_list = sorted(new_list)
    new_list = new_list + not_numbers

    return new_list