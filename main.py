import requests
import selectorlib


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


def send_email():
    print("Email was sent")


def store(tour):
    with open("data.txt", "a") as file:
        file.write(tour + "\n")


def read(tour):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scrapped = scrape(URL)
    tours = extract(scrapped)
    content = read(tours)
    print(tours)
    if tours != "No upcoming tours":
        if tours not in content:
            store(tour=tours)
            send_email()
