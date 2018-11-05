// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>


#include "dictionary.h"



///list
typedef struct node
{
    bool is_word;
    struct node* children[27];
}
node;


node* root;



// Size of trie
unsigned int total_nodes = 0;


// Returns index of letter

int getIndex(const char c)
{
    if (c == '\'')
    {
        return 26;
    }
    else
    {
        return tolower(c) % 'a';
    }
}


// Returns true if word is in dictionary
bool check(const char *word)
{
    // TODO node* ptr = root;
     node* cursor = root;

    // for each letter in input word
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Find the index of the letter
        int index = getIndex(word[i]);


        if (cursor->children[index] == NULL)
        {
            // if NULL word is mispelled
            return false;
        }

        // if not NULL, move to next letter
        cursor = cursor->children[index];
    }

    // once at end of input word, check if is_word is true
    return cursor->is_word;


}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
   // Create space for root
   root = malloc(sizeof(node));

   // Initialize number of nodes
    total_nodes = 0;

    // Read dictionary
    FILE* fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        unload();
        return false;
    }

    // Set cursor to root
    node* cursor = root;

    // Read r in dictionary
    for (int c = fgetc(fp); c != EOF; c = fgetc(fp))
    {
        // Check if it is newline
        if (c == '\n')
        {

            cursor->is_word = true;


            total_nodes++;


            cursor = root;
        }
        else
        {

            int index = getIndex(c);


            if (cursor->children[index] == NULL)
            {

                cursor->children[index] = malloc(sizeof(node));
            }


            cursor = cursor->children[index];
        }
    }

    // Close dictionary
    fclose(fp);

    return true;
}



// Returns number of words in dictionary
unsigned int size(void)
{
    // TODO
    return total_nodes;

}


bool clean_nodes(node* ptr)
{

     for (int i = 0; i < 27; i++)
    {

        if (ptr->children[i] != NULL)
        {
            clean_nodes(ptr->children[i]);
        }
    }


    free(ptr);

    return true;
}


bool unload(void)
{
    // TODO
    return clean_nodes(root);

    return true;
}
