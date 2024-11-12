def main():
    lst = []  # Make an empty list to store values

    val = input("Enter a value: ")  # Get an initial value from the user
    while val:  # Keep looping while the user doesn't press enter without typing
        lst.append(val)  # Add the entered value to the list
        val = input("Enter a value: ")  # Get the next value to add

    print("Here's the list:", lst)  # Print the list when user presses Enter without any value


if __name__ == '__main__':
    main()
