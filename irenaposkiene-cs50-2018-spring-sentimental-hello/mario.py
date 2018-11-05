import cs50

def main():


    # ask for a height

    while True:
        print("Height: ", end = "")

        a = cs50.get_int()
        if a <= 23 and a > 0:
            break

    # Print lines
        for i in range(0, a):

            for j in range(0, a-1-i):

                print(" ", end="")

    # print hashes

            for z in range(0, i+1):

                print("#", end="")


    # print spaces

            for j in range(0, 2):

                print(" ", end="")

     # print hashes

            for z in range(0, i+1):

                print("#", end="")

        print();




if __name__ == "__main__":
    main()