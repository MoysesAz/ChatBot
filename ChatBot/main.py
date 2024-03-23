from Application.create_financial_json import CreateFinancialJson
from Utils.create_json import CreateJson
import json

#create_financial_json = CreateFinancialJson()
#create_financial_json.generateFinancialJSON()
#financialJson = create_financial_json.get_financialJson()
#CreateJson(financialJson, "Infra/JSONs/Financial.json")
#print(financialJson)


with open('Infra/JSONs/Financial.json', 'r') as file:
    financialJson = json.load(file)

print(financialJson)
