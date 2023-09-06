<h3> GreyHat 2023 CTF </h3>

Here are the writeups to the pwn challenges I solved:
- Babypwn


#### Babypwn

After downloading the attached file checking the file type shows this

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a38b5ee8-e0e5-4f05-8715-500ea7b58bb5)

So we're working with a x64 binary which is dynamically linked, not stripped and has all protections enabled

I'll run the binary to know what it does:
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3b54bef9-ace8-4052-b279-07e02d56b5da)

Seems to be some banking system that allows us withdraw & deposit money 

We can't find the vuln yet so let us look at the decompiled code

I'll be using ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bf53084c-d396-43af-bf9e-f19c0210129d)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/37ab1bcd-e9a9-445f-a646-379e689b8ad6)

```c
int main(void)

{
  long in_FS_OFFSET;
  short option;
  int accountBalance;
  uint tmp;
  long withdrawalAmount;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  accountBalance = 100;
  puts("==== Secure Banking System ====");
  puts("Welcome to the banking system.\nEarn $1000 to get the flag!\n");
menu:
  if (999 < accountBalance) {
    printf("\nCongratulations! You have reached the required account balance ($%d).\n",
           (ulong)(uint)accountBalance);
    puts("The flag is: grey{fake_flag}");
exit:
    if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
      return 0;
    }
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  puts("1. Check account balance");
  puts("2. Withdraw money");
  puts("3. Deposit money");
  puts("4. Exit\n");
  puts("Enter your option:");
  __isoc99_scanf("%hu",&option);
  if (option == 4) {
    puts("Thank you for banking with us.");
    goto exit;
  }
  if (option < 5) {
    if (option == 3) {
      puts("Deposit is still work in progress.");
      goto menu;
    }
    if (3 < option) goto LAB_00101344;
    if (option == 1) {
      printf("Your account balance is: $%d\n",(ulong)(uint)accountBalance);
      goto menu;
    }
    if (option == 2) {
      printf("Enter the amount to withdraw: ");
      __isoc99_scanf("%ld",&withdrawalAmount);
      tmp = accountBalance - (int)withdrawalAmount;
      if ((int)tmp < 0) {
        puts("You cannot withdraw more than your account balance.");
      }
      else {
        accountBalance = tmp;
        printf("Withdrawal successful. New account balance: $%d\n",(ulong)tmp);
      }
      goto menu;
    }
  }
LAB_00101344:
  puts("Invalid option.");
  goto menu;
}
```

