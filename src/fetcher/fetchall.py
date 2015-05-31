import sys
import json
import urlparse
import requests

BASE_URL = 'http://compras.dados.gov.br'
LICITACOES_URL = 'licitacoes/v1/licitacoes.json'
CONTRATOS_URL = 'contratos/v1/contratos.json'
MATERIAIS_URL = 'materiais/v1/materiais.json'
CLASSES_URL = 'materiais/v1/classes.json'

def get_url(url):
    return '%s/%s' % (BASE_URL, url)

def download_all(url, dataname):
    has_next = True
    params = {}
    c = 0;

    error_url = []

    while has_next:
        print 'GET:', url
        r = requests.get(get_url(url), params=params)

        if r.status_code != 200:
            error_url.append(url)
            parse = urlparse.urlparse(get_url(url))
            query = dict(urlparse.parse_qsl(parse.query))
            offset = int(query['offset'])
            offset += 500
            url = url.replace(query['offset'], str(offset))
            continue
        data = r.json()

        f = open('%s_%09d.json' % (dataname, c), 'w')
        f.write(json.dumps(data))
        f.close()
        c += 1

        links = data['_links']
        has_next = links.get('next', False)
        if has_next:
#            print has_next['href']
#            parseresult = urlparse.urlparse(has_next['href'])
#            offset = parseresult.params['offset']
#            params['offset'] = offset
            url = has_next['href']
    print error_url

def fetch_all(out_file, url, dataname, params):
    has_next = True
    data_list = []
    while has_next:
        print 'GET:', url, params
        r = requests.get(get_url(url), params=params)
        data = json.loads(r.text)
        links = data['_links']
        has_next = links.get('next', False)
        if has_next:
#            print has_next['href']
#            parseresult = urlparse.urlparse(has_next['href'])
#            offset = parseresult.params['offset']
#            params['offset'] = offset
            url = has_next['href']
        embedded = data['_embedded']
        data_list.extend(embedded[dataname])

    if out_file:
        f = open(out_file, 'w')
        f.write(json.dumps({dataname: data_list}))
        f.close()

    return data_list

def fetch_licitacao(out_file, item_material=None):
    return fetch_all(out_file, LICITACOES_URL, 'licitacoes', {'item_material' : item_material})

def fetch_contrato(out_file, params={}):
    return fetch_all(out_file, CONTRATOS_URL, 'contratos', params)

if __name__ == '__main__':
#    fetch_contrato('contratos.json')
    lics = fetch_licitacao('licitacoes_000001805.json', '000001805')
#    lics = json.load(open('licitacoes_000103047.json'))['licitacoes']
    c = 0
    valores = []
    for l in lics:
        if int(l['numero_itens']) == 1:
            contratos = fetch_all(None, l['_links']['contratos']['href'].replace('contratos?', 'contratos.json?'), 'contratos', {})
            itens = fetch_all(None, l['_links']['itens']['href'] + '.json', 'itensLicitacao', {})
            if len(contratos) == 1:
                total = float(contratos[0]['valor_inicial'])
                quantidade = int(itens[0]['quantidade'])
                print '%f / %d' % (total, quantidade)
                valores.append(total / quantidade)
                print valores[-1]
                print
                c+=1
    print '\n\n\n\n'
    for v in valores: print v
    print sum(valores) / len(valores)
    print len(valores)
