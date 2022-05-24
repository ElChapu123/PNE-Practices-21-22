from server_class import Client
import commands
import termcolor as t

print(f"-----| Practice 3, Exercise 7 |------")

IP = "127.0.0.1"
PORT = 8080

c = Client(IP, PORT)
print(c)

command_list = ["/list", "/karyotype", "/chromosome", "/geneseq", "/geneseq", "/genelist"]

for cmd in command_list:
    t.cprint("* Testing " + cmd + "...", "green", end="\n\n")

    if cmd == "/list":
        limit = input("Enter a limit for the list: ")
        params = "?" + "limit=" + limit + "&json=on"

        response = commands.make_server_request(cmd, params)

    elif cmd == "/karyotype":
        species = input("Enter a species: ")
        params = "?" + "species=" + species + "&json=on"

        response = commands.make_server_request(cmd, params)
    print(response)
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
