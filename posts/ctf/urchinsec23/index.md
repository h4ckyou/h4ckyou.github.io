<h3> Urchinsec XMAS 2023 CTF </h3>

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/1f0815f9-8bb1-4c87-b612-69c1107d0b7d)

#### INITIAL DETAILS 
I wanted to make a detailed solution.......... but eventually felt lazy to do so

So you can view the solve script of some challenges: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/)

#### FINAL DETAILS

The organizers put a prize on the best writeup that would be provided then I came back here to make a detailed writeup! 😸
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/9bb0ac0c-75a0-4ec9-af40-f11731fce45f)

I will be writing on the crypto, pwn and rev challenges that I solved.

#### Reverse Engineering
- Sexy Primes
- UrchinFlag
- SugarPlum

#### Cryptography
- Minstix
- SantaZIP
- Honey Sea
- By Polar RSA

#### Pwn
- BOF

### Reverse Engineering

#### Sexy Primes
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/de1ea3d1-5038-47b5-b4ac-6bfd76fac54b)

So we're working with a x64 binary which is dynamically linked and not stripped

Running it keeps printing out `6` for some reason

Decompiling it in Ghidra and going over to the main function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/21b121cb-880e-4edf-8707-537536dfbd1e)

```c
undefined8 main(void)

{
  sexyprime();
  return 0;
}
```

Nothing really there except that it calls the `sexyprime` function

Here's the decompiled `sexyprime` function
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4918dd40-aede-41e4-a019-a9664fdeee65)

```c
void sexyprime(void)

{
  long in_FS_OFFSET;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  printf("%d",6);
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Looking at it we can see it just indeeds prints out `6` but is that all?

Ghidra does not seem to decompile the binary well I have no idea why, but if you take a look at the assembly decompilation you'd see it does some other stuffs
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/6a146c4f-af52-441d-86d9-78a6c99f0ffb)

At some point it's supposed to receive user input but that check isn't being reached

So I decided to manually step through each instruction to figure why it doesn't work

I set a breapoint at the `sexyprime` function:

```
break *sexyprime
```

At `sexyprime+58` I saw that it compares the value of `$rbp-0x80` to `0x6`, checking the current value shows it's right
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/390db2f2-9c3b-4402-8431-374f484a018a)

Moving to the next 3 instructions shows another comparism
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/11da310c-8758-481a-882b-c40b250f57b5)

In this case it would fail and if it does it would jump to `sexyprime+1701` which would `ret` and the program would exit

The reason it would fail is because of this:

```
mov    DWORD PTR [rbp-0x7c], 0x10
```

The value of `$rbp-0x7c` would be `0x10` and when it's compared to `0x6` that would return False

We can set the value to `0x6`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/02323163-4b53-48ae-a84d-d75954c763ab)

Moving to the next instructions continues the execution flow till we reach the first `scanf` call which expects an integer
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/43688677-cab5-4e1f-9250-ef6b5851d393)

After moving through some few instructions I noticed that it would put some value to the `edx` register then subtracts it by the current value of the `eax` register and compare to `0x6` 

So what I just did was to copy the values that's been put to the `edx` register then used `chr` which would convert the integer to its unicode character 

And that turned out to be the flag

Here's how it looked like in my python history

```
>>> flag
'urchinsec{sexy_primes_'
>>> flag += chr(0x70)
>>> flag += chr(0x72)
>>> flag
'urchinsec{sexy_primes_pr'
>>> flag += chr(0x69)
>>> flag += chr(0x6d)
>>> flag += chr(0x69)
>>> flag
'urchinsec{sexy_primes_primi'
>>> flag += chr(0x6e)
>>> flag
'urchinsec{sexy_primes_primin'
>>> flag += chr(0x67)
>>> flag
'urchinsec{sexy_primes_priming'
>>> flag += chr(0x7d)
>>> flag
'urchinsec{sexy_primes_priming}'
>>>
```

And I got the final flag:

```
Flag: urchinsec{sexy_primes_priming}
```

#### UrchinFlag

We were given an apk file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/eff4b412-09d8-4eac-a1d5-89c360ba9e79)

First thing I did was to unzip it and after doing that I got this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/03e53a5d-021c-40a7-aa5f-233382fa4c97)

There are three `.dex` files which I converted to a `.jar` file using [dex2jar](https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip)

And from there I decompiled it using `jd-gui`

It's the `classes3.dex` file that had the source code for the apk file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/8649f9c0-010a-44d5-afba-2eb6269496cf)

```java
package com.urchinsec.urchinflag;

