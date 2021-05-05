#!/usr/bin/env python3
import os
import sys
import yaml
import smtplib
import argparse
from email.message import EmailMessage

# Parse arguments
parser = argparse.ArgumentParser(description="Get difference between 2 files. One from stdin and one from argv[1].")
parser.add_argument("file", help="Old file to campare against your new file (stdin)")
parser.add_argument("-e", "--email", help="Email to alert of new data found")
parser.add_argument("-s", "--subject", help="Subject of the email")
parser.add_argument("-c", "--config", help="Yaml file containing your email and password to login")

args        = parser.parse_args()
subject     = args.subject
email       = args.email
old_file    = args.file
yaml_config = args.config

def sendmail(results):
    with open(yaml_config, 'r') as f:
        yaml_data = yaml.safe_load(f)

    login_username = yaml_data["username"][0]
    login_password = yaml_data["password"][0]
    
    msg = f"Subject: {subject}\n\n"

    for result in results:
        msg = msg + result

    # Send the message
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(login_username, login_password)
        s.sendmail(login_username, email, msg)

def main():
    # Check if file exists
    if not os.path.exists(old_file):
        with open(old_file, "w+") as f:
            pass

    # Previouse file of domains
    b = []
    with open(old_file, "r") as f:
        b = f.readlines()

    # New file of domains
    a = []
    for word in sys.stdin:
        a.append(word)

    results = list(set(a) - set(b))

    if results:
        if email and yaml_config and subject:
            sendmail(results)
        else:
            print("Missing one more required arguments: --subject|--config|--email")
            
        for result in results:
            print(result.strip())
            sys.stdout.flush()

        # Append new subdomains to previous file
        with open(old_file, "a") as f:
            f.writelines(results)
    else:
        print("Nothing here")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
