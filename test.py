import socket
import getpass
import poplib
#import parse email action required python parse module
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

s = socket.socket()
s = 'pop.gmail.com'
print('----------------------------------------------------------------------')
#input email address, password
email = input('Enter Email: ')
p = getpass.getpass('Enter Password: ')
#connect to server:
s = poplib.POP3_SSL(s,'995')
#debug info between client & server
s.set_debuglevel(1)
#get welcome message from server
welcome_msg = s.getwelcome().decode('utf-8')
print(s.getwelcome().decode('utf-8'))

#account authentication
s.user(email)
s.pass_(p)
print(' >>User authenticated\n')

#resetting all previous deleted messages
s.rset()
print(' >>Deleted messages will be restore...')
#stat() func return email count and occupied disk size
print(' >>Messages: %s. Size: %s' %s.stat())
#list() func return all email list
resp, mails, octets = s.list()
print(mails)
print('')

#encoding charset of email content
def guess_charset(msg):
    # get charset from message object.
    charset = msg.get_charset()
    # if can not get charset
    if charset is None:
       #get message header content-type value & retrieve the charset from the value
       content_type = msg.get('Content-Type', '').lower()
       pos = content_type.find('charset=')
       if pos >= 0:
          charset = content_type[pos + 8:].strip()
    return charset

#retrieve the newest email index number
index = len(mails)
#s.retr func get email's content  w/ index variable value index number
resp, lines, octets = s.retr(index)
"""
lines stores each line of the original text
so that the original text of entire message use join func & lines variable
"""
msg_content = b'  \r\n'.join(lines).decode("utf-8")
#parse the email object to a message object
msg = Parser().parsestr(msg_content)

print(' >>Reading email message...')
#get email 'from, to, subject' value
email_from = msg.get('From')
email_to = msg.get('To')
email_subject = msg.get('Subject')
print(' >>From: ' + email_from)
print('   To: ' + email_to)
print('   Subject: ' + email_subject)
content_type = msg.get_content_type() 
#if plain text or html content type.
if content_type=='text/plain' or content_type=='text/html':
    #email content
    content = msg.get_payload()
    #content string charset
    charset = guess_charset(msg)
    #decode the content with charset if provided
    print('' +msg.get_payload())
    print('')
else:
    print('   <Failed to retrieve attachment>\n')

#delete email directly by email index
s.dele(index)
print(' >>This message will be deleted immediately!\n')

#close connection
s.quit()
print(' >>Oya? Jumpa lagii')
print('----------------------------------------------------------------------')
s.close()
