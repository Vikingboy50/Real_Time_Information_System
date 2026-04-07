#include <stdlib.h>
#include <time.h>

// Fonction qui génère 2 nombres aléatoires jusqu'à 1000000 et les multiplie

long long multiply_random_numbers() {
    long long a = (rand() % 1000000) + 1;
    long long b = (rand() % 1000000) + 1;
    return a * b;
}

// Main
int main() {
    srand(time(NULL)); // Initialiser le générateur de nombres aléatoires
    long long result = multiply_random_numbers();
    return 0;
}