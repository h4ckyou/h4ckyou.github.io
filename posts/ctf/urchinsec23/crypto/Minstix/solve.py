from cryptography.fernet import Fernet

with open("secret_zip.fzip", "rb") as fp:
    file_data = fp.read()

with open("pew.key") as fp:
    key = fp.read()

f = Fernet(key)
d = f.decrypt(file_data)

with open('dump.zip', 'wb') as fp:
    fp.write(d)

# unzip the dump.zip file with password: dexter
