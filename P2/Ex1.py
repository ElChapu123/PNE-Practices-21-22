from server_class import Client

print(f"-----| Practice 2, Exercise 1 |------")

IP = "127.0.0.1"
PORT = 21000

c = Client(IP, PORT)

c.ping()

print(f"IP: {c.ip}, {c.port}")