from Application.create_financial_json import CreateFinancialJson
from Utils.create_json import CreateJson

createFinancialJson = CreateFinancialJson()
createFinancialJson.generateFinancialJSON()
financialJson = createFinancialJson.get_financialJson()
CreateJson(financialJson, "Infra/BD/Financial.json")

