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

I won't explain what that all does. But basically.
- While our current account balance is less than 1000
- We have the choice to choose any of the 3 options in the menu
- The first option shows us our account balance
- The second option allows us to make withdrawal
- The third option is still in progress
- The fourth option exits the program

The aim of this program is to earn $1000 to get the flag

```c
puts("Welcome to the banking system.\nEarn $1000 to get the flag!\n")
```

How can we achieve that?

Take a look at the withdrawal option

```c
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
```

After it receives the amount we want to withdraw, It will set a temp variable holding the difference between our current account balance and the withdrawalamount

If the temp variable is less than 0 we get the error message that basically means we can't withdraw an amount greater than our current account balance

Else it sets our current account balance to the temp variable and prints out the current balance

The vulnerability in this program is that it doesn't check if the amount to be withdrawed is a negative number

With that if we give it a number less than our balance it will sum up to a positive number greater than our current balance

```
accountBalance = 100
withdrawalAmount = -10000
tmp = accountBalance - withdrawalAmount
# tmp = 100 - (-10000) --> 100 + 10000
```

That logic is one of the vulnerability of this program and with that we can get the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3b16142b-3015-4599-b05e-d3a6c71e4342)

Another way we can exploit this is via Integer Overflow

I won't explain that but here's a good sample payload: `0xffffffff - 10000`

That will sum our account balance to `0` then `10000` will be added since the negative sign will turn to positive
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/5b677d4f-f318-4bef-a691-44e5cfe6402f)

We can try that on the remote server
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/68063319-70b9-4bd3-8fc0-f1958f0a76d2)

```
Flag: grey{b4by_pwn_df831aa280e25ed6c3d70653b8f165b7}
```




