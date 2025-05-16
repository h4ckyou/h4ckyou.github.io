import os
import subprocess

base_dir = "/usr/share/wordlists/seclists/Passwords/"

hash_file = "hash.txt"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".txt"):
            wordlist_path = os.path.join(root, file)
            print(f"[*] Trying wordlist: {wordlist_path}")
            try:
                subprocess.run(["john", f"--wordlist={wordlist_path}", hash_file], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[!] Failed on {wordlist_path}: {e}")