import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
  Button login_button;
  
  EditText password_input;
  
  EditText username_input;
  
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(R.layout.activity_main);
    this.login_button = (Button)findViewById(R.id.login_btn);
    this.username_input = (EditText)findViewById(R.id.username_inp);
    this.password_input = (EditText)findViewById(R.id.password_inp);
    this.login_button.setOnClickListener(new View.OnClickListener() {
          final MainActivity this$0;
          
          public void onClick(View param1View) {
            if (MainActivity.this.username_input.equals("urchinsec_rang3r")) {
              if (MainActivity.this.password_input.equals("s0m334ga71344$!$")) {
                StringBuilder stringBuilder = (new StringBuilder((CharSequence)MainActivity.this.password_input)).reverse();
                String str = "urchinsec{" + MainActivity.this.username_input + "_@_" + stringBuilder + "}";
                Toast.makeText((Context)MainActivity.this, str, 1);
              } else {
                Toast.makeText((Context)MainActivity.this, "Wrong Password", 0);
              } 
            } else {
              Toast.makeText((Context)MainActivity.this, "Wrong Username", 0);
            } 
          }
        });
  }
}

```

I don't know Java but this was quite understandable:
- First it seems to receive our input which are the `username & password`
- It compares the received username to `urchinsec_rang3r` and the received password to `s0m334ga71344$!$`
- If the comparism returns True it would reverse the password provided which is stored in the `stringBuilder` variable
- Then finally the flag is formed from this: `urchinsec{" + username + "_@_" + stringBuilder + "}"`

With that said I just reversed the password string and was able to submit the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/38afef1e-d553-4d45-ba2d-d9813fab0d65)

```
Flag: urchinsec{urchinsec_rang3r_@_$!$44317ag433m0s}
```

#### SugerPlum
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/53c77e9a-58fa-49fa-901d-4152017f12e7)

We were given a binary and a file which supposedly is the encrypted flag

This challenge was really easy but I was intimidated by the challenge description and stopped tryin to solve it after making my first attempt 😥

But then someone solved it and I was like whaaaaat!

I then decided to check it again

Running the binary would return this error
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e9db6f2a-9d32-4604-84d0-373559fb8c0c)

This is a common complain in rev/pwn challenges when there's no `flag.txt` file present in the current directory

So I just add the file and put some content in it
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f228f59e-941f-4c60-ac0e-43cca4626bff)

It would write the encrypted content to a file named `enc`

Let's decompile it in Ghidra to see what this binary has to offer!

Looking at the available functions I could tell it's a rust binary cause ghidra was able to identify it

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aae03de2-122a-47ba-a433-7a9036f21f92)

Moving over to the main function shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/80e0b372-ec2a-4d35-baf0-481838c04594)

I don't know rust but this looks like it's calling `sugerplum::main`, clicking that shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/868e1295-50a0-46bf-9c84-7491eba40ca8)

