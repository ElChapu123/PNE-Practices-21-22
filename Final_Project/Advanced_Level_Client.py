from server_class import Client
import commands
import termcolor as t


IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)
print(c)

command_list = ["/list", "/karyotype", "/chromosome", "/geneseq", "/genecalc", "/genelist"]

for cmd in command_list:
    t.cprint("* Testing " + cmd + "...", "green")

    if cmd == "/list":
        limit = input("Enter a limit for the list: ")

        params = "?" + "limit=" + limit + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/karyotype":
        species = input("Enter a species: ")

        params = "?" + "species=" + species + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/chromosome":
        species = input("Enter a species: ")
        chromosome = input("Enter a chromosome: ")

        params = "?" + "species=" + species + "&chromosome=" + chromosome + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/geneseq":
        identifier = input("Enter a gene identifier: ")

        params = "?" + "identifier=" + identifier + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/genecalc":
        identifier = input("Enter a gene identifier: ")

        params = "?" + "identifier=" + identifier + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/genelist":
        chromosome = input("Enter a chromosome: ")
        startpoint = input("Select the start point: ")
        endpoint = input("Select the end point: ")

        params = "?" + "chromosome=" + chromosome + "&startpoint=" + startpoint + "&endpoint=" + endpoint +"&json=on"

        response = commands.make_server_request(cmd, params)

    print()

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
