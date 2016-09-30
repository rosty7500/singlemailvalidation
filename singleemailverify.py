import csv
import requests
import dns.resolver
import socket
import smtplib

def verifying_emails(i,domain):
        email_details = {}
        record = dns.resolver.query(domain, 'MX')
        mxRecord = record[0].exchange
        mxRecord = str(mxRecord)

        # Get local server hostname
        host = socket.gethostname()

        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)

        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(i))
        server.quit()
        print("Status code:", code)
        email_details['Email']= i
        email_details['Status']= code

        with open('emailfiltered.csv', 'a', newline='') as csvfile:
            fieldnames = ['Email', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(email_details)
        return code, i


with open('directemailvalidation.csv') as csv_file:
    reader = csv.reader(csv_file)
    for records in reader:
        for i in records:
            print("Email id to be checked :", i)
            splitAddress = i.split('@')
            domain = str(splitAddress[1])
            try:
                r = requests.get("http://www." +domain)
                x = dns.resolver.query(domain, 'MX')
                if len(x) > 0:
                    try:
                        value = verifying_emails(i,domain)
                        print('Completed')
                    except:
                        print('error')
            except:
                print(domain,"-- This domain is Invalid")
                break
                pass


