#include <cs50.h>
#include <stdio.h>

void print_row (int bricks);

int main (void)

{
    int n;
    do
    {                                   //Here we are asking user to give height until n > 0
        n = get_int ("Height: ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        print_row (i + 1);
    }
}

void print_row (int bricks)             // To print desired number of bricks in the rows we just created
{
for (int i = 0; i < bricks; i++)
{
    printf ("#");
}

    printf ("\n");
}
