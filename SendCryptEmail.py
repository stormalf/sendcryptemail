#!/usr/bin/python3
# -*- coding: utf-8 -*-
import smtplib
import os
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
import argparse
from pycryptofile import pyCryptoFile



__version__ = "1.0.0"

#Constants
SERVER = 'smtp.gmail.com'
PORT = 587
DFTEXT = '.enc'

#return version
def SendCryptEmailVersion():
    return f"SendCryptEmail version : {__version__}"

#return encrypted data from a file using public ssh key
#note that pyCryptoFile generates a file.enc for encrypted file
def cryptedAttachment(file, keyfile):
    pyCryptoFile.pyCryptoFile(file, mode="encrypt", keyfile=keyfile, outputfile="")  
    encryptedfile = file + DFTEXT
    with open(encryptedfile, "rb") as f:
        data = f.read()     
    return data
        
#return MIMEapplication with attachment crypted or not        
def emailAttachment(attachment, crypted, keyfile):
    filename = attachment[0]
    data = b''
    if crypted == "yes":
        data=cryptedAttachment(filename, keyfile)
        filename = filename + DFTEXT
    else:            
        with open(filename, "rb") as f:
            data = f.read()
    part = MIMEApplication(
        data,
        Name=basename(filename)
    )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
    return part       

#return all emails separated by semicolon (to, cc, bcc)
def formatEmail(targets):
    toaddr = []
    for target in targets: 
        toaddr.append(target)
    return toaddr

#check if received arguments are correct
def check_arguments(args):
    isOk = True
    if args.keyfile == "" and (args.passwordcrypted == "yes" or args.bodycrypted == "yes" or args.attachmentcrypted == "yes"):
        print("at least one crypted option, keyfile required! ")
        isOk = False
        return isOk
    return isOk

#check if user is set
def check_user(user):
    isOk = True
    if user == '':
        useremail = os.environ.get('SENDCRYPTEMAIL_USER')
        if useremail == None:
            print("user email required! no user parameter received neither environment variable SENDCRYPTEMAIL_USER")
            isOk = False
            return isOk, useremail
    else:
        useremail = user
    return isOk, useremail    

#check if password is set
def check_password(password, crypted):
    isOk = True
    if password == '':
        pwd = os.environ.get('SENDCRYPTEMAIL_PASSWORD')
        if pwd == None:
            print("password required! no password received neither environment variable SENDCRYPTEMAIL_PASSWORD")        
            isOk = False
            return isOk, pwd
    else:
        pwd = password    
    if crypted == "yes":
        privkey = pyCryptoFile.get_private_key()
        try: 
            decryptedpassword = pyCryptoFile.decrypt_private_key(pwd, privkey)
        except:
            print("error during decrypting password! check that your password had crypted using pycryptofile!")            
            isOk = False
            return isOk, pwd
        pwd = str(decryptedpassword, "utf-8")
        #remove the /n
        pwd = pwd.replace('\n', '')
    return isOk, pwd   

#format the body that can be encrypted or not         
def format_body(body, crypted):
    fbody = body
    body_msg = ""
    if fbody == '':
        body_msg = "test"
    else:        
        if crypted == "yes":
            fbody = pyCryptoFile.pyCryptoFile(body, mode="encrypt", keyfile=args.keyfile, outputfile="")
            body_msg = str(fbody, "utf-8")       
        else:
            with open(body, 'rb') as f:
                fbody = f.read()        
            body_msg = str(fbody, "utf-8") 
    return body_msg            


#check and if ok send email crypted or not depending the value for each parameter
# send_message works better than sendmail
def main(args):
    isOk = check_arguments(args)
    if not isOk:
        return
    isOk, useremail = check_user(args.user)        
    if not isOk:
        return
    isOk, password = check_password(args.password, args.passwordcrypted)
    if not isOk:
        return
    #formatting email    
    msg = MIMEMultipart()    
    msg['From'] = useremail
    toaddr = formatEmail(args.target)
    cc = formatEmail(args.carboncopy)
    bcc = formatEmail(args.blindcarboncopy)
    msg['To'] = ",".join([item[0] for item in toaddr])
    msg['Cc'] = ",".join([item[0] for item in cc])
    msg['Bcc'] = ",".join([item[0] for item in bcc])
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = args.subject
    body_msg = format_body(args.body, args.bodycrypted)
    msg.attach(MIMEText(body_msg, "plain", "utf-8"))   
    if args.attachment != []: 
        for attachment in args.attachment:
            part = emailAttachment(attachment, args.attachmentcrypted, args.keyfile)
            msg.attach(part)
    # print(body_msg)            
    # return
    smtpServer = SERVER
    smtpPort = PORT        
    session = smtplib.SMTP(smtpServer, smtpPort)
    #session = smtplib.SMTP_SSL(smtpServer, smtpPort)
    session.ehlo()
    session.starttls() #enable security
    session.login(useremail, password) #login with mail_id and password
    #session.sendmail(useremail, recipients, msg.as_string())
    session.send_message(msg)
    session.close()
    print('Mail Sent')


if __name__== "__main__":
    description = "SendCryptEmail is a python3 program that encrypts and sends emails using ssh key encryption\n"
    description = description + "Note that the content and attachment should be crypted using the target user public ssh key\n"
    description = description + "The target user could easily decrypt using his private ssh key\n"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-V', '--version', help='Display the version of SendCryptEmail', action='version', version=SendCryptEmailVersion())
    parser.add_argument('-t', '--target', help='target email', action='append',  nargs='+', required=True)
    parser.add_argument('-cc', '--carboncopy', help='carbon copy email', action='append',  nargs='*', default=[], required=False)
    parser.add_argument('-bcc', '--blindcarboncopy', help='blind carbon copy email', action='append',  nargs='*', default=[], required=False)    
    parser.add_argument('-u', '--user', help='your email if not provided use SENDCRYPTEMAIL_USER environment variable', default='', required=False)    
    parser.add_argument('-p', '--password', help='your gmail password or your gmail app password if not provided use SENDCRYPTEMAIL_PASSWORD environment variable', default='', required=False)        
    parser.add_argument('-pc', '--passwordcrypted', help='if yes assume that your password is crypted by pycryptofile', default="yes", choices=["yes", "no"], required=False)            
    parser.add_argument('-a', '--attachment', help='attachment file', default=[], required=False, action='append',  nargs='+')
    parser.add_argument('-ac', '--attachmentcrypted', help='if yes attachment file will be crypted by pycryptofile and attached', default="yes", choices=["yes", "no"], required=False)
    parser.add_argument('-s', '--subject', help='Email subject', default="test", required=False) 
    parser.add_argument('-b', '--body', help='body template file', default="", required=False)
    parser.add_argument('-bc', '--bodycrypted', help='yes to crypt the body content too by pycryptofile', default="yes", choices=["yes", "no"], required=False)        
    parser.add_argument('-k', '--keyfile', help='target user public ssh key file', default="", required=False)
    parser.add_argument('-S', '--server', help='smtp server', default=SERVER, required=False)    
    parser.add_argument('-P', '--port', help='smtp port', default=PORT, required=False)    
    args = parser.parse_args()
    main(args)
   



