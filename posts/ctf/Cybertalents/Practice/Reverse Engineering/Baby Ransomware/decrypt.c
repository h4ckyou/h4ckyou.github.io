#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

struct evil {
    uint8_t array[256];
    uint32_t i;
    uint32_t j;
};

struct evil *obj;
char *content;
long size;
char key[16] = "Hell";

void swap(uint8_t i, uint8_t j) {
    uint8_t value = obj->array[i];
    obj->array[i] = obj->array[j];
    obj->array[j] = value;
}

void initialize() {
    obj = malloc(sizeof(struct evil));
    uint32_t size = strlen(key);

    for (size_t i = 0; i <= 255; i++) {
        obj->array[i] = i;
    }

    obj->j = 0;

    for (obj->i = 0; obj->i <= 255; obj->i++) {
        obj->j = (obj->array[obj->i] + obj->j + key[obj->i % size]) % 256;
        swap(obj->i, obj->j);
    }
    
    obj->j = 0;
    obj->i = 0;

}

uint8_t get_byte(){
    obj->i = (obj->i + 1) % 256;
    obj->j = (obj->j + obj->array[obj->i]) % 256;
    swap(obj->i, obj->j);
    uint8_t pos = obj->array[obj->i] + obj->array[obj->j];
    return obj->array[pos];
}


char *decrypt() {
    char *result = malloc(size);

    for (size_t i = 0; i < size; i++){
        uint8_t key = get_byte();
        result[i] = key ^ content[i];
    }

    return result;
}

void brute() {
    char digit_str[2] = {0};
    uint16_t value = 0;
    uint32_t timestamp = 0x5f1c438e;
    uint32_t start = timestamp - 0x10000;
    uint32_t end = timestamp + 0x100000;

    for (uint32_t seed = start; seed <= end; seed++) {
        srand(seed);

        for (int i = 0; i <= 4; i++) {
            value = rand() % 10;
            snprintf(digit_str, 2, "%d", value);
            strncat(key, digit_str, 1);
        }
        
        initialize();

        char *data = decrypt();
        
        if (strstr(data, "FLAG")) {
            printf("%s", data);
            exit(EXIT_SUCCESS);
        }

        memset(key, 0, 16);
        strncpy(key, "Hell", 4);

        free(obj);
        free(data);

        obj = NULL;
        data = NULL;
    }

}

int main(int argc, char *argv[]) {

    if (argc < 2) {
        fprintf(stderr, "Usage: %s filename \n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "rb");
    if (file == NULL) {
        perror("Error opening file");
        return -1;
    }

    fseek(file, 0, SEEK_END);
    size = ftell(file);
    fseek(file, 0, SEEK_SET);

    content = malloc(size);
    if (content == NULL) {
        perror("Error allocating memory");
        return -1;
    }

    fread(content, 1, size, file); 
    fclose(file);

    brute();

}
