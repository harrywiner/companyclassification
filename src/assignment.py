import json
from dotenv import load_dotenv
from openai import OpenAI
import os


# Open the JSON file
with open('companies.json') as file:
  # Load the JSON data
  companies = json.load(file)

load_dotenv()

client = OpenAI()


def classify_company(description):
  # Call the OpenAI API
  # tools = [
  #   {
  #     "type": "function",
  #     "function": {
  #       "name": "classify_company",
  #       "description": "Determine the classification of a company based on its description",
  #       "parameters": {
  #         "type": "object",
  #         "properties": {
  #           "description": {
  #             "type": "string",
  #             "description": "The company's description",
  #           },
  #         },
  #         "required": ["description"],
  #       },
  #     }
  #   }
  # ]
  messages = [{"role": "user", "content": f"Answer in one or two words. Determine the classification of this company's industry: {description}"}]
  completion = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
  )

  print(completion)
  return completion.choices[0].message.content

classify_company(companies[1]["description"])


def write_classifications(companies):
  new_companies = []
  

  try:
    for company in companies:
      new_company = company.copy()
      description = new_company["description"]
      classification = classify_company(description)
      new_company["classification"] = classification

      new_companies.append(new_company)
  except KeyboardInterrupt:
    with open('companies_classifications.json', 'w') as file:
      json.dump(new_companies, file)
  with open('companies_classifications.json', 'w') as file:
    json.dump(new_companies, file)

write_classifications(companies)