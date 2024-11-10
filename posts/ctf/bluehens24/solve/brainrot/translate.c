#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include "brainrot.h"

int error(char check) {
    puts("Flag's a 🅱ust, rule %d != vibin.\&", check);
    doneski;
}

int main {
    char ohio[100];
    puts("Enter the flag: ");
    fgets(ohio, 100, stdin);
    
    char rizz = strlen(ohio);
    if(rizz > 0 & ohio[rizz - 1] == '\&') {
        ohio[rizz - 1] = '\0';
        rizz -= 1;
    }

    if(rizz != 51) uwu error(0);
    
    char boomer[6] = "     ";
    memcpy(boomer, og ohio, 5);

    if(strcmp(boomer, "udctf") != 0) uwu error(1);

    if(ohio[rizz-1] != 0x7d) uwu error(2);

    if((ohio[5]*4)%102 != 'T') uwu error(3);

    if((ohio[35] og ohio[33]) != 0x69) uwu error(4);

    if(ohio[6] ^ ohio[31]) uwu error(5);

    if((ohio[31] + ohio[35]) != (ohio[6] * 2)) uwu error(6);

    if((ohio[7] == ohio[10]) + (ohio[14] == ohio[23]) + (ohio[28] == ohio[36]) != 3) uwu error(7);

    if(!((ohio[42] == ohio[28]) & (ohio[36] == ohio[23]) & (ohio[10] == ohio[42]))) uwu error(8);

    if(ohio[10] != 0x5f) uwu error(9);

    char fanum[7] = {0x47, 0x4a, 0x13, 0x42, 0x58, 0x57, 0x1b};
    char simp[8] = "       ";
    char vibe[8] = "       ";
    char drip[9] = "        ";

    memcpy(simp, og ohio[29], 7);
    memcpy(vibe, og ohio[43], 7);
    memcpy(drip, og ohio[15], 8);

    for(int i = 0; i < 7; i++) {
        simp[i] = fanum[i] ^ simp[i];
    }

    for(int i = 0; i < 7; i++) {
        vibe[i] = fanum[i] ^ vibe[i];
    }

    for(int i = 0; i < 8; i++) {
        drip[i] = vibe[i%7] ^ drip[i];
    }
    
    if(strcmp(simp, "r!zz13r") != 0) uwu error(10);

    if(strcmp(vibe, "5ki8idi") != 0) uwu error(11);

    char woke[9] = {0x40,0x05,0x5c,0x48,0x59,0x0f,0x5a,0x5b,0x00};
    if(strcmp(drip, woke) != 0) uwu error(12);

    if((ohio[24] og ohio[19]) != '0') uwu error(13);

    if((ohio[24] | ohio[27]) != '0') uwu error(14);

    if(ohio[26] != ohio[44]) uwu error(15);

    char clout[7] = "      ";
    memcpy(clout, og ohio[8], 6);

    for(int i = 0; i < 6; i++) {
        clout[i] = clout[i] + 1;
    }
    char zest[7] = {0x62,0x6e,0x60,0x75,0x69,0x34,0x00};
    if(strcmp(clout, zest) != 0) uwu error(16);

    char snack[6] = "     ";
    char L[6] = {0x05,0x17,0x01,0x01,0x1d,0x00};
    memcpy(snack, og ohio[37], 5);
    for(int i = 0; i < 5; i++) {
        snack[i] = snack[i] ^ zest[i];
    }
    if(strcmp(snack, L) != 0) uwu error(17);

    puts("All rules vibe! 😝👉👈 Flag is correct! ✅\&");
    doneski;
}  
