#include <iostream>
#include <string>

int findLongestRepetition(const std::string &sequence) {
    int maxRepetition = 0;
    int currentRepetition = 1;
    char previousChar = sequence[0];

    for (size_t i = 1; i < sequence.length(); ++i) {
        char currentChar = sequence[i];
        if (currentChar == previousChar) {
            ++currentRepetition;
        } else {
            maxRepetition = std::max(maxRepetition, currentRepetition);
            currentRepetition = 1;
            previousChar = currentChar;
        }
    }

    return std::max(maxRepetition, currentRepetition);
}

int main() {
    std::string sequence;
    std::cout << "";
    std::cin >> sequence;

    int longestRepetition = findLongestRepetition(sequence);
    std::cout << "" << longestRepetition << std::endl;

    return 0;
}
