def main():
    name : str = input("What is your name? ")
    print(greet(name))


def greet(name):
    return "Greetings " + name + "!"
	
if __name__ == '__main__':
    main()
