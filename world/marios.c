#include <cs50.h>
#include <stdio.h>

void print_row(int row, int height);

int main(void)
{
    int n;
    do
    {   // Here we are asking the user to give height until n > 0
        n = get_int("Height: ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        print_row(i + 1, n); // Corrected function call
    }
}

void print_row(int row, int height) // To print desired number of bricks in the rows we just created
{
    // Print spaces for left alignment
    for (int i = 0; i < height - row; i++)
    {
        printf(" ");
    }

    // Print left pyramid
    for (int i = 0; i < row; i++)
    {
        printf("#");
    }

    // Print gap between pyramids
    printf("  ");

    // Print right pyramid
    for (int i = 0; i < row; i++)
    {
        printf("#");
    }

    // Move to the next line
    printf("\n");
}