```rust

/* sugarplum::main */

undefined8 sugarplum::main(void)

{
  undefined8 uVar1;
  undefined auVar2 [16];
  undefined8 local_148;
  undefined4 local_13c;
  int local_138;
  undefined4 local_134;
  undefined8 local_130;
  undefined local_128 [16];
  undefined local_118 [24];
  long local_100;
  undefined8 local_f8;
  undefined local_f0 [16];
  undefined local_e0 [28];
  undefined4 local_c4;
  int local_c0;
  undefined4 local_bc;
  undefined8 local_b8;
  undefined local_b0 [16];
  long local_a0;
  undefined local_98 [52];
  undefined4 local_64;
  undefined8 local_50;
  char *local_48;
  undefined8 local_40;
  undefined4 local_34;
  long local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined8 local_18;
  char *local_10;
  undefined8 local_8;
  
  std::fs::File::open(local_128,
                      "flag.txtextern \"NulErrorencYour Data Is Secured!\nError: \n/rustc/cc66ad4689 55717ab92600c770da8c1601a4ff33/library/core/src/alloc/layout.rs"
                      ,8);
  <>::branch(&local_138,local_128);
  if (local_138 == 0) {
    local_64 = local_134;
    local_13c = local_134;
                    /* try { // try from 0010b7d9 to 0010b7e5 has its CatchHandler @ 0010b81d */
    alloc::vec::Vec<T>::new(local_118);
                    /* try { // try from 0010b833 to 0010b850 has its CatchHandler @ 0010b862 */
    <>::read_to_end(local_f0,&local_13c,local_118);
                    /* try { // try from 0010b878 to 0010b950 has its CatchHandler @ 0010b862 */
    <>::branch(&local_100,local_f0);
    if (local_100 == 0) {
      local_50 = local_f8;
      local_10 = 
      "cafebabe1337007flag.txtextern \"NulErrorencYour Data Is Secured!\nError: \n/rustc/cc66ad46895 5717ab92600c770da8c1601a4ff33/library/core/src/alloc/layout.rs"
      ;
      local_8 = 0xf;
      local_48 = 
      "cafebabe1337007flag.txtextern \"NulErrorencYour Data Is Secured!\nError: \n/rustc/cc66ad46895 5717ab92600c770da8c1601a4ff33/library/core/src/alloc/layout.rs"
      ;
      local_40 = 0xf;
      auVar2 = <>::deref(local_118);
      xor_encrypt(local_e0,auVar2._0_8_,auVar2._8_8_,
                  "cafebabe1337007flag.txtextern \"NulErrorencYour Data Is Secured!\nError: \n/rustc /cc66ad468955717ab92600c770da8c1601a4ff33/library/core/src/alloc/layout.rs"
                  ,0xf);
                    /* try { // try from 0010b953 to 0010b96b has its CatchHandler @ 0010b980 */
      std::fs::File::create
                (local_b0,
                 "encYour Data Is Secured!\nError: \n/rustc/cc66ad468955717ab92600c770da8c1601a4ff33 /library/core/src/alloc/layout.rs"
                 ,3);
                    /* try { // try from 0010b996 to 0010b9aa has its CatchHandler @ 0010b980 */
      <>::branch(&local_c0,local_b0);
      if (local_c0 == 0) {
        local_34 = local_bc;
        local_c4 = local_bc;
                    /* try { // try from 0010b9cf to 0010b9db has its CatchHandler @ 0010ba20 */
        auVar2 = <>::deref(local_e0);
                    /* try { // try from 0010ba36 to 0010badc has its CatchHandler @ 0010ba20 */
        uVar1 = std::io::Write::write_all(&local_c4,auVar2._0_8_,auVar2._8_8_);
        local_a0 = <>::branch(uVar1);
        if (local_a0 == 0) {
          core::fmt::Arguments::new_const(local_98,&DAT_0015ff38,1);
          std::io::stdio::_print(local_98);
                    /* try { // try from 0010bae8 to 0010baf4 has its CatchHandler @ 0010b980 */
          core::ptr::drop_in_place<>(&local_c4);
                    /* try { // try from 0010baf7 to 0010bb03 has its CatchHandler @ 0010b862 */
          core::ptr::drop_in_place<>(local_e0);
                    /* try { // try from 0010bb06 to 0010bb12 has its CatchHandler @ 0010b81d */
          core::ptr::drop_in_place<>(local_118);
          core::ptr::drop_in_place<>(&local_13c);
          return 0;
        }
        local_30 = local_a0;
        local_148 = <>::from_residual(local_a0,&PTR_s_src/main.rs_0015ff48);
                    /* try { // try from 0010bb35 to 0010bb41 has its CatchHandler @ 0010b980 */
        core::ptr::drop_in_place<>(&local_c4);
      }
      else {
        local_28 = local_b8;
                    /* try { // try from 0010b9f8 to 0010ba03 has its CatchHandler @ 0010b980 */
        local_148 = <>::from_residual(local_b8,&PTR_s_src/main.rs_0015ff60);
      }
                    /* try { // try from 0010bb44 to 0010bb50 has its CatchHandler @ 0010b862 */
      core::ptr::drop_in_place<>(local_e0);
    }
    else {
      local_20 = local_f8;
      local_148 = <>::from_residual(local_f8,&PTR_s_src/main.rs_0015ff78);
    }
                    /* try { // try from 0010bb6a to 0010bb76 has its CatchHandler @ 0010b81d */
    core::ptr::drop_in_place<>(local_118);
    core::ptr::drop_in_place<>(&local_13c);
  }
  else {
    local_18 = local_130;
    local_148 = <>::from_residual(local_130,&PTR_s_src/main.rs_0015ff90);
  }
  return local_148;
}
```

