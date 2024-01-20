#### Challenge:
    - Name: EzRev
    - Description: In and out of the matrix 🙂

The file attached to this challenge is a binary called `matrix`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/bed56af0-99e3-4324-92b8-f63a2d040f12)

So we're working with a x64 executable and after running the binary it showed this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7f2fbaf1-f27a-4c4e-8bea-6a64caf1e45d)

It seems that it only requires an integer which will be provided 4 times and from the result of the output we need the right input to escape the matrix

Since there's nothing much that can be done here I loaded the binary up in Ghidra

Here's the main function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/0efcd88e-9e5d-4ee9-abbf-7c31d45c4c28)

Since the variable names from the pseudocode isn't looking good I renamed it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/722f5948-5898-43f7-b3b9-86e4fd350608)

Ok it's looking good but here's the part which does not look too nice to the eyes:

```c
*(int *)(matrix + ((long)k + (long)j * 4) * 4);
```

Inorder words that piece of code is equivalent to `matrix[j][k]` so this means the data type for the global variable `matrix` isn't right

So I checked it to know the length of the array

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39ca954b-9356-46da-84c9-889927f0b008)

The size is 64 and since the elements there are `DWORD --> int()` whose size is 4 bytes that means the number of elements there are 16

And from the 2 nested inner loop which defines `j and k` it iterates till it reaches 4 twice meaning the matrix is a 4x4 matrix i.e it has 4 rows and 4 columns

At this point I changed the data type of the global variable matrix to `int[4][4]` 

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/02b4abc7-4aa6-4c8c-bdf6-36c5d4423b6a)

Now the pseudocode looks ok
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/87a7ef47-45b2-4f3d-bba5-2379d0030953)

```c

undefined8 main(void)

{
  undefined8 ret;
  int value [7];
  int sum;
  int c;
  int k;
  int j;
  int i;
  
  sum = 0;
  for (c = 0; c < 4; c = c + 1) {
    __isoc99_scanf("%d", &value[c]);
  }
  for (i = 0; i < 4; i = i + 1) {
    for (j = 0; j < 4; j = j + 1) {
      for (k = 0; k < 4; k = k + 1) {
        sum = sum + value[i] * matrix[j][k];
      }
    }
  }
  if (sum == check) {
    check_pass();
    ret = 0;
  }
  else {
    check_failed();
    ret = 0xffffffff;
  }
  return ret;
}
```

Now I'll explain what this does exactly

- First it would receive our input as an integer in a loop 4 times and the values are stored at the corresponding index position of the value array
- It defines a variable `sum` which initially holds the value `0` then in a 3 nested loop it does this:
      - Transverse over all the elements in the matrix, during the transversal it multiplies the elements by `value[i]` where the result is stored in the `sum` variable

Then the sum after the operation is done is compared with the value stored in the global variable `check` which is `0x00E00C4`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/39d948d8-d520-4da5-9c63-1f1c13caea12)


