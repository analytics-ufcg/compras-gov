import json
import urlparse
import requests

BASE_URL = 'http://compras.dados.gov.br'
LICITACOES_URL = 'licitacoes/v1/licitacoes.json'

def get_url(url):
    return '%s/%s' % (BASE_URL, url)

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

    f = open(out_file, 'w')
    f.write(json.dumps({dataname: data_list}))
    f.close()

    return data_list

def fetch_licitacao(out_file, item_material=None):
    return fetch_all(out_file, LICITACOES_URL, 'licitacoes', {'item_material' : item_material})

if __name__ == '__main__':
    lic = fetch_licitacao('licitacoes_000103047.json', '000103047')
