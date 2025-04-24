#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"


unsigned int count_words = 0;


unsigned int size(void);


typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;


const unsigned int N = 20000;


node *table[N];

bool check(const char *word)
{

    int word_index = hash(word);


    node *cursor = table[word_index];


    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true; // word is found
        }
        // set the cursor to the next node in the linked list
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

    unsigned int roll_sum = 0;
    unsigned int squared = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        squared = pow(toupper(word[i]), 2);
        if (i == round(strlen(word) / 2))
        {
            roll_sum = roll_sum + round(sqrt(roll_sum)) + 17;
        }
        roll_sum = squared + roll_sum + 47;
    }
    return roll_sum % N;
}

bool load(const char *dictionary)
{

    FILE *dict_open = fopen(dictionary, "r");
    if (dict_open == NULL)
    {
        printf("Could not open the dictionary file.\n");
        return false;
    }
    else if (dict_open != NULL)
    {
        char buffer[LENGTH + 1];
        int hash_index = 0;
        while (fscanf(dict_open, "%s", buffer) != EOF)
        {

            node *n = malloc(sizeof(node));
            // check that memory is initialized ok
            if (n == NULL)
            {
                return false;
                break;
            }
            else if (n != NULL)
            {
                strcpy(n->word, buffer);
                // set address to NULL
                n->next = NULL;



                hash_index = hash(buffer);

                // if nothing is there equal the first entry to the new node
                if (table[hash_index] == NULL)
                {
                    table[hash_index] = n;
                }

                else if (table[hash_index] != NULL)
                {
                    n->next = table[hash_index];
                    table[hash_index] = n;
                }

                // count words
                count_words++;
            }
        } // end while loop
        fclose(dict_open);
        return true;
    }
    else
    {
        return false;
    }
}

unsigned int size(void)
{
    // summed count words whilst loading
    return count_words;
}

bool unload(void)
{

    for (int i = 0; i < N; i++)
    {
        node *temp = table[i];
        node *cursor = table[i];


        while (temp != NULL)
        {
            // set cursor to next
            cursor = cursor->next; // i+1
            free(temp);
            temp = cursor;
        }
    }
    return true;
}
