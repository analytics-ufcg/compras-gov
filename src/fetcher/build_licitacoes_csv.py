import sys
import json
import requests

BASE_URL = 'http://compras.dados.gov.br'
LICITACOES_URL = 'licitacoes/v1/licitacoes.json'

def get_url(url):
    return '%s/%s' % (BASE_URL, url)

def fetch_all(url, dataname, params):
    has_next = True
    data_list = []
    while has_next:
        print 'GET:', url, params

        try:
            r = requests.get(get_url(url), params=params)
        except requests.exceptions.ConnectionError:
            print 'Connection error. Retrying...'
            time.sleep(2)
            r = requests.get(get_url(url), params=params)

        data = json.loads(r.text)
        links = data['_links']
        has_next = links.get('next', False)
        if has_next:
            url = has_next['href']
        embedded = data['_embedded']
        data_list.extend(embedded[dataname])

    return data_list

def fetch_licitacao(item_material=None):
    return fetch_all(LICITACOES_URL, 'licitacoes', {'item_material' : item_material})

if __name__ == '__main__':
    num_material = sys.argv[1]
    assert len(num_material) == 9, 'Your parameter needs to be a number of 9 digits.'

    outfile_name = 'licitacoes_' + num_material + '.csv'
    lics = fetch_licitacao(num_material)

    file_csv = open(outfile_name, 'w')
    file_csv.write('url;total;quantidade;valor\n')
    for l in lics:
        if int(l['numero_itens']) == 1:
            contratos = fetch_all(l['_links']['contratos']['href'].replace('contratos?', 'contratos.json?'), 'contratos', {})
            itens = fetch_all(l['_links']['itens']['href'] + '.json', 'itensLicitacao', {})
            if len(contratos) == 1:
                total = float(contratos[0]['valor_inicial'])
                quantidade = int(itens[0]['quantidade'])
                lic_url = l['_links']['self']['href']
                valor = total / quantidade
                
                print lic_url
                file_csv.write(lic_url + ';' + str(total) + ';' + str(quantidade) + ';' + str(valor) + '\n')

    file_csv.close()
