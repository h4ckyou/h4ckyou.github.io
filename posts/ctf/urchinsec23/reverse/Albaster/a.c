#include <stdio.h>

void b(int num)
{
    int result = num % 10 + ((num / 10) % 10) * 10;
    putchar(result);
    // printf("test");
    // printf("(%d) ", result);
}

void a(void)
{
    unsigned long long int i = 0x989FE854689F4DBD;
    long long int code;

    printf("\n [*] Please Enter The Code : ");
    scanf("%d", &code);

    if (code == 0) {
        puts("\n [*] Santa Is Going To Like You [*] ");
        puts("\n [*] ************************** [*] ");
        puts("\n [*] YOUR SECRET MESSAGE IS ..  [*] ");

        while (i > 0)
        {
            b((int)(i / 100) * -100 + (int)i);
            i = i / 100;
        }

        putchar(10);
    }
    else {
        puts("\n [*] TROLL FLAG [*] ");
    }

  return;
}

int main() {
    a();
    return 0;
}                                                                                            
