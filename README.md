# Arquivo Cívico BR — Observatório 2.0

Enciclopédia visual de políticos, partidos, proposições, votações e fontes oficiais brasileiras. Projeto editorial independente e sem orientação político-partidária.

## Início rápido

1. Abra `index.html` em um navegador moderno para experimentar o acervo inicial offline, ou hospede o repositório com GitHub Pages usando a branch `main` e a pasta `/ (root)`.
2. No site publicado, use **Atualizar da Câmara** para buscar parlamentares via API, ou execute o workflow `Atualizar dados oficiais da Câmara` para gerar um snapshot versionado para quem visita o site.
3. Se o navegador bloquear a API, abra a fonte indicada nos próprios painéis. Dados que não puderem ser comprovados **não** são substituídos por valores simulados.

## Fontes / cobertura

- **Partidos:** 30 registros datados de 26/10/2026 do [TSE](https://www.tse.jus.br/partidos/partidos-registrados-no-tse). Inclui sigla, número, data do deferimento e dirigente listado; a data do registro não equivale necessariamente à fundação histórica.
- **Senado:** 81 nomes, partido e UF na [lista oficial consultada em 25/10/2026](https://adm.senado.gov.br/adm-dadosabertos/api/v1/senadores?formato=html). É uma fotografia datada, não uma afirmação permanente.
- **Câmara:** integração com [Dados Abertos](https://dadosabertos.camara.leg.br/swagger/api.html), com cadastro, proposições, despesa e votações onde a API permitir. O workflow opcional gera `data/deputados.json` após validar o volume da resposta.
- **Executivo histórico:** seis nomes como pontos de partida, com link ao Planalto; filiação histórica, gastos e processos judiciais **não** são presumidos.
- **Federações:** cinco registros listados pelo [TSE](https://www.tse.jus.br/partidos/federacoes-registradas-no-tse).
- **Controle/judiciário:** links para TCU, CGU, STF, STJ e base de contas do TSE. Nenhuma acusação ou decisão individual foi cadastrada sem documentação específica.


## Observatório 2.0 — interface e coleta ampliada

- Painel inicial inteiramente redesenhado: hero visual inspirado no Congresso, cards dinâmicos, distribuição partidária com alternância Câmara/Senado, quadro por UF, filtros de PL/PEC, votos recentes e navegação interativa.
- Gráficos e contagens vêm **somente dos registros carregados**; nenhuma porcentagem de apoio, aprovação, desempenho ou ideologia é estimada.
- Ações do painel levam diretamente aos filtros de políticos e às páginas documentais.
- `scripts/update_legislative.py` consulta listas recentes de proposições e votações no endpoint da **API Dados Abertos da Câmara** e gera `data/legislativo.json` com URL, horário da coleta e amostra limitada. A rotina roda no GitHub Actions diariamente e em alterações do script.
- A amostra legislativa **não deve ser apresentada como total nacional ou histórico completo**. O status de um projeto (aprovado, sancionado etc.) não é inferido da ementa.
- O cache web muda para `acb-v2.0.0` para evitar que visitantes recebam o CSS antigo.

## Funcionalidades

- Página inicial com navegação visual e contagens honestas.
- Busca, filtros por partido, UF e esfera; catálogo paginado de pessoas; fichas detalhadas.
- Registro de 30 partidos, detalhes cadastrais, representação no acervo, fusões documentadas e federações.
- Consulta de proposições, trâmites, votações nominais e despesas de deputados via API da Câmara, quando disponível.
- Comparação descritiva entre até três pessoas, sem avaliações ou rankings.
- Página de metodologia, fontes e glossário de estágios processuais.
- Caderno privado de pesquisa, nunca apresentado como verificado, com exportação JSON.
- Cache de dados com IndexedDB, PWA para instalação pelo navegador, interface responsiva e dois temas.
- Workflow programado de atualização de dados oficiais para ampliar a cobertura no site publicado.

## Integridade de informações

- Alegação não equivale a inquérito, denúncia, réu, condenação ou trânsito em julgado.
- Um projeto de lei apresentado não equivale a lei aprovada.
- Uma orientação partidária não equivale ao voto nominal de todos os seus integrantes.
- Nenhuma ausência de registro deve ser entendida como absolvição ou inexistência de processo.
- Não há avaliações, notas ou comparações prescritivas de políticos.
- Informações não obtidas do sistema oficial são exibidas como não catalogadas.

## GitHub

Abra [https://github.com/new?name=Arquivo-Civico-BR](https://github.com/new?name=Arquivo-Civico-BR), crie um repositório público com branch `main` e carregue **todos** os arquivos do ZIP, preservando pastas. Depois, em **Settings → Pages**, selecione `Deploy from a branch → main → /(root)`. O site aparecerá em `https://SEU_USUARIO.github.io/Arquivo-Civico-BR/`.

Para gerar o snapshot completo de deputados, abra **Actions → Atualizar dados oficiais da Câmara → Run workflow**. As dependências são apenas Python padrão e as APIs públicas. A atualização diária não é garantia de disponibilidade da fonte ou de execução do workflow.

## Limites

Não é um inventário exaustivo de todos os políticos, processos e leis do Brasil. A base parlamentar pode estar desatualizada até uma consulta subsequente. O navegador pode impedir chamadas externas por CORS, e as entidades governamentais podem mudar seus endpoints. Para registrar processos individualizados é necessária pesquisa documental humana. O banco local IndexedDB não sincroniza automaticamente entre aparelhos.

## Licenciamento

Código do projeto disponibilizado para organização inicial no repositório pessoal. As fotografias e demais conteúdos de fontes externas conservam seus respectivos direitos e atribuições; nenhuma foto foi incorporada ao ZIP. Dados oficiais devem manter a atribuição de origem.