Honestly I had no idea what that is exactly but thanks to `debug_symbols` being enabled I was able to identify what that does

The first thing the binary would do is to try open the `flag.txt` file using:

```rust
std::fs::File::open
```

Then it eventually calls the `xor_encrypt` function

```rust
undefined8 *
sugarplum::xor_encrypt
          (undefined8 *param_1,undefined8 param_2,undefined8 param_3,long param_4,ulong param_5)

{
  ulong uVar1;
  undefined auVar2 [16];
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined local_80 [24];
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined local_50 [16];
  undefined8 local_40;
  undefined8 local_38;
  long local_30;
  ulong local_28;
  byte local_9;
  ulong local_8;
  
  local_40 = param_2;
  local_38 = param_3;
  local_30 = param_4;
  local_28 = param_5;
  alloc::vec::Vec<T>::with_capacity(&local_b0);
                    /* try { // try from 0010b581 to 0010b585 has its CatchHandler @ 0010b5a1 */
  auVar2 = core::slice::<impl[T]>::iter(param_2,param_3);
                    /* try { // try from 0010b5b7 to 0010b74a has its CatchHandler @ 0010b5a1 */
  core::iter::traits::iterator::Iterator::enumerate(local_80,auVar2._0_8_,auVar2._8_8_);
  <>::into_iter(&local_98,local_80);
  local_68 = local_98;
  local_60 = local_90;
  local_58 = local_88;
  while( true ) {
    auVar2 = <>::next(&local_68);
    local_8 = auVar2._0_8_;
    if (auVar2._8_8_ == (byte *)0x0) {
      *param_1 = local_b0;
      param_1[1] = local_a8;
      param_1[2] = local_a0;
      return param_1;
    }
    local_9 = *auVar2._8_8_;
    local_50 = auVar2;
    if (param_5 == 0) break;
    uVar1 = local_8 % param_5;
    if (param_5 <= uVar1) {
      core::panicking::panic_bounds_check(uVar1,param_5,&PTR_s_src/main.rs_0015ff20);
      goto LAB_0010b70f;
    }
    alloc::vec::Vec<T,A>::push(&local_b0,local_9 ^ *(byte *)(param_4 + uVar1));
  }
  core::panicking::panic
            ("attempt to calculate the remainder with a divisor of zerocafebabe1337007flag.txtextern  \"NulErrorencYour Data Is Secured!\nError: \n/rustc/cc66ad468955717ab92600c770da8c1601a 4ff33/library/core/src/alloc/layout.rs"
             ,0x39,&PTR_s_src/main.rs_0015ff08);
LAB_0010b70f:
  do {
    invalidInstructionException();
  } while( true );
}
```

This was where I had issue since I didn't understand that, I was feeling maybe it would not just "xor" only cause the challenge description was too intimidating

Next I left this and decided to play with the binary and it's output

I assumed it would just `xor` and if that's the case that means the key can be retrieved because xor is reversible

Since I know the plaintext and ciphertext I can just xor them both to retrieve the key
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7591bcde-b57e-4a3c-b51b-1affa4afbd66)

Ok that looks right, with that I just wrote a script to decrypt the flag

Here's my solve script: [link](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/reverse/Suger%20Plum/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/329ae3e6-b031-425d-b6e9-c3f64179a77f)

```
Flag: urchinsec{I4M_santas_f4v0rit1_1eELF}
```

That's all for the reverse engineering I did! I remember that I spent a lot of time trying to solve `Albaster` but it refused to let me solve it 😂

### Cryptography

#### Minstix

