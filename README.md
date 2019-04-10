# automated_attachment_downloader
A script which runs after every x minutes and that accesses your email account by decrypting the password that once you had entered and then checks up for any attachments and if present,downloads it on the local machine. After accessing the email, it marks the email read so that when the loop runs after next x minutes, it won't download the same attachment.
