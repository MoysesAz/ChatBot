import json
import csv

path = "Infra/BD/Financial.json"

with open(path, 'r') as file:
    financialJson = json.load(file)


print(financialJson)