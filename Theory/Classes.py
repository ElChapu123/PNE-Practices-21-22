class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_your_name(self):
        print("I'm {}".format(self.name))

    def show_your_age(self):
        print("I'm {} years old".format(self.age))

Antonio = Person("Antonio", 17)
Antonio.say_your_name()
Antonio.show_your_age()