We were given three files `main.py, pew.key, secret_zip.fzip`

Checking the content of `main.py` shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2b074971-02c0-4894-b49c-e7c969baa991)

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

zip_filename = "fernet.zip"
with open(zip_filename, 'rb') as file:
    file_data = file.read()

encrypted_data = cipher_suite.encrypt(file_data)

encrypted_zip_filename = "secret_zip.fzip"
with open(encrypted_zip_filename, 'wb') as encrypted_zip_file:
    encrypted_zip_file.write(encrypted_data)

with open("pew.key", "wb") as key_file:
    key_file.write(key)
```

Looking at this code we can see it implements Fernet cryptography and then it encryptes the zipfile data using the generated key and writes the encrypted value content to `secret_zip.fzip`

The interesting thing about this challenge which makes it easy is that the key is given which is `pew.key` file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/effdabc4-ed0d-4fe2-9d4b-5551ccce1d38)

So we can easily just decrypt it 

Looking at the documentation I found how to decrypt it: [docs](https://cryptography.io/en/latest/fernet/)

And I was able to implement it and decrypt the fzip file, here's my solve script:

```python
from cryptography.fernet import Fernet

with open("secret_zip.fzip", "rb") as fp:
    file_data = fp.read()

with open("pew.key") as fp:
    key = fp.read()

f = Fernet(key)
d = f.decrypt(file_data)

with open('dump.zip', 'wb') as fp:
    fp.write(d)
```

Running it works but when I tried to unzip the zip file it requires a password
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2612c7cf-e7fb-4b9c-bbb3-dc96375c6f4f)

Luckily the password was easily cracked by JohnTheRipper
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/f0def6d4-2997-40f3-a5fe-0bc68f90e579)

The password is: `dexter` and now we can unzip it and get our flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/379244b3-3352-4d0d-a518-950420142d58)

```
Flag: urchinsec{FERNET_SYMMETRIC_ENCRYPTION_WITHZIP_FILES}
```

#### SantaZIP

Hmmmm this challenge was an interesting one, I never planned on doing anything crypto related cause that isn't what I do

But in this ctf I was able to solve all crypto challenges which surprised me 😅

We were given three files: `app.py, santazip.py, flag.zip`

Checking the content of `app.py` shows this
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/4301703f-bba6-4b62-8702-10ada55452e5)

```python
from santazip import SantaZip

zip_object = SantaZip("flag.txt", "flag.zip", "[REDACTED]")
print(zip_object.generate_zip_file())
```

So this would import the Class `SantaZip` from the `santazip.py` file, then it would pass in `flag.txt, flag.zip, testing` as the paramater

It would then generate the encrypted zip file

At this point there's nothing we know aside that it would generate a zip so let's take a look at the `santazip.py` file
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/897ad8f1-92b4-4394-9102-08a459b3e6c5)

```python
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import zlib
import struct

class SantaZip(object):
    def __init__(self, file_to_zip, zip_output, password):
        self.file_to_zip = file_to_zip
        self.zip_output = zip_output
        self.password = password

    def generate_zip_file(self):
        try:
            password = self.password
            salt = get_random_bytes(16)
            iv = get_random_bytes(16)
            key = PBKDF2(password, salt, dkLen=32, count=1000000)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            with open(self.file_to_zip, "rb") as input_file:
                plaintext = input_file.read()

            compressed_data = zlib.compress(plaintext)
            padded_data = compressed_data + b' ' * (16 - len(compressed_data) % 16)
            ciphertext = cipher.encrypt(padded_data)

            with open(self.zip_output, "wb") as output_file:
                output_file.write(salt)
                output_file.write(iv)
                output_file.write(ciphertext)
            
            return f"{self.file_to_zip} is zipped into {self.zip_output}"
        except Exception as e:
            return f"Error : {e}"
