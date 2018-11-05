#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

// Create a program that encrypts messages using Caesar’s cipher.

int main(int argc, string argv[])
{
    // check for 2 arguments only
    if (argc != 2)
    {
        printf("Nope\n");
        return 1;
    }


    int k = atoi(argv[1]);

    // input text
    printf("plaintext: ");

    // give output
    string text = get_string();
    printf("ciphertext: ");

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        //check if the letter is uppercase or lowercase then convert
        if islower(text[i])
        {
            printf("%c", (((text[i] + k) - 97) % 26) + 97);
        }
        else if isupper(text[i])
        {
            printf("%c", (((text[i] + k) - 65) % 26) + 65);
        }
        //if neither then just print whatever it is
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;

}