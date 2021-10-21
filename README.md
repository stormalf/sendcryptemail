# SendCryptEmail

SendCryptEmail tool sends emails that can be encrypted using ssh keys.
Use the target user public ssh key that it will be able to decrypt the email and/or attachments using his private key.

---

python3 SendCryptEmail.py --help

    usage: SendCryptEmail.py [-h] [-V] -t TARGET [TARGET ...]
                            [-cc [CARBONCOPY [CARBONCOPY ...]]]
                            [-bcc [BLINDCARBONCOPY [BLINDCARBONCOPY ...]]] [-u USER]
                            [-p PASSWORD] [-pc {yes,no}] [-a ATTACHMENT [ATTACHMENT ...]]
                            [-ac {yes,no}] [-s SUBJECT] [-b BODY] [-bc {yes,no}]
                            [-k KEYFILE] [-S SERVER] [-P PORT]

    SendCryptEmail is a python3 program that encrypts and sends emails using ssh key
    encryption Note that the content and attachment should be crypted using the target
    user public ssh key The target user could easily decrypt using his private ssh key

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of SendCryptEmail
    -t TARGET [TARGET ...], --target TARGET [TARGET ...]
                            target email
    -cc [CARBONCOPY [CARBONCOPY ...]], --carboncopy [CARBONCOPY [CARBONCOPY ...]]
                            carbon copy email
    -bcc [BLINDCARBONCOPY [BLINDCARBONCOPY ...]], --blindcarboncopy [BLINDCARBONCOPY [BLINDCARBONCOPY ...]]
                            blind carbon copy email
    -u USER, --user USER  your email if not provided use SENDCRYPTEMAIL_USER environment
                            variable
    -p PASSWORD, --password PASSWORD
                            your gmail password or your gmail app password if not provided
                            use SENDCRYPTEMAIL_PASSWORD environment variable
    -pc {yes,no}, --passwordcrypted {yes,no}
                            if yes assume that your password is crypted by pycryptofile
    -a ATTACHMENT [ATTACHMENT ...], --attachment ATTACHMENT [ATTACHMENT ...]
                            attachment file
    -ac {yes,no}, --attachmentcrypted {yes,no}
                            if yes attachment file will be crypted by pycryptofile and
                            attached
    -s SUBJECT, --subject SUBJECT
                            Email subject
    -b BODY, --body BODY  body template file
    -bc {yes,no}, --bodycrypted {yes,no}
                            yes to crypt the body content too by pycryptofile
    -k KEYFILE, --keyfile KEYFILE
                            target user public ssh key file
    -S SERVER, --server SERVER
                            smtp server
    -P PORT, --port PORT  smtp port

Examples :

sending an email without encrypting the body but encrypting the attachments (not that the carbon copy and the blind carbon copy are samples no way that all the receivers decrypt the attachment without the private key corresponding to the public key used to encryp!)

    python3 SendCryptEmail.py -t fg1@gmail.com -cc fg2@gmail.com -cc fg3@gmail.com -bcc fg4@gmail.com -b t1 -k ~/.ssh/id_rsa.pub -s "test email by python encrypted mode" -bcc fg5@gmail.com -bcc fg6@gmail.com -a test.gif -a test.
    pdf -u sender@gmail.com -bc no

# release notes

1.0.0 initial version use pycryptofile==1.0.8

# some ideas for someone that want to improve it

- adding gpg as a new encrypt way
- adding a basic encryption using a secret key
- giving the possibility to encrypt only some attachment by having some tuple attachment encrypted(yes/no)
