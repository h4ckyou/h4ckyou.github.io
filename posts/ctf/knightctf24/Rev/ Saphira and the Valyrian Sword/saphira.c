/* This code isn't functioning as i wanted it to I'm a bad coder jsyk */

#include <stdio.h>

int generate(unsigned long int time);
int final(unsigned long int v6);

int main(){
    
    int password;

    password = generate(1705876256);

    printf("Password: %lu\n", password);

}  

int generate(unsigned long int time){
    unsigned long int sum;
    unsigned long int a1;
    unsigned long int v5;
    unsigned long int v3;
    unsigned long int i;
    unsigned long int v7;
    unsigned long int v6;


    sum = 823;

    v6 = 0;
    v7 = 1;
    a1 = time;

    while (a1 > 0) {
        v5 = a1 % 10;
        v6 += v7 * (sum ^ v5);
        v7 *= 10;

        a1 /= 10;
    }

    printf("V6 %lu\n", v6);

    return time ^ final(v6);

}

int final(unsigned long int v6){
    long i;
    unsigned long int iterate;

    i = 0;

    for (iterate = v6; iterate != 0; iterate = iterate / 10){ 
        i = i * 10 + iterate % 10;
    }

    printf("Val: %lu\n", i);

    return i;
}
