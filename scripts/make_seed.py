import json, pathlib, datetime
root=pathlib.Path(__file__).resolve().parents[1]
# Sigla|nome|data do deferimento no TSE|número|dirigente listado no TSE (26/10/2026)
parties_raw='''MDB|Movimento Democrático Brasileiro|30/06/1981|15|Luiz Felipe Baleia Tenuto Rossi
PDT|Partido Democrático Trabalhista|10/11/1981|12|Carlos Roberto Lupi
PT|Partido dos Trabalhadores|11/02/1982|13|Edson Antonio Edinho da Silva
PCdoB|Partido Comunista do Brasil|23/06/1988|65|Nádia Campeão (em exercício)
PSB|Partido Socialista Brasileiro|01/07/1988|40|João Henrique de Andrade Lima Campos
PSDB|Partido da Social Democracia Brasileira|24/08/1989|45|Aécio Neves da Cunha
AGIR|Agir|22/02/1990|36|Daniel S. Tourinho
MOBILIZA|Mobilização Nacional|25/10/1990|33|Antonio Carlos Bosco Massarollo
CIDADANIA|Cidadania|19/03/1992|23|Alex Spinelli Manente
PV|Partido Verde|30/09/1993|43|José Luiz de França Penna
AVANTE|Avante|11/10/1994|70|Luis Henrique de Oliveira Resende
PP|Progressistas|16/11/1995|11|Ciro Nogueira Lima Filho
PSTU|Partido Socialista dos Trabalhadores Unificado|19/12/1995|16|José Maria de Almeida
PCB|Partido Comunista Brasileiro|09/05/1996|21|Edmilson Silva Costa
PRTB|Partido Renovador Trabalhista Brasileiro|18/02/1997|28|Leonardo Alves de Araújo
DC|Democracia Cristã|05/08/1997|27|João Caldas da Silva (em exercício)
PCO|Partido da Causa Operária|30/09/1997|29|Rui Costa Pimenta
PODE|Podemos|02/10/1997|20|Renata Hellmeister de Abreu
REPUBLICANOS|Republicanos|25/08/2005|10|Marcos Antonio Pereira
PSOL|Partido Socialismo e Liberdade|15/09/2005|50|Paula Bermudes Moraes Coradi
PL|Partido Liberal|19/12/2006|22|Valdemar Costa Neto
PSD|Partido Social Democrático|27/09/2011|55|Gilberto Kassab
SOLIDARIEDADE|Solidariedade|24/09/2013|77|Paulo Pereira da Silva
NOVO|Partido Novo|15/09/2015|30|Eduardo Rodrigo Fernandes Ribeiro
REDE|Rede Sustentabilidade|22/09/2015|18|Paulo Roberto Lamac Junior
DEMOCRATA|Democrata|29/09/2015|35|Suêd Haidar Nogueira
UP|Unidade Popular|10/12/2019|80|Leonardo Pericles Vieira Roque
UNIÃO|União Brasil|08/02/2022|44|Antônio Eduardo Gonçalves de Rueda
PRD|Partido Renovação Democrática|09/11/2023|25|Marcus Vinícius de Vasconcelos Ferreira
MISSÃO|Partido Missão|04/11/2025|14|Renan Antonio Ferreira dos Santos'''
parties=[]
for row in parties_raw.splitlines():
    short,name,date,num,president=row.split('|')
    parties.append({'sigla':short,'nome':name,'deferimento':date,'numero':int(num),'dirigente':president,'source':'https://www.tse.jus.br/partidos/partidos-registrados-no-tse','sourceDate':'2026-10-26','provenance':'TSE'})