```

So this might look hard or no? But if you look at it well you'd see it's pretty easy

I'll be starting from the `__init__` method
- It defines the parameter being passed into this class as the `file_to_zip, zip_output, password` respectively
  - So this means the file to zip is: `flag.txt`, the zip output should be: `flag.zip` and finally the password is unknown since they REDACT it (too bad)
- The next portion is the function which would generate the zip file
  - First it would set the password as the provided password which in this case we don't know
  - The iv and salt are 16 random bytes (really secure i think)
  - The key is going to be generated using PBKDF2 with salt as the random 16 bytes
  - Then the content of `flag.txt` is stored in variable `plaintext`
  - It compresses the plaintext using `zlib`
  - Then it pads the compressed data with space character
  - Then the ciphertext is formed by using AES CBC mode where the key is the generated PBKDF2 key and the iv is the 16 random bytes
  - It would write the salt, iv and ciphertext to the zip output file

At this point the code really looks secured right?

Next thing I checked was how to decrypt AES CBC encrypted data and found the documentation: [docs](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html)

So the step is really the same except this time we use `cipher.decrypt`

```python
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)
```

Look well at this point we can see that the iv is known and not just that but also the salt

With the iv being known means we can potentially decrypt the ciphertext but that can only occur when we know the key

Looking back at the code the key is generated using this:

```python
key = PBKDF2(password, salt, dkLen=32, count=1000000)
```

Ok this is good because we know the salt meaning there's possiblilty of us brute forcing the password (which happens to be the hint xD)

The idea is going to be just to recreate the process but this time we are decrypting the ciphertext where the password being used is from brute forcing

Now where is the salt & iv?

Look here:

```python
with open(self.zip_output, "wb") as output_file:
    output_file.write(salt)
    output_file.write(iv)
    output_file.write(ciphertext)
```

Since the salt and iv are 16 bytes that means we can differientiate it from the ciphertext

With that said here's a screenshot of my solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/crypto/Santa%20Zip/solve.py)
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/7d063126-e4db-4c09-a02b-d7e6ae3d0156)

Running it gives the flag after about ~10mins
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/40f9218e-b375-43f4-9b16-ba94dbd761f5)

```
Flag: urchinsec{sant4_zip_1s_th3_new_ZIP}
```

#### Honey SEA

From the challenge name it's clearly an AES challenge

After solving the first AES challenge I had the courage to do this one and it turned out easy too

We were two files: `enc.py, cipher`

Here's the content of `enc.py`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/2c571d06-c1fc-4e43-bcdb-20342d522918)

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import binascii

def generate_key():
    return os.urandom(16)

def generate_iv():
    return os.urandom(16)

def encrypt_flag(flag, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(flag.encode(), 16))
    return encrypted

def generate_signature(iv, key):
    signature_bytes = [a ^ b for a, b in zip(iv, key[::-1])] # abc ^ cde ==> abc ^ edc
    signature_hex = binascii.hexlify(bytearray(signature_bytes)).decode() # convert xored result to hex
    return signature_hex

def encrypt_flag_with_signature(flag, key, iv):
    encrypted_data = encrypt_flag(flag, key, iv)
    signature = generate_signature(iv, key)
    iv_hex = iv.hex()[4:] 
    encrypted_hex = encrypted_data.hex()
    ciphertext = iv_hex + encrypted_hex + signature
    return {"cipher": ciphertext}

def main():
    FLAG = "urchinsec{Fake_Flag}"
    KEY = generate_key()
    IV = generate_iv()

    encrypted_flag = encrypt_flag_with_signature(FLAG, KEY, IV)
    print(encrypted_flag)

if __name__ == "__main__":
    main()
```

It looks intimidating at first but after I looked at it well it turned out similar to the previous one

Let's start from the main function 🙂

- It defines three variables `FLAG, IV & KEY`
  - The FLAG is of cause the flag 😵‍💫, the IV & KEY are randomly generated by calling the `generate_*` function which returns 16 random bytes
- It calls the `encrypt_flag_with_signature` function passing the `flag, key & iv` as the parameter

Here's what this function does

- First it has a variable `encrypted_data` which holds the return value from calling the `encrypted_data` function passing the `flag, key & iv ` as the parameter
  - This function `encrypted_data` implements AES CBC mode and returns the encrypted data
- Next the variable `signature` hold the value return from calling the `generate_signature` function passing the `iv & key` as the parameter
  - This function basically would xor each byte of the iv with each byte of the reversed key value
  - Then it's converted to hex and that's the signature
