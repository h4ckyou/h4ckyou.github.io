#include <stdio.h>
#include <string.h>

#define LEN 13

void print_password(char *correct, char *shift_array){
    char password[LEN + 1];

    for (int i = 0; i < LEN; i++){
        password[i] = correct[i] + shift_array[i];
    }

    printf("flag: flag{%s}", password);
}


int main(int argc, char** argv) {
    
    char correct[LEN + 1] = "ReenYbkV'('&)";
    char shift_array[LEN + 1] = {2,3,4,5,6,7,8,9,10,11,12,13,14};    

    print_password(correct, shift_array);

    return 1;

}

// gcc solve.c -o solve
// ./solve
