
#include <stdio.h>
#include <cs50.h>

//rules: American Express uses 15-digit numbers, MasterCard uses 16-digit numbers, and Visa uses 13- and 16-digit numbers.
//rules: American Express numbers all start with 34 or 37; MasterCard numbers all start with 51, 52, 53, 54, or 55; and Visa numbers all start with 4.
//check sum with Luhn’s algorithm

int main(void)
{
    long long number, cnumber, seconddigit;
    int firstdigitsum, seconddigitsum, finalsum;

    // ask credit card number
    do
    {
        printf("Number:\n");
        number = get_long_long();
    }
    while (number < 0);

    // get sum of digits starting with the number’s firs-to-last digit

    for (cnumber = number, firstdigitsum = 0; cnumber > 0; cnumber /= 100)
    {
        firstdigitsum += cnumber % 10;
    }

    // get sum of digits starting with the number’s second-to-last digit
    // also sum of themself

    for (seconddigit = number / 10, seconddigitsum = 0; seconddigit > 0; seconddigit /= 100)
    {
        if (2 * (seconddigit % 10) > 9)
        {
            seconddigitsum += (2 * (seconddigit % 10)) / 10;
            seconddigitsum += (2 * (seconddigit % 10)) % 10;
        }
        else
        {
            seconddigitsum += 2 * (seconddigit % 10);
        }
    }

    finalsum = firstdigitsum + seconddigitsum;

    // check the Card number
    //American Express numbers all start with 34 or 37; MasterCard numbers all start with 51, 52, 53, 54, or 55; and Visa numbers all start with 4
    //American Express uses 15-digit numbers, MasterCard uses 16-digit numbers, and Visa uses 13- and 16-digit numbers


    if (finalsum % 10 == 0)
    {
        if ((number >= 340000000000000 && number < 350000000000000) || (number >= 370000000000000 && number < 380000000000000))
        {
            printf("AMEX\n");
        }

        else if (number >= 5100000000000000 && number < 5600000000000000)
        {
            printf("MASTERCARD\n");
        }

        else if ((number >= 4000000000000 && number < 5000000000000) || (number >= 4000000000000000 && number < 5000000000000000))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }

    }
    else
    {
        printf("INVALID\n");

        return 0;
    }

    return 0;
}
