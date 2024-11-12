def main():
	num = int(input("Enter a number: "))
	num = subtract_seven(num)
	print("After Subtracting seven your output is : ", num)

def subtract_seven(num):
	num = num - 7
	return num



if __name__ == '__main__':
    main()