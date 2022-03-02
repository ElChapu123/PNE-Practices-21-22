from server_class import Client

print(f"-----| Practice 2, Exercise 1 |------")

IP = "127.0.0.1"
PORT = 21000

c = Client(IP, PORT)
print(c)

print("Sending a message to the server...")
response = c.talk("Testing!!!")
print(f"Response:\n {response}")