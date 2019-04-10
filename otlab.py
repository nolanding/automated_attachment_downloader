import smtplib
import time
import imaplib
import email
import os
from Crypto import Random
from Crypto.Cipher import AES
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")
def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    r=dec.decode("utf-8")
    return r
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

password=decrypt_file('test.txt.enc',key)
detach_dir='/Users/deekshachandwani/Desktop/lab_project'
mail = imaplib.IMAP4_SSL('imap.gmail.com')
(retcode, capabilities) = mail.login('rathiruchi10@gmail.com',password)
mail.list()
mail.select('inbox')

n=0
(retcode, messages) = mail.search(None, '(UNSEEN)')
if retcode == 'OK':

   for num in reversed(messages[0].split()) :
      print ('Processing ')
      n=n+1
      typ, data = mail.fetch(num,'(RFC822)')
      emailbody=data[0][1]
      original = email.message_from_bytes(emailbody)
      #print(original['From'])
      for part in original.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(detach_dir, fileName)
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            break
      typ, data = mail.store(num,'+FLAGS','\\Seen')
print (n)
   
