import requests
from bs4 import BeautifulSoup
import json

def clean_name(name):
  return name.replace("\t", "").replace("\n", "")


def get_description(link): 

  # Fetch the content of the web page
  response = requests.get(link)

  # Parse the HTML content
  soup = BeautifulSoup(response.text, 'html.parser')

  desc = soup.find("div", "company-partner-description").text.strip()

  return desc


def get_exhibitors():
  # URL of the page to scrape
  url = 'https://techjobsfair.com/exhibitors/'

  # Fetch the content of the web page
  response = requests.get(url)

  # Parse the HTML content
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find the list by its class name (change 'list-class-name' to the actual class name of your list)
  list_items = soup.find_all('li', class_='company-partner-item')

  companies = []
  for item in list_items:
    name = clean_name(item.find("a", class_="company-partner-name-text").text)
    address = item.find("li", class_="company-location").text

    founded = item.find("li", class_="company-founded")
    if founded:
      founded = founded.text
    else:
      founded = None
    
    logo = item.find("div", class_="company-partner-logo")
    link = logo.find("a")["href"]
    print(link)
    desc = get_description(link)

    company_info = {
      "name": name,
      "address": address,
      "founded": founded,
      "description": desc
    }

    companies.append(company_info)

  return companies

companies = get_exhibitors()

with open('/home/beanboy/projects/techjobsfair/data/companies.json', 'w') as file: json.dump(companies, file)

