#include <stdlib.h>
#include <time.h>

// Function that generates 2 random numbers up to 1000000 and multiplies them

long long multiply_random_numbers() {
    long long a = (rand() % 1000000) + 1;
    long long b = (rand() % 1000000) + 1;
    return a * b;
}

// Main
int main() {
    srand(time(NULL)); // Initialize the random number generator
    long long result = multiply_random_numbers();
    return 0;
}