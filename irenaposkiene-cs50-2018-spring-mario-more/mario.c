#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int a;
    // ask for a height
    do
    {
        a = get_int("HEIGHT:");

    }
    while (a < 0 || a > 23);

        // Print lines
    for (int i = 0; i < a; i++)
    {



        for (int j = 0; j  < a - 1 - i ; j++)
        {

            printf(" ");

        }
        // print hashes
        for (int z = 0; z < i + 1 ; z++)
        {

            printf("#");


        }

        // print spaces

        for (int j = 0; j < 2; j++)
        {

            printf(" ");

        }
        // print hashes
        for (int z = 0; z < i + 1; z++)
        {
            printf("#");

        }

        printf("\n");
    }


}
