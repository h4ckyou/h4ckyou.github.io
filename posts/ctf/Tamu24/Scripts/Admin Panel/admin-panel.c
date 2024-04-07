#include <stdio.h>
#include <string.h>

int upkeep() {
	// IGNORE THIS
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

int admin() {
	int choice = 0;
	char report[64];

	puts("\nWelcome to the administrator panel!\n");
	puts("Here are your options:");
	puts("1. Display current status report");
	puts("2. Submit error report");
	puts("3: Perform cloning (currently disabled)\n");

	puts("Enter either 1, 2 or 3: ");
	scanf("%d", &choice);

	printf("You picked: %d\n\n", choice);

	if (choice==1) {
		puts("Status report: \n");
		
		puts("\tAdministrator panel functioning as expected.");
		puts("\tSome people have told me that my code is insecure, but");
		puts("\tfortunately, the panel has many standard security measures implemented");
		puts("\tto make up for that fact.\n");

		puts("\tCurrently working on implementing cloning functionality,");
		puts("\tthough it may be somewhat difficult (I am not a competent programmer).");
	}
	else if (choice==2) {
		puts("Enter information on what went wrong:");
		scanf("%128s", report);
		puts("Report submitted!");
	}
	else if (choice==3) {
		// NOTE: Too dangerous in the wrong hands, very spooky indeed
		puts("Sorry, this functionality has not been thoroughly tested yet! Try again later.");
		return 0;

		clone();
	}
	else {
		puts("Invalid option!");
	}
}

int main() {
	upkeep();

	char username[16];
	char password[24];
	char status[24] = "Login Successful!\n";

	puts("Secure Login:");
	puts("Enter username of length 16:");
	scanf("%16s", username);
	puts("Enter password of length 24:");
	scanf("%44s", password);
	printf("Username entered: %s\n", username);
	if (strncmp(username, "admin", 5) != 0 || strncmp(password, "secretpass123", 13) != 0) {
		strcpy(status, "Login failed!\n");
		printf(status);
		printf("\nAccess denied to admin panel.\n");
		printf("Exiting...\n");
		return 0;
	}
	
	printf(status);
	admin();

	printf("\nExiting...\n");
}

