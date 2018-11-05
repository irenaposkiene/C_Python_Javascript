def main() :

    # input the card number
    while True :
        cnumber = input("Please enter a card number : ")
        if cnumber.isdecimal() and int(cnumber ) > 0 :
            break

    # AMEX
    if len(cnumber ) == 15 and int(cnumber [0]) == 3 :
        if valid_15(cnumber ) == True :
            print("AMEX")
        else :
            print("INVALID")

    # MASTER
    elif len(cnumber ) == 16 and int(cnumber [0]) == 5 :
        if valid_16(cnumber ) == True :
            print("MASTERCARD")
        else :
            print("INVALID")

    #  VISA
    elif (len(cnumber ) == 16 or len(cnumber ) == 13 ) and int(cnumber [0]) == 4 :
        if (valid_16(cnumber ) or valid_13(cnumber ))== True :
            print("VISA")
        else :
            print("INVALID")

    else :
        print("INVALID")

    exit(0)

# validation credit card
def valid_16(cnumber ) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(8) :

        if int(cnumber [2*i]) * 2 >= 10 :
            res = int(cnumber [2*i]) * 2 % 10
            sum_even_1 += res + (int(cnumber [2*i]) * 2 - res) / 10
        else :
            sum_even_1 += int(cnumber [2*i]) * 2

    for i in range(8) :
        sum_even_2 += int(cnumber [2*i+1])

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True

    else :
        return False

def valid_15(cnumber ) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(7) :
        if int(cnumber [2*i+1]) * 2 >= 10 :
            res = int(cnumber [2*i+1]) * 2 % 10
            sum_even_1 += res + (int(cnumber [2*i+1]) * 2 - res) / 10
        else :
            sum_even_1 += int(cnumber [2*i+1]) * 2

    for i in range(8) :
        sum_even_2 += int(cnumber [2*i])

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True

    else :
        return False

def valid_13(cnumber ) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(6) :
        if int(cnumber [2*i+1]) * 2 >= 10 :
            res = int(cnumber [2*i+1]) * 2 % 10
            sum_even_1 += res + (int(cnumber [2*i+1]) * 2 - res) / 10
        else :
            sum_even_1 += int(cnumber [2*i+1]) * 2

    for i in range(7) :
        sum_even_2 += int(cnumber [2*i])

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True

    else :
        return False

if __name__ == "__main__" :
    main()