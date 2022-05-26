import commands
import termcolor as t
import http.client

IP = "127.0.0.1"
PORT = 8080

SERVER = "127.0.0.1:8080"

conn = http.client.HTTPConnection(SERVER)

command_list = ["/list", "/karyotype", "/chromosome", "/geneseq", "/genecalc", "/genelist"]

for cmd in command_list:
    t.cprint("* Testing " + cmd + "...", "green")

    if cmd == "/list":
        limit = input("Enter a limit for the list: ")

        params = "?" + "limit=" + limit + "&json=on"

    elif cmd == "/karyotype":
        species = input("Enter a species: ")

        params = "?" + "species=" + species + "&json=on"

    elif cmd == "/chromosome":
        species = input("Enter a species: ")
        length = input("Enter a number: ")

        params = "?" + "species=" + species + "&length=" + length + "&json=on"

    elif cmd == "/geneseq":
        identifier = input("Enter a gene identifier: ")

        params = "?" + "identifier=" + identifier + "&json=on"

    elif cmd == "/genecalc":
        identifier = input("Enter a gene identifier: ")

        params = "?" + "identifier=" + identifier + "&json=on"

    elif cmd == "/genelist":
        chromosome = input("Enter a chromosome: ")
        startpoint = input("Select the start point: ")
        endpoint = input("Select the end point: ")

        params = "?" + "chromosome=" + chromosome + "&startpoint=" + startpoint + "&endpoint=" + endpoint +"&json=on"

    response = commands.make_server_request(conn, cmd, params)

    for e in response:
        t.cprint(e + ": ", "blue", end="")
        if type(response[e]) == list:
            print()
            for i in response[e]:
                t.cprint("   - " + str(i), "white")
        elif type(response[e]) == dict:
            for k, v in response[e]:
                t.cprint("   - " + k + ": ", "red", end="")
                t.cprint(v, "white")
        else:
            t.cprint(str(response[e]), "white")
    print()
