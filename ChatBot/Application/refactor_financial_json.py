import json

class RefactorFinancialJson:
    def __init__(self, json_path):
        self.__path = json_path
        self.__csv_companies = []
        self.__refactorFinancialJson = {}

    def refactor(self):
        with open(self.__path, 'r') as financial_json:
            financial_data = json.load(financial_json)

        consolidated_data = {}
        company_name = ""
        shareholder_position = {}
        company_data = {}

        for company_key in financial_data:
            bd = financial_data[company_key]
            for key_bd in bd:
                if "Dados da Companhia" == key_bd:
                    company_data = bd[key_bd]['csv']
                    company_name = f"{company_key[:-4]} {company_data['Nome de Pregão:']}"
                elif "Dados Econômico-Financeiros" in key_bd:
                    economic_data = bd[key_bd]
                    for key_def in economic_data:
                        company_data.update(economic_data[key_def]['csv'])
                elif "Posição Acionária*" == key_bd:
                    shareholder_position = bd[key_bd]
                else:
                    company_data.update(bd[key_bd]['csv'])

            consolidated_data = {}
            consolidated_data[company_name] = {"info": company_data, 'Posição Acionária*': shareholder_position}

        self.__refactorFinancialJson = consolidated_data

    def getRefactorFinancialJson(self):
        return self.__refactorFinancialJson



