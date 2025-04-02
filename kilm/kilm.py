import argparse
import os
import requests
import smtplib
import sys

from bs4 import BeautifulSoup
from email.mime.text import MIMEText

MAIL_SUBJECT = "Kilmainham Slots"
URL_TEMPLATE = url = 'https://kilmainhamgaol.admit-one.eu/?p=details&ga=1&dt={date}&ev=TOUR'


def fetch_page(url: str) -> str | None:
    """
    Fetch the HTML content of a page.

    :param url: The URL of the page to fetch.
    :return: The HTML content of the page as a string, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None


def parse_time_slots(html: str) -> list[tuple[str, str]]:
    """
    Parse the HTML to find available time slots.

    :param html: The HTML content of the page.
    :return: A list of tuples containing available time slots and their corresponding links.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    if not soup:
        return []

    available_slots = [
        (link.text.strip(), link['href'])
        for link in soup.select('div.OPW_timesHolder div a:not(.soldOut)')
    ]

    return available_slots


def get_available_slots(date: str) -> list[tuple[str, str]]:
    """
    Main function to execute the scraping.

    :param date: The date to be used in the URL.
    """
    url = URL_TEMPLATE.format(date=date)
    html_content = fetch_page(url)

    if html_content is None:
        print("Failed to retrieve HTML content.")
        return

    available_slots = parse_time_slots(html_content)

    if not available_slots:
        print("No available time slots found.")
        return

    print("Available Time Slots:")
    for time, link in available_slots:
        print(f'Time: {time}, Link: {link}')
    return available_slots


def send_email(sender_email: str, sender_password: str, recipient_email: str, subject: str, body: str):
    """Sends an email.

    :param sender_email: The email address of the sender.
    :param sender_password: The password for the sender's email account.
    :param recipient_email: The email address of the recipient.
    :param subject: The subject line of the email.
    :param body: The body text of the email.
    :raises smtplib.SMTPException: If an SMTP-related error occurs.
    :raises Exception: For other potential errors during the process.
    """
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP_SSL('smtp.mail.de', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape available time slots for Kilmainham Gaol.")
    parser.add_argument('date', type=str, help='The date in YYYYMMDD format to check for available time slots.')
    parser.add_argument('receiver', type=str, help='The receiver of the email if stuff is available.')

    args = parser.parse_args()
    
    slots = get_available_slots(args.date)
    if not slots:
        sys.exit(0)

    header = f"Found the following free slots on {args.date}:"
    slot_text = "\n".join([f'Time: {time}\nLink: {link}' for time, link in slots])
    message = f"{header}\n{slot_text}"

    email = os.environ.get("EMAIL")
    pwd = os.environ.get("PWD")

    send_email(email, pwd, args.receiver, MAIL_SUBJECT, message)

    sys.exit(0)


if __name__ == "__main__":
    main()
