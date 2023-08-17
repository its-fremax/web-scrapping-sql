import smtplib, ssl
import time
import requests
import sqlite3
import selectorlib

connection = sqlite3.connect("data.db")

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """scrape the page"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "arinzemaxwell22@gmail.com"
    password = "kezriqutitaflzmk"
    receiver = "arinzemaxwell22@gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent")


def store(tour):
    row = tour.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(tour):
    row = tour.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    row = cursor.fetchall()
    print(row)
    return row


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        tours = extract(scrapped)
        print(tours)
        if tours != "No upcoming tours":
            rows = read(tours)
            if not rows:
                store(tour=tours)
                send_email(message=f"Hey there is a new event. {tours} is starting soon")
        time.sleep(3)

