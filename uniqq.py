#!/usr/bin/env python3
import os
import sys
import yaml
import smtplib
import argparse
from email.message import EmailMessage

# Parse arguments
parser = argparse.ArgumentParser(description="Get difference between 2 files. One from stdin and one from `file`.")
parser.add_argument("file", help="File to campare against your new file from `stdin`")
parser.add_argument("-s", "--subject", help="Subject of the email", required=True)
parser.add_argument("-c", "--config", help="Yaml file containing your email, password, and email to alert", required=True)

args        = parser.parse_args()
subject     = args.subject
old_file    = args.file
yaml_config = args.config

def sendmail(results):
    with open(yaml_config, 'r') as f:
        yaml_data = yaml.safe_load(f)

    username  = yaml_data["username"][0]
    password  = yaml_data["password"][0]
    recipient = yaml_data["recipient"][0]

    msg = f"Subject: {subject}\n\n"

    for result in results:
        msg = msg + result

    # Send the message
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(username, password)
        s.sendmail(username, recipient, msg)

def main():
    # Previouse file of domains
    b = []
    with open(old_file, "r") as f:
        b = f.readlines()

    # New file of domains
    a = []
    for word in sys.stdin:
        a.append(word)

    results = list(set(a) - set(b))

    if len(results) > 0:
        # Output the results to the terminal
        [print(f"{result.strip()}") for result in results]

        sendmail(results)

        # Append new subdomains to previous file
        with open(old_file, "a+") as f:
            f.writelines(results)

if __name__ == "__main__":
    main()
