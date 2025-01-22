#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

struct Table {
    uint8_t array[256];
    uint32_t i;
    uint32_t j;
};

struct Table *table;
char *content;
char *key = "Troll1337";
// char key[16] = "Hell";

void swap(uint32_t i, uint32_t j) {
    uint32_t value = table->array[i];
    table->array[i] = table->array[j];
    table->array[j] = value;
}

void init_table() {

    table = malloc(sizeof(struct Table));
    memset(table, 0, sizeof(struct Table));
    uint32_t size = strlen(key);

    for (size_t i = 0; i <= 255; i++) {
        table->array[i] = i;
    }

    table->j = 0;

    for (table->i = 0; table->i <= 255; table->i++) {
        table->j = (table->array[table->i] + table->j + key[table->i % size]) % 256;
        swap(table->i, table->j);
        // printf("val: %d\n", table->j);
    }
    
    table->j = 0;
    table->i = 0;

}

uint8_t get_byte(){
    table->i = (table->i + 1) % 256;
    table->j = (table->j + table->array[table->i]) % 256;
    swap(table->i, table->j);
    return table->array[(uint8_t)(table->array[table->i] + table->array[table->j])];
}

void decrypt(long size) {
    
        init_table();

        for (size_t i = 0; i < size; i++) {
            uint8_t key = get_byte();
            printf("%c", content[i] ^ key);
        }

        free(table);
}

void brute(long size) {
    char digit_str[2] = {0};
    int value = 0;
    uint32_t start = 0x67916000;
    uint32_t end = start + 0x1000;

    for (uint32_t seed = start; seed <= end; seed++) {
        srand(seed);

        for (int i = 0; i <= 4; i++) {
            value = rand() % 10;
            snprintf(digit_str, 2, "%d", value);
            strncat(key, digit_str, 1);
        }

        init_table();

        // for (size_t i = 0; i <= size; i++){
        //     uint8_t key1 = get_byte();
        //     if (key == 0xa4)
        // }

        uint8_t key1 = get_byte();
        uint8_t key2 = get_byte();
        uint8_t key3 = get_byte();

        putchar(0xa);
        memset(key, 0, 16);
        strncpy(key, "Hell", 4);

        free(table);
        table = NULL;
    }

    
}

int main(int argc, char *argv[]) {

    if (argc < 2) {
        fprintf(stderr, "Usage: %s <file_path>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "rb");
    if (file == NULL) {
        perror("Error opening file");
        return -1;
    }

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);

    content = malloc(size);
    if (content == NULL) {
        perror("Error allocating memory");
        return -1;
    }

    fread(content, 1, size, file); 
    fclose(file);

    decrypt(size);

}
