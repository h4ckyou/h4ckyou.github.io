#include <stdio.h>
#include <stdlib.h>
int *clothes[10];
int clothes_count = 0;
int money = 10;
int *inprogress_clothe = NULL;
int upgrade_quality = 0;
int upgrade_timer = 0;
void print_flag()
{
    char buf[0x80];
    FILE *file;
    if ((file = fopen("flag.txt", "r")) != NULL)
    {
        fgets(buf, sizeof(buf), file);
        printf("Flag: %s\n", buf);
    }
    else
    {
        printf("No flag found. If you're getting this on the server, message an admin.\n"
               "If you're getting this locally, try on the server!\n");
    }
}
void help()
{
    printf("------------------------\n");
    printf("You have %d moneyz, 1 moneyz buys 1 swagz\n", money);
    printf("You have %d clothes\n", clothes_count);
    printf("What do you want?\n");
    printf("1. Buy clothes\n");
    printf("2. Sell clothes\n");
    printf("3. Upgrade clothes\n");
    printf("4. Assess swag\n");
}
int buy_clothes()
{
    if (clothes_count > 9)
    {
        printf("Your wardrobe is full. Maybe one day you can upgrade to a bigger wardrobe.\n");
        return 0;
    }
    int quality = 0;
    printf("What quality clothes would you like to buy? (1-5)\n");
    printf("> ");
    scanf("%d", &quality);
    if (money < quality || quality < 1 || quality > 5)
        return 0;
    money -= quality;
    int *cloth = malloc(sizeof(int));
    *cloth = quality;
    clothes[clothes_count++] = cloth;
    return 1;
}

int sell_clothes()
{
    if (clothes_count == 0)
    {
        printf("No clothes to sell\n");
        return 0;
    }
    char c = 0;
    printf("Sell your last clothe? (y/n)\n");
    printf("> ");
    while (c != 'y' && c != 'n')
        scanf("%c", &c);
    if (c != 'y')
        return 0;
    money += *clothes[clothes_count-1];
    free(clothes[--clothes_count]);
    return 1;
}

int queue_upgrade_clothes()
{
    int index = -1;
    int quality = 0;
    printf("Cut hole in which clothe?\n");
    printf("> ");
    scanf("%d", &index);
    if (index < 0 || index >= clothes_count)
        return 0;
    printf("How many holes? (1-5)\n");
    printf("> ");
    scanf("%d", &quality);
    if (money < quality || quality < 1 || quality > 5)
        return 0;
    money -= quality;
    upgrade_quality = *clothes[index] + quality;
    upgrade_timer = quality;
    inprogress_clothe = clothes[index];
    printf("Your clothes will be ready in %d\n", quality);
    return 1;
}
void apply_upgrade()
{
    *inprogress_clothe = upgrade_quality;
    inprogress_clothe = NULL;
    upgrade_quality = 0;
    upgrade_timer = 0;
    printf("Your upgrade is done!\n");
}
void assess()
{
    int swag = 0;
    for (int i = 0; i < clothes_count; ++i)
    {
        swag += *clothes[i];
    }
    printf("You have %d swagz\n", swag);
    if (money > 100)
    {
        printf("Ah, a true entrepreneur\n");
        print_flag();
    }
}
void menu()
{
    int option = 0;
    help();
    if (inprogress_clothe && --upgrade_timer == 0)
        apply_upgrade();
    printf("> ");
    scanf("%d", &option);
    int result = 1;
    switch(option)
    {
        case 1:
            result = buy_clothes();
            break;
        case 2:
            result = sell_clothes();
            break;
        case 3:
            result = queue_upgrade_clothes();
            break;
        case 4:
            assess();
            break;
        default:
            break;
    }
    if (!result)
    {
        printf("Something went wrong :(\n");
    }
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    for (int i = 0; i < 300; ++i)
    {
        menu();
    }
    printf("You died of old age.\n");
    return 0;
}
