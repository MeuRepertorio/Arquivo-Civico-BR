#!/usr/bin/env python3
"""Publicar amostra datada de proposições e votações da API oficial da Câmara.

Não preencher lacunas, não criar rankings, não inferir resultado de votação.
Um erro de rede mantém o último snapshot publicado inalterado.
"""
import datetime
import json
import pathlib
import time
import urllib.parse
import urllib.request

ROOT=pathlib.Path(__file__).resolve().parents[1]
API='https://dadosabertos.camara.leg.br/api/v2'


def fetch(endpoint, params):
    url=f'{API}/{endpoint}?'+urllib.parse.urlencode(params)
    error=None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'ArquivoCivicoBR/2.0 contato:github.com/MeuRepertorio/Arquivo-Civico-BR','Accept':'application/json'})
            with urllib.request.urlopen(req,timeout=55) as res:
                payload=json.load(res)
            records=payload.get('dados',[])
            if not isinstance(records,list):raise ValueError('Resposta sem array dados')
            return records,url
        except Exception as exc:
            error=exc
            if attempt<2: time.sleep(2**attempt)
    raise RuntimeError(f'Falha ao consultar {endpoint}: {error}')


def snapshot():
    props,purl=fetch('proposicoes',{'itens':100,'ordem':'DESC','ordenarPor':'id'})
    votes,vurl=fetch('votacoes',{'itens':50,'ordem':'DESC','ordenarPor':'dataHoraRegistro'})
    outprops=[]
    for p in props:
        id=p.get('id')
        if not isinstance(id,int) or not p.get('ementa'):continue
        outprops.append({'id':id,'tipo':p.get('siglaTipo') or '', 'numero':p.get('numero'), 'ano':p.get('ano'), 'ementa':p['ementa'], 'dataApresentacao':p.get('dataApresentacao') or '', 'url':f'https://www.camara.leg.br/propostas-legislativas/{id}'})
    outvotes=[]
    for v in votes:
        id=v.get('id')
        if not id or not v.get('data'):continue
        outvotes.append({'id':str(id),'data':v['data'],'descricao':v.get('descricao') or '', 'ultimaApresentacao':v.get('ultimaApresentacao') or '', 'url':f'{API}/votacoes/{urllib.parse.quote(str(id),safe="")}'})
    if len(outprops)<30 or len(outvotes)<10:
        raise ValueError(f'Resposta insuficiente: {len(outprops)} proposições, {len(outvotes)} votações')
    body={'institution':'Câmara dos Deputados','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Amostra recente retornada pela API; NÃO é o total de proposições ou votações brasileiras.', 'sources':{'proposicoes':purl,'votacoes':vurl}, 'counts':{'proposicoesNaAmostra':len(outprops),'votacoesNaAmostra':len(outvotes)}, 'proposicoes':outprops,'votacoes':outvotes}
    path=ROOT/'data'/'legislativo.json'
    path.write_text(json.dumps(body,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('Saved official sample',len(outprops),'propositions,',len(outvotes),'votes to',path)


if __name__=='__main__':snapshot()