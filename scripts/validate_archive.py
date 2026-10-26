#!/usr/bin/env python3
"""Static integrity checks for Arquivo Cívico BR; no political conclusions."""
from pathlib import Path
import json, re, sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'index.html','assets/app.js','assets/style.css','assets/logo.svg',
    'data/seed.json','data/seed.js','docs/EDITORIAL.md','docs/schema.sql',
    'scripts/update_official.py','manifest.webmanifest','sw.js'
]

def require(ok, why):
    if not ok: raise AssertionError(why)

def official_link(value):
    parsed = urlparse(value or '')
    return parsed.scheme == 'https' and bool(parsed.netloc)

def main():
    for path in REQUIRED:
        require((ROOT/path).is_file(), f'Arquivo necessário ausente: {path}')
    seed = json.loads((ROOT/'data/seed.json').read_text(encoding='utf-8'))
    require(len(seed['parties']) >= 25, 'Base de partidos inesperadamente reduzida')
    require(len(seed['senators']) >= 70, 'Snapshot de senadores inesperadamente reduzido')
    require(len(seed['federations']) >= 4, 'Snapshot de federações inesperadamente reduzido')
    require(len({p['sigla'] for p in seed['parties']}) == len(seed['parties']), 'Siglas partidárias duplicadas')
    require(len({s['nome'] for s in seed['senators']}) == len(seed['senators']), 'Nomes duplicados no snapshot do Senado')
    for category in ('parties','senators','historical'):
        for row in seed[category]:
            require(official_link(row.get('source')), f'Registro sem URL HTTPS de origem em {category}: {row.get("nome") or row.get("sigla")}')
    js = (ROOT/'data/seed.js').read_text(encoding='utf-8')
    require(js.startswith('window.ARCHIVE_SEED = '), 'Formato de seed.js inválido')
    require(json.loads(js[len('window.ARCHIVE_SEED = '):].rstrip().removesuffix(';')) == seed, 'seed.js e seed.json divergentes')
    html = (ROOT/'index.html').read_text(encoding='utf-8')
    require('data/seed.js' in html and 'assets/app.js' in html, 'HTML não inicializa scripts de dados e interface')
    for path in ('data/seed.js','assets/app.js','assets/style.css','assets/logo.svg'):
        require(path in html, f'HTML não inclui {path}')
    deputy_path = ROOT/'data/deputados.json'
    if deputy_path.exists():
        deputies = json.loads(deputy_path.read_text(encoding='utf-8'))
        items = deputies.get('items',[])
        require(len(items) >= 450, 'Snapshot da Câmara tem volume insuficiente')
        require(len({x['id'] for x in items}) == len(items), 'IDs duplicados no snapshot da Câmara')
        require(official_link(deputies.get('source')), 'Snapshot da Câmara sem fonte HTTPS')
        require(deputies.get('count') == len(items), 'Contagem da Câmara inconsistente')
        print(f'Câmara: {len(items)} registros verificados estruturalmente, data {deputies.get("capturedAt")}')
    else:
        print('Câmara: snapshot ainda não criado; carregamento sob demanda previsto')
    print(f'OK — {len(seed["parties"])} partidos; {len(seed["senators"])} senadores; {len(seed["federations"])} federações; referências HTTPS presentes.')
    print('Importante: integridade estrutural não equivale a validação jurídica de fatos individuais.')

if __name__ == '__main__':
    try: main()
    except (AssertionError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f'FALHA: {exc}', file=sys.stderr)
        sys.exit(1)