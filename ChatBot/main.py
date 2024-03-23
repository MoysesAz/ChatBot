from Application.create_financial_json import CreateFinancialJson
from Utils.create_json import CreateJson

create_financial_json = CreateFinancialJson()
create_financial_json.generateFinancialJSON()
financialJson = create_financial_json.get_financialJson()
CreateJson(financialJson, "Infra/Jsons/Financial.json")



print(financialJson)
