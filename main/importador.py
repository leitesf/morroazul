import csv
from main.models import Cliente

def importar_clientes():
    dados = csv.DictReader(open('clientes.csv', 'r'), delimiter=';')
    erros = 0
    importados = 0
    for row in dados:
        try:
            cliente = Cliente()
            if len(row['documento'])==11:
                cliente.cpf=row['documento']
            else:
                cliente.cnpj=row['documento']
            cliente.nome = row['nome']
            if row['nome_fantasia']:
                cliente.nome_fantasia = row['nome_fantasia']
            telefone = ""
            if row["telefone1"]:
                telefone = row["telefone1"]
            if row["telefone2"] and not telefone:
                telefone = row["telefone2"]
            elif row["telefone2"] and telefone:
                telefone = f"{telefone} / {row['telefone2']}"
            cliente.telefone = telefone
            cliente.endereco = row["endereco"]
            cliente.cep = row["cep"]
            cliente.cidade = row["cidade"]
            cliente.estado = row["uf"]
            cliente.save()
            importados += 1
        except:
            print(row['nome']+'\n')
            erros+=1

    print(u"Dados Importados: %i \n" % importados)
    print(u"Erros: %i" % erros)