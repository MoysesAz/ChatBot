import os

class ManagerFilesPDF:
    directory = 'Infra/PDFs'
    @staticmethod
    def getFileNamesPdfs():
        directory = 'Infra/PDFs'
        return os.listdir(directory)

