
import os
import json
import csv
import requests

def contratos(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
    onlyfiles.sort()
    for f in onlyfiles:
        print f
        with open(os.path.join(path, f)) as data_file:
            data = json.load(data_file)
            yield data['_embedded']['contratos']

def get_fornecedor_name(cnpj):
    r = requests.get('http://compras.dados.gov.br/fornecedores/doc/fornecedor_pj/' + cnpj + '.json')
    return r.json()

fornecedores = {}
def get_fornecedor(cnpj):
    return ''
    if not cnpj:
        return ''
    if cnpj in fornecedores:
        return fornecedores[cnpj]
    fornecedores[cnpj] = get_fornecedor_name(cnpj)
    return fornecedores[cnpj].get('razao_social', '')


if __name__ == '__main__':
    output = sys.argv[1]
    cache_dir = sys.argv[2]
    with open(output, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['identificador', 'uasg', 'uasg_title',
                         'cnpj_contratada', 'cnpj_title', 'data_assinatura',
                         'valor_inicial', 'numero_itens', 'objeto'])
        for c_list in contratos(cache_dir):
            for c in c_list:
                if c.get('modalidade_licitacao', None) and int(c.get('modalidade_licitacao', 0)) == 5:
                    fornecedor = get_fornecedor(c.get('cnpj_contratada', None))
                    writer.writerow([c['identificador'], c['uasg'], c['_links']['uasg']['title'].encode('latin1'),
                                     c.get('cnpj_contratada', ''), fornecedor, c['data_assinatura'],
                                     c['valor_inicial'], c.get('numero_itens', ''), '"' + c['objeto'].encode('latin1') + '"'])
