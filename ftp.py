import ftplib,os
  
def up():
    ftp.connect("ftpupload.net",21)
    ftp.login("if0_39451019","110205gyh")
    ftp = ftplib.FTP()
    ftp.cwd("htdocs")
    filename = "savedata_vp.pkl"
    with open(filename, 'rb') as file:
        ftp.storbinary(f'STOR {filename}', file)
    ftp.quit()
def down():
    ftp = ftplib.FTP()
    ftp.connect("ftpupload.net",21)
    ftp.login("if0_39451019","110205gyh")
    ftp.cwd("htdocs")
    filename = 'savedata_vp.pkl'
    with open(filename, 'wb') as file:
        ftp.retrbinary(f'RETR {filename}', file.write)
    ftp.quit()
