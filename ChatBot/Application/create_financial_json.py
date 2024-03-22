from Utils.manage_files import ManagerFilesPDF
from Application.process_financial_pdf import ProcessFinancialPdf

class CreateFinancialJson:
    def __init__(self):
        self.path = "Infra/PDFs/"
        self.file_names = ManagerFilesPDF.getFileNamesPdfs()
        self.financialJson = {}

    def generateFinancialJSON(self):
        for file_name in self.file_names:
            managerPDF = ProcessFinancialPdf(self.path + file_name)
            managerPDF.processPDF()
            dictPDF = managerPDF.getPdfInDict()
            self.financialJson[file_name] = dictPDF

    def get_financialJson(self):
        return self.financialJson


