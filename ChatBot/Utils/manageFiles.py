import os

class ManagerFiles:
    @staticmethod
    def getFileNamesPdfs():
        directory = 'Infra/PDFs'
        return os.listdir(directory)

