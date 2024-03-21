import pdfplumber
from Utils.manageFiles import ManagerFiles
from datetime import datetime

path = "Infra/PDFs/"
fileNames = ManagerFiles.getFileNamesPdfs()
bd = {
    "Dados da Companhia": {
        "info": {}
    },
    "Dados Econômico-Financeiros - R$ - mil": {
        "Balanço Patrimonial - Consolidado": {
            "info": {}
        },
        "Demonstração do Resultado - Consolidado": {
            "info": {}
        },
        "Demonstração do Fluxo de Caixa - Consolidado": {
            "info": {}
        },
    },
    "Posição Acionária*": {

    },

    "Ações em Circulação no Mercado": {
        "date": "",
        "info": {}
    },
}

newBd = {
    "7": [],
    "8": [],
    "9": []
}


def getInfoPDF(pdfName):
    state = 0
    title = ""
    with pdfplumber.open(path + pdfName) as pdf:
        for indexPage, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for indexTable, table in enumerate(tables):
                for indexLine, line in enumerate(table):
                    if state == 0:
                        if "Balanço Patrimonial - Consolidado" in line[0]:
                            state += 1
                            title = line[0]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Inicio"] = line[2]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Fim"] = line[1]
                            continue
                        bd["Dados da Companhia"]["info"][line[0]] = line[1]
                    if state == 1:
                        refactorLine = line[0].rsplit(" ", 2)
                        if "Demonstração do Resultado" in line[0]:
                            state += 1
                            title = line[0]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Inicio"] = line[2]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Fim"] = line[1]
                            continue
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Inicial"] = refactorLine[2]
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Final"] = refactorLine[1]
                    if state == 2:
                        refactorLine = line[0].rsplit(" ", 2)
                        if "Demonstração do Fluxo de Caixa - Consolidado" in line[0]:
                            state += 1
                            title = line[0]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Inicio"] = line[2]
                            bd["Dados Econômico-Financeiros - R$ - mil"][title]["Fim"] = line[1]
                            continue
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Inicial"] = refactorLine[2]
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Final"] = refactorLine[1]
                    if state == 3:
                        refactorLine = line[0].rsplit(" ", 2)
                        if line[0] == "Nome":
                            state += 1
                            continue
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Inicial"] = \
                        refactorLine[2]
                        bd["Dados Econômico-Financeiros - R$ - mil"][title]["info"][refactorLine[0] + " - Final"] = \
                        refactorLine[1]
                    if state == 4:
                        refactorLine = line[0].rsplit(" ", 3)
                        if line[0] == "Nome":
                            continue
                        if "Total" in line[0]:
                            state += 1
                            continue
                        bd["Posição Acionária*"][refactorLine[0] + " %ON"] = refactorLine[1]
                        bd["Posição Acionária*"][refactorLine[0] + " %PN"] = refactorLine[2]
                        bd["Posição Acionária*"][refactorLine[0] + " %TOTAL"] = refactorLine[3]
                    if state == 5:
                        try:
                            datetime.strptime(line[0], '%d/%m/%Y').date()
                            state += 1
                            continue
                        except ValueError:
                            print("erro")
                    if state == 6:
                        if "Tipos de Investidores / Ações" in line[0]:
                            state += 1
                            continue
                    if state == 7:
                        try:
                            refactorLine = line[0][-10:]
                            datetime.strptime(refactorLine, '%d/%m/%Y').date()
                            state += 1
                            continue
                        except ValueError:
                            refactorLine = line[0].rsplit(" ", 2)
                            bd["Ações em Circulação no Mercado"]['info'][refactorLine[0] + ' - Quantidade'] = refactorLine[1]
                            bd["Ações em Circulação no Mercado"]['info'][refactorLine[0] + ' - Percentual'] = refactorLine[2]

def mostrarInformacoes(bd):
    for secao, subsecoes in bd.items():
        print(f"== {secao} ==")
        if isinstance(subsecoes, dict):
            for subsecao, detalhes in subsecoes.items():
                print(f"== {subsecao} ==")
                if isinstance(detalhes, dict):
                    for chave, valor in detalhes.items():
                        if chave == "info":
                            print("Detalhes:")
                            for info_chave, info_valor in valor.items():
                                print(f"- {info_chave}: {info_valor}")
                        else:
                            print(f"{chave}: {valor}")
                else:
                    print(f"{subsecao}: {detalhes}")
        else:
            print(f"{secao}: {subsecoes}")
        print("=" * 30)

for i in fileNames:
    getInfoPDF(i)

