#include <stdio.h>
#include <string.h>

#define LEN 13

int Password_Checker(char* password, char* correct, char* shift_array) {
    int i = 0;
    char success = 1;
    do {
        char shift_arrayed_char = correct[i] + shift_array[i];
        if (shift_arrayed_char != password[i]) {
            return 0;
        }
        i++;
    } while (correct[i] != 0 && password[i] != 0);
    return 1;
}

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Needs one argument :D.\n");
        return -1;
    }
    char correct[LEN + 1] = "ReenYbkV'('&)";
    char shift_array[LEN + 1] = {2,3,4,5,6,7,8,9,10,11,12,13,14};    
    if (strlen(argv[1]) == LEN && Password_Checker(argv[1], correct, shift_array)) {
        printf("Correct :D \n");
        return 0;
    }
    
    printf("Wrong password \n");
    return 1;

}
