import pdfplumber
from datetime import datetime
class ProcessFinancialPdf:
    def __init__(self, path):
        self.__path = path
        self.__cache = {
            "Dados da Companhia": {"csv": {}},
            "Dados Econômico-Financeiros - R$ - mil": {
                "Balanço Patrimonial - Consolidado": {"csv": {}},
                "Demonstração do Resultado - Consolidado": {"csv": {}},
                "Demonstração do Fluxo de Caixa - Consolidado": {"csv": {}},
            },
            "Posição Acionária*": {},
            "Ações em Circulação no Mercado": {"date": "", "csv": {}},
            "Composição do Capital Social": { "date": "", "csv": {}
            }
        }
        self.title = ""
        self.state = 0
        self.line = ["", "", "", "", "", "", ""]
        self.refactorLine = ["", "", "", "", "", "", ""]
        self.__composeStates = {
            0: [[], self.switchToStateBalanceSheet, self.fillTableCompanyData],
            1: [[0, 2], self.switchToStateResultDemonstration, self.fillTableBalanceSheet],
            2: [[0, 2], self.switchToStateCashFlowStatement, self.fillTableResultDemonstration],
            3: [[0, 2], self.switchToStateShareholdingPosition, self.fillTableCashFlowStatement],
            4: [[0, 3], self.switchToStateFinishShareholdingPosition, self.fillTableShareHoldingPosition],
            5: [[], self.switchToStateDataOutstandingShares, lambda: None],
            6: [[0, 2], self.switchToStateShareCapital, self.fillTableOutstandingShares],
            7: [[0, 2],lambda: False, self.fillTableShareCapital],
        }
    def processPDF(self):
        with pdfplumber.open(self.__path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for line in table:
                        self.line = line
                        self.handler_state()
    def handler_state(self):
        if self.state in self.__composeStates:
            settings_treating_line, switch_function, fill_function = self.__composeStates[self.state]
            if switch_function():
                return
            if settings_treating_line != []:
                self.treating_line(settings_treating_line)
            fill_function()

    def treating_line(self, settings_treating_line):
        if settings_treating_line[1] == 0:
            self.refactorLine = self.line[settings_treating_line[0]].rsplit(" ")
        else:
            self.refactorLine = self.line[settings_treating_line[0]].rsplit(" ", settings_treating_line[1])
    def fillTableCompanyData(self):
        self.__cache["Dados da Companhia"]["csv"][self.line[0]] = self.line[1]
    def fillDateInEconomicData(self):
        self.title = self.line[0]
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]
        pathBD["Inicio"] = self.line[2]
        pathBD["Fim"] = self.line[1]
    def switchToStateBalanceSheet(self):
        if "Balanço Patrimonial - Consolidado" in self.line[0]:
            self.fillDateInEconomicData()
            self.state += 1
            return True

        return False
    def fillDateInResultDemonstration(self):
        self.title = self.line[0]
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]
        pathBD["Inicio"] = self.line[2]
        pathBD["Fim"] = self.line[1]
    def switchToStateResultDemonstration(self):
        if "Demonstração do Resultado" in self.line[0]:
            self.fillDateInResultDemonstration()
            self.state += 1
            return True
        return False
    def fillTableBalanceSheet(self):
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]["csv"]
        pathBD[self.refactorLine[0] + " - Inicial"] = self.refactorLine[2]
        pathBD[self.refactorLine[0] + " - Final"] = self.refactorLine[1]
    def fillDateInCashFlowStatement(self):
        self.title = self.line[0]
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]
        pathBD["Inicio"] = self.line[2]
        pathBD["Fim"] = self.line[1]
    def switchToStateCashFlowStatement(self):
        if "Demonstração do Fluxo de Caixa - Consolidado" in self.line[0]:
            self.state += 1
            self.fillDateInCashFlowStatement()
            return True

        return False
    def fillTableResultDemonstration(self):
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]["csv"]
        pathBD[self.refactorLine[0] + " - Inicial"] = self.refactorLine[2]
        pathBD[self.refactorLine[0] + " - Final"] = self.refactorLine[1]
    def switchToStateShareholdingPosition(self):
        if self.line[0] == "Nome":
            self.state += 1
            return True
        return False
    def fillTableCashFlowStatement(self):
        pathBD = self.__cache["Dados Econômico-Financeiros - R$ - mil"][self.title]["csv"]
        pathBD[self.refactorLine[0] + " - Inicial"] = self.refactorLine[2]
        pathBD[self.refactorLine[0] + " - Final"] = self.refactorLine[1]
    def switchToStateFinishShareholdingPosition(self):
        if self.line[0] == "Nome":
            return True
        if "Total" in self.line[0]:
            self.state += 1
            return True
        return False
    def switchToStateShareCapital(self):
        if "Tipos de Investidores / Ações" in self.line[0]:
            return True
        try:
            self.refactorLine = self.line[0][-10:]
            datetime.strptime(self.refactorLine, '%d/%m/%Y').date()
            self.__cache["Composição do Capital Social"]["date"] = self.refactorLine
            self.state += 1
            return True
        except ValueError:
            return False
    def switchToStateDataOutstandingShares(self):
        try:
            self.refactorLine = self.line[0][-10:]
            datetime.strptime(self.refactorLine, '%d/%m/%Y').date()
            self.__cache["Ações em Circulação no Mercado"]["date"] = self.refactorLine
            self.state += 1
            return True
        except ValueError:
            print("erro")
            return False
    def fillTableShareHoldingPosition(self):
        pathBD = self.__cache["Posição Acionária*"]
        pathBD[self.refactorLine[0] + " %ON"] = self.refactorLine[1]
        pathBD[self.refactorLine[0] + " %PN"] = self.refactorLine[2]
        pathBD[self.refactorLine[0] + " %TOTAL"] = self.refactorLine[3]
    def fillTableOutstandingShares(self):
        pathBD = self.__cache["Ações em Circulação no Mercado"]['csv']
        pathBD[self.refactorLine[0] + ' - Quantidade'] = self.refactorLine[1]
        pathBD[self.refactorLine[0] + ' - Percentual'] = self.refactorLine[2]
    def fillTableShareCapital(self):
        pathBD = self.__cache["Composição do Capital Social"]["csv"]
        pathBD[self.refactorLine[0]] = self.refactorLine[1]

    def getPdfInDict(self):
        return self.__cache
