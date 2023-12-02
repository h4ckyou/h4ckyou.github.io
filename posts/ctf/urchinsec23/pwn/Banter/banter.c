#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
void finale(int haha);

void setup(){
        setvbuf(stdout, NULL, _IONBF, 0);
}
int menu(){
        char banter_password[10] = {0};
        int answer;
        printf("%s","[Man behind the mask]: Heeey, do you remember when we first met with Tahaa?\nWhat is the secr3t word to access the private room?\n");
        fgets(banter_password, sizeof(banter_password), stdin);
        answer = strncmp((char *)&banter_password,"N1CH0L0US_P4SS",0x9);
        if(answer == 0){
                printf("%s","\n[Man behind the mask]: Welcome to the Private Room Nich0!\n");
                printf("%s","[Nich0]: Am glad!\n");
                return 0;
        }else{
                printf("%s","[Man behind the mask]: Maybe you should try out some web challs!\n");
                exit(1);
        }
}

struct man{
        int age;
        char *name;
};

void winner(){
        puts("Hurray , you won!");
}
int main( int argc , char **argv ) {
        int i;
        struct man *man1, *man2, *man3;
        char name[20], description[20];
        man1 = malloc(sizeof(struct man));
        man1->age = 1;
        man1->name = malloc(8);
        man2 = malloc(sizeof(struct man));
        man2->age = 1;
        man2->name = malloc(8);
        setup();
        i = menu();
        sleep(1);
        if(i == 0){
                finale(1);
        }
        sleep(1);

        read(0 , name , 40);
        read(0 , description , 20);
        strcpy(man1->name , name);
        fflush(0);
        strcpy(man2->name , description);

        printf("\n[Nich0]: Siet !");
        return 0;
}
void finale(int haha){
        char buf[8] = {0};
        int result;

        printf("%s","[Man behind the mask]: There are some exclusive options, available only for you:)\n");
        read(0,&buf,8);
        result = strncmp((char *)&buf ,"Like?" , 0x5); 
        if(result == 0){
                printf("[Nich0]: %p ?\n",main);
                puts("\n[Chat...]: Loading ...");
        }
        sleep(10);
        printf("\n[Man behind the mask]: You have exhausted all the resources!");
}