# Senate source: official live HTML of Senators in office 25 October 2026. A person may be a substitute or hold another office; no categorical claim of current mandate beyond snapshot.
senate_raw='''ALAN RICK|REPUBLICANOS|AC
ALESSANDRO VIEIRA|MDB|SE
ANA PAULA LOBATO|PSB|MA
ANGELO CORONEL|REPUBLICANOS|BA
ASTRONAUTA MARCOS PONTES|PL|SP
BETO FARO|PT|PA
CAMILO SANTANA|PT|CE
CARLOS FÁVARO|PSD|MT
CARLOS PORTINHO|PL|RJ
CARLOS VIANA|PSD|MG
CHICO RODRIGUES|PSB|RR
CID GOMES|PSB|CE
CIRO NOGUEIRA|PP|PI
CLEITINHO|REPUBLICANOS|MG
CONFUCIO MOURA|MDB|RO
DAMARES ALVES|REPUBLICANOS|DF
DANIELLA RIBEIRO|PP|PB
DAVI ALCOLUMBRE|UNIÃO|AP
DR. HIRAN|PP|RR
DRA. EUDOCIA|PSDB|AL
EDUARDO BRAGA|MDB|AM
EDUARDO GOMES|PL|TO
EFRAIM FILHO|PL|PB
ELIZIANE GAMA|PSD|MA
ESPERIDIÃO AMIN|PP|SC
FABIANO CONTARATO|PT|ES
FERNANDO DUEIRE|PSD|PE
FLÁVIO ARNS|PSB|PR
FLÁVIO BOLSONARO|PL|RJ
GIORDANO|PODE|SP
HAMILTON MOURÃO|REPUBLICANOS|RS
HUMBERTO COSTA|PT|PE
IRAJÁ|PSD|TO
IVETE DA SILVEIRA|MDB|SC
IZALCI LUCAS|PL|DF
JADER BARBALHO|MDB|PA
JAIME BAGATTOLI|PL|RO
JAQUES WAGNER|PT|BA
JAYME CAMPOS|UNIÃO|MT
JORGE KAJURU|PSB|GO
JORGE SEIF|PL|SC
JUSSARA LIMA|PSD|PI
LAÉRCIO OLIVEIRA|PP|SE
LEANY LEMOS|PSB|DF
LUCAS BARRETO|PSD|AP
LUIS CARLOS HEINZE|PP|RS
MAGNO MALTA|PL|ES
MARA GABRILLI|PSD|SP
MARCELO CASTRO|MDB|PI
MARCIO BITTAR|PL|AC
MARCOS DO VAL|AVANTE|ES
MARCOS ROGÉRIO|PL|RO
NELSINHO TRAD FILHO|PSD|MS
OMAR AZIZ|PSD|AM
ORIOVISTO GUIMARÃES|PSDB|PR
OTTO ALENCAR|PSD|BA
PAULO PAIM|PT|RS
PLÍNIO VALÉRIO|PSDB|AM
PROFESSORA DORINHA SEABRA|UNIÃO|TO
RANDOLFE RODRIGUES|PT|AP
RENAN CALHEIROS|MDB|AL
RENAN FILHO|MDB|AL
RENZO BRAZ|PP|MG
ROBERTA ACIOLY|REPUBLICANOS|RR
ROGÉRIO CARVALHO|PT|SE
ROGERIO MARINHO|PL|RN
ROMÁRIO|S/Partido|RJ
SARGENTO REGINAURO|PSDB|CE
SERGIO MORO|PL|PR
SÉRGIO PETECÃO|PSD|AC
SORAYA THRONICKE|PSB|MS
STYVENSON VALENTIM|PODE|RN
TERESA LEITÃO|PT|PE
TEREZA CRISTINA|PP|MS
VANDERLAN CARDOSO|PSD|GO
VENEZIANO VITAL DO RÊGO|MDB|PB
WELLINGTON FAGUNDES|PL|MT
WEVERTON|PDT|MA
WILDER MORAIS|PL|GO
ZENAIDE MAIA|PSD|RN
ZEQUINHA MARINHO|PODE|PA'''
senators=[]
for i,row in enumerate(senate_raw.splitlines()):
    name,party,uf=row.split('|'); senators.append({'id':'sen'+str(i+1),'nome':name.title().replace('Do Val','do Val'),'partido':party,'uf':uf,'camara':'Senado','fonte':'Senado — relação de senadores em exercício','source':'https://adm.senado.gov.br/adm-dadosabertos/api/v1/senadores?formato=html','sourceDate':'2026-10-25','kind':'snapshot','nota':'Lista oficial consultada em 25/10/2026. Verificar titularidade e exercício atual na fonte antes de citar.'})
# Presidents: minimal identity, no unverified party affiliation, allegations or claims. Links are official biography pages, to investigate further.
historical=[
 {'id':'hist-lula','nome':'Luiz Inácio Lula da Silva','descricao':'Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'},
 {'id':'hist-bolsonaro','nome':'Jair Messias Bolsonaro','descricao':'Ex-Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'},
 {'id':'hist-dilma','nome':'Dilma Vana Rousseff','descricao':'Ex-Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'},
 {'id':'hist-temer','nome':'Michel Miguel Elias Temer Lulia','descricao':'Ex-Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'},
 {'id':'hist-fhc','nome':'Fernando Henrique Cardoso','descricao':'Ex-Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'},
 {'id':'hist-collor','nome':'Fernando Collor de Mello','descricao':'Ex-Presidência da República — trajetória e atos oficiais a consultar','camara':'Executivo / histórico','source':'https://www.gov.br/planalto/pt-br'}
]
federations=[
{'nome':'Federação União Progressista','siglas':['UNIÃO','PP'],'registro':'26/03/2026'},
{'nome':'Federação Renovação Solidária','siglas':['PRD','SOLIDARIEDADE'],'registro':'04/12/2025'},
{'nome':'Federação Brasil da Esperança','siglas':['PT','PCdoB','PV'],'registro':'24/05/2022'},
{'nome':'Federação PSDB Cidadania','siglas':['PSDB','CIDADANIA'],'registro':'26/05/2022'},
{'nome':'Federação PSOL REDE','siglas':['PSOL','REDE'],'registro':'26/05/2022'}]
changes=[{'title':'Fusão de PSL e DEM na União Brasil','date':'08/02/2022','link':'https://www.tse.jus.br/partidos/partidos-registrados-no-tse','siglas':['UNIÃO']},{'title':'Fusão de PTB e Patriota no PRD','date':'09/11/2023','link':'https://www.tse.jus.br/partidos/partidos-registrados-no-tse','siglas':['PRD']},{'title':'Federações partidárias registradas','date':'2022–2026','link':'https://www.tse.jus.br/partidos/federacoes-registradas-no-tse','siglas':[]}]
seed={'meta':{'name':'Arquivo Cívico BR — acervo base','snapshotDate':'2026-10-26','partyCount':len(parties),'senateCount':len(senators),'warnings':['Dados públicos sujeitos a atualizações.','Partido de senador é retrato de 25/10/2026, não afirmação permanente.','Nenhum dossiê judicial vinculado sem processo, órgão e documento primário.']},'parties':parties,'senators':senators,'historical':historical,'federations':federations,'changes':changes}
(root/'data'/'seed.json').write_text(json.dumps(seed,ensure_ascii=False,indent=2),encoding='utf8')
print('Created seed',len(parties),'parties',len(senators),'senators',len(historical),'historical figures')