#!/usr/bin/env python3
"""GitHub Actions ETL: retrieve data from primary Brazilian legislative source.
Never fabricate missing fields. On network failure, preserve previously published snapshot.
"""
import datetime, json, pathlib, sys, time, urllib.request
BASE='https://dadosabertos.camara.leg.br/api/v2'
ROOT=pathlib.Path(__file__).resolve().parents[1]
def request(url):
  req=urllib.request.Request(url,headers={'User-Agent':'ArquivoCivicoBR/1.0 research tool','Accept':'application/json'})
  with urllib.request.urlopen(req,timeout=40) as response:return json.load(response)
def run():
  items=[]
  for page in range(1,13):
    url=f'{BASE}/deputados?itens=100&pagina={page}&ordem=ASC&ordenarPor=nome'
    data=None
    for attempt in range(3):
      try:data=request(url);break
      except Exception as ex:
        if attempt==2:raise RuntimeError(f'Failed page {page}: {ex}') from ex
        time.sleep(2**attempt)
    part=data.get('dados',[])
    if not isinstance(part,list):raise ValueError('Unexpected deputy API payload')
    items.extend(part)
    if len(part)<100 or not any(x.get('rel')=='next' for x in data.get('links',[])):break
    time.sleep(.3)
  people=[]
  for person in items:
    if not isinstance(person.get('id'),int) or not person.get('nome'):continue
    people.append({'id':'dep'+str(person['id']),'apiId':person['id'],'nome':person['nome'],'partido':person.get('siglaPartido') or '', 'uf':person.get('siglaUf') or '', 'camara':'Câmara','foto':person.get('urlFoto') or '', 'source':f'https://www.camara.leg.br/deputados/{person["id"]}','sourceDate':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),'kind':'api-snapshot'})
  if len(people)<450:raise RuntimeError(f'API returned only {len(people)} deputy records: refuse to overwrite a healthy snapshot')
  p=ROOT/'data'/'deputados.json'
  output={'source':BASE+'/deputados','institution':'Câmara dos Deputados','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':len(people),'items':people,'note':'Registro de deputados na API no instante da coleta; mandatos, nomes e partidos podem mudar.'}
  p.write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
  print('Saved',len(people),'official deputy records to',p)
if __name__=='__main__':
  try:run()
  except Exception as e:
    print('Could not refresh source; prior snapshot left untouched:',e,file=sys.stderr)
    sys.exit(1)