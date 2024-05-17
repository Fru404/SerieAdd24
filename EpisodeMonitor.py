from ReadLink_firestore import ReadLink
import requests
from bs4 import BeautifulSoup
import json
from firebase_admin import db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email
def send_email(receiver_email, latest_link):
    # Email configuration
    sender_email = "dohng28@gmail.com"
    password = "cfob vngu pycx atki"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "New Episode released"

    # Email body
    body = f"Hello,\n\nlink to new episode: {latest_link}\n\nRegards,\nYour Application"

    # Attach email body
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

# Assuming ReadLink() returns a JSON string
urls_json = ReadLink()

# Parse JSON string into a Python list of dictionaries
urls = json.loads(urls_json)

# Read count from Realtime Database
ref = db.reference('name_counts')
counts_from_db = ref.get()

output_data = {}

for entry in urls:
    name = entry['name']
    url = entry['link']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all div elements with class 'episodiotitle'
    episodio_titles = soup.find_all('div', class_='episodiotitle')

    # Count the links from the webpage
    count_from_webpage = len(episodio_titles)

    # If name not in output_data, initialize the count and links list
    if name not in output_data:
        output_data[name] = {"links": [], "count": 0}

    # Extract links from each div
    for episodio_title in episodio_titles:
        link = episodio_title.find('a')['href']
        output_data[name]["links"].append(link)
        output_data[name]["count"] += 1

    # Compare counts
    if counts_from_db and name in counts_from_db:
        count_from_db = counts_from_db[name]["count"]
        if count_from_webpage > count_from_db:
            latest_link = output_data[name]["links"][0]  # Get the last link added
            send_email("ngwafru15@gmail.com", latest_link)
    
    # Update counts in Realtime Database
    ref.set(output_data)