- Next it converts the iv bytes to hex ignoring the first 4 bytes which means only 12 bytes are converted to hex (it's stored as iv_hex)
- Then it converts the encrypted data to hex
- Finally the ciphertext is the concatenation of the iv_hex, encrypted_hex and the signature
- And it returns the ciphertext valye

Quite an encryption you might say 🥷

First what came to my mind was how would I decrypt the ciphertext?

Now to do that we need the iv and key

But looking at the code it gave us the iv but how about the key?

If you notice the `generate_signature` function it xors the key and iv together, the only catch there is that the key is reversed before it's xored but is that really a problem?

Well that isn't a problem cause we can still recover the key since the signature and iv are known

So to recover the key we can do this:

```python
xor(signature, iv)[::-1]
```

What next? If you notice the given iv isn't complete cause it's missing 4 bytes but that's not a problem cause we can brute force smartly by using the `itertools` python module

At this point we know the iv & key meaning we can just decrypt the ciphertext 

The ciphertext should be this:

```python
ct = cipher[28:-32]
```

Cause the signaure is 16 bytes and the iv is 14 bytes 🙂

Finally the solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/crypto/Honey%20SEA/solve.py) ❤️‍🔥
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/3ec19d20-304d-4b8d-8368-62fa0560e273)

Running it gives the flag after about ~2mins
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/e394bf30-c50c-41d7-986f-d4c2d93ff2a9)

```
Flag: urchinsec{H4acker_L00Ks_A35_y0Y}
```

#### By Polar RSA

We were given two files: `cipher, By_Polar_RSA.py`

Here's the content of `By_Polar_RSA.py`
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/459d5c3a-992f-4016-b5e8-50169cf344b7)

```python
from Crypto.Util.number import getPrime, long_to_bytes
import random
import sympy.ntheory as nt

def g_prime(bit_length):
    return getPrime(bit_length)

def g_rsa_pair(bit_length):
    p = g_prime(bit_length)
    q = nt.nextprime(p)
    
    x, y = 1337, 5000
    for _ in range(random.randint(x, y)):
        q = nt.nextprime(q)

    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi_N)  
    public_key = (N, e)
    private_key = (N, d)
    return public_key, private_key

def enryption(message, public_key):
    N, e = public_key
    pt = btl(message.encode())
    ct = pow(pt, e, N)
    return ct

bit_length = 1024
public_key, _ = g_rsa_pair(bit_length)
msg = "urchinsec{Fake_Flag}"
ciphertext = enryption(msg, public_key)
print(f"n: {public_key[0]}")
print(f"e: {public_key[1]}")
print(f"cipher: {ciphertext}")
```

So this challenges after I looked at it I didn't find anything weird except this:

```python
q = nt.nextprime(p)

for _ in range(random.randint(x, y)):
    q = nt.nextprime(q)
```

I looked up to google and found a similar thing from this writeup: [reference](https://ctftime.org/writeup/38102)

And it did Fermet Attack

I edited the script being used there to use the cipher values given to us
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a3e30564-bd81-4d64-9801-517137d94b5c)

Running the [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/crypto/By%20Polar%20RSA/solve.py) gave the flag
![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/127d1f1b-511d-49ed-800c-7f61c8021d1d)

```
Flag: urchinsec{1t's_Qu1t3_Th3_H4rd_BUt_E4syy5}
```

### Binary Exploitation

The challenges here were very few and I was able to solve just one easy one out of two

The second pwn was Heap related and I have no idea about Heap that's why I couldn't solve it

As to regarding the first one I'm too lazy to make writeup but incase you're interested in reading the "general way" I'd use to solve it check here: [link](https://h4ckyou.github.io/posts/bof/index.html)

The challenge idea was just a basic variable overwrite to `0xcafebabe` at offset 42

Here's the solve [script](https://github.com/h4ckyou/h4ckyou.github.io/blob/main/posts/ctf/urchinsec23/pwn/BOF/solve.py)

Welp that's all xD

I played as `@rizz` 🙂

![image](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/aa3e5b95-6373-493f-9ce9-c69069021017)

Till next time

![Alt Text](https://github.com/h4ckyou/h4ckyou.github.io/assets/127159644/a82acdb6-6a75-43eb-8107-211bbbeccfc4)


