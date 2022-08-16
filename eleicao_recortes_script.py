

# https://dadosabertos.tse.jus.br/dataset/candidatos-2022

# 2018: https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip

# 2022: https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2022.zip

# Consulte os metadados: https://drive.google.com/file/d/1mM1U-2hN-9usXOE4Dyvewk_wWjN-ZMuW/

# O TSE impede o colab de carregar os dados diretamente. Baixei e salvei os datasets no Google Drive e no Github

# Pandas é a biblioteca de código que usamos para processar os dados

import pandas as pd

# Matplotlib e Seaborn são as bibliotecas para geraçao de gráficos
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

# ID dos datasets salvos no Google Sheets
id_planilha_2018 = '1TilkWAd_vya4MlS0V4kCib8p23FKKqvjoToy0mywAko'
id_planilha_2022 = '1v0EcG29yzU2JhY_5cAin1KQrpwL3K5-Ar9-2IPJoujc'

# ID das abas com as eleições de 2018 e 2022
eleicoes_2018 = '124256647'
eleicoes_2022 = '1264465923'

# Carrega os datasets no Pandas usando uma URL do Google Drive e no Github para baixar CSVs

candidatos_2018 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{id_planilha_2018}/gviz/tq?tqx=out:csv&gid={eleicoes_2018}')

candidatos_2022 = pd.read_csv('https://raw.githubusercontent.com/rafagarc/eleicoes_2022/main/consulta_cand_2022_BRASIL.csv', sep=';', encoding='ISO-8859-1')

# Separa o dataset de primeiro turno da eleição de 2018

candidatos_2018 = candidatos_2018[candidatos_2018['NR_TURNO'] == 1]

# Junta os datasets das duas eleições em um só

candidatos = pd.concat([candidatos_2018, candidatos_2022]).reset_index(drop=True)

# Renomeia os datasets
df = candidatos

# Deleta dataframes usados só para manipulação
del candidatos
del candidatos_2018
del candidatos_2022



"""## Total de candidatos
Número de candidatos para todos os cargos nas eleições de 2018 e 2022
"""

# Soma o número total de candidatos dos dois anos

total_candidatos = [df[df['ANO_ELEICAO'] == 2018].shape[0], df[df['ANO_ELEICAO'] == 2022].shape[0]]

plt.bar([f'{total_candidatos[0]:,}\n\nEleições 2018', f'{total_candidatos[1]:,}\n\nEleições 2022'],total_candidatos)
plt.xlabel('')
plt.ylabel('Nº de candidatos\n')
plt.title('Total de candidatos a todos os cargos\n')
plt.show()

"""## Candidatos por partido"""

# Corrige a sigla dos partidos que mudaram de nome entre 2018 e 2022
# Para partidos incorporados mudamos o nome retroativamente, para efeito de comparação

nome_partido = {'PR':'PL', 'PPS':'CIDADANIA', 'PRB':'REPUBLICANOS', 'DEM':'UNIÃO', 'PTC':'AGIR', 'PSL':'UNIÃO',
                'PPL': 'PC do B', 'PRP':'PATRIOTA', 'PHS':'PODE'}

df['SG_PARTIDO'] = df.SG_PARTIDO.replace(nome_partido)

ranking_partidos = df.groupby(['SG_PARTIDO', 'ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index().sort_values(by='SQ_CANDIDATO', ascending=False).reset_index(drop=True)
ranking_partidos = ranking_partidos.pivot(index='SG_PARTIDO', columns='ANO_ELEICAO', values='SQ_CANDIDATO').fillna(0).astype(int).sort_values(by=2022, ascending=False)

ranking_partidos.reset_index()

"""## Candidatos por raça"""

df['DS_COR_RACA'] = df.DS_COR_RACA.replace('NÃO DIVULGÁVEL', 'NÃO INFORMADO')
raca = df.groupby(['ANO_ELEICAO', 'DS_COR_RACA']).SQ_CANDIDATO.count().reset_index().sort_values(by=['DS_COR_RACA', 'ANO_ELEICAO'], ascending=True)
raca.columns = ['Eleição', 'Cor/Raça', 'Candidatos']
raca['Cor/Raça'] = raca['Cor/Raça'].str.capitalize()

raca

raca_pie_1 = raca[raca['Eleição'] == 2018].Candidatos
raca_pie_2 = raca[raca['Eleição'] == 2022].Candidatos
raca_pie_labels = raca[raca['Eleição'] == 2022]['Cor/Raça']

raca_colors = ['#f9c97d', '#ffdbac', '#f09c81', '#cccccc', '#c68642', '#8d5524']

fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(6)
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.pie(raca_pie_1, autopct='%1.1f%%', colors=raca_colors)
ax2.pie(raca_pie_2, autopct='%1.1f%%', colors=raca_colors)

ax1.title.set_text('Eleições 2018')
ax2.title.set_text('Eleições 2022')
plt.legend(raca_pie_labels, bbox_to_anchor=(1,1))
plt.suptitle('Candidatos por Raça/Cor')

plt.show()

"""### Partidos com mais negros/pardos (%)"""

raca_partido = df.groupby(['ANO_ELEICAO','DS_COR_RACA', 'SG_PARTIDO']).SQ_CANDIDATO.count().reset_index().sort_values(by='SQ_CANDIDATO', ascending=False)

raca_partido

partido_raca = pd.pivot(raca_partido[raca_partido.ANO_ELEICAO == 2022],index='SG_PARTIDO',columns='DS_COR_RACA', values='SQ_CANDIDATO').fillna(0).astype(int).reset_index()

partido_raca

partido_raca['TODAS'] = partido_raca['PRETA']+partido_raca['PARDA']+partido_raca['AMARELA']+partido_raca['BRANCA']+partido_raca['INDÍGENA']+partido_raca['NÃO INFORMADO']

partido_raca['pct_pretos_pardos'] = ((partido_raca['PRETA']+partido_raca['PARDA'])/partido_raca['TODAS']*100).round(1)

raca_ranking = partido_raca.sort_values(by='pct_pretos_pardos', ascending=False).reset_index(drop=True)

raca_ranking.columns

raca_ranking.columns = ['Partido', 'Amarela', 'Branca', 'Indígena', 
                        'Não informado', 'Parda', 'Preta', 'Todas', 
                        'Pretos+Pardos (%)']

negros_ranking = raca_ranking[['Partido', 'Parda', 'Preta', 'Todas', 'Pretos+Pardos (%)']]

negros_ranking

"""### Partidos com mais indígenas (%)"""

raca_ranking['Indigenas (%)'] = (raca_ranking['Indígena']/raca_ranking['Todas']*100).round(1)

ranking_indigenas = raca_ranking.sort_values(by='Indigenas (%)', ascending=False)[['Partido', 'Indígena', 'Todas', 'Indigenas (%)']]

ranking_indigenas

"""## Candidatos por gênero"""

genero = df.groupby(['ANO_ELEICAO', 'DS_GENERO']).SQ_CANDIDATO.count().reset_index().sort_values(by=['ANO_ELEICAO', 'DS_GENERO'], ascending=True)
genero.columns = ['Eleição', 'Gênero', 'Candidatos']
genero['Gênero'] = genero['Gênero'].str.capitalize()
genero = genero[genero['Gênero'] != 'Não Divulgável']
genero

genero_pie_1 = genero[genero['Eleição'] == 2018].Candidatos
genero_pie_2 = genero[genero['Eleição'] == 2022].Candidatos
genero_pie_labels = genero[genero['Eleição'] == 2018]['Gênero']

fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(6)
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.pie(genero_pie_1, autopct='%1.1f%%', colors=['#ff6666', '#6666ff', '#cccccc'])
ax2.pie(genero_pie_2, autopct='%1.1f%%', colors=['#ff6666', '#6666ff', '#cccccc'])

ax1.title.set_text('Eleições 2018')
ax2.title.set_text('Eleições 2022')
plt.legend(genero_pie_labels, bbox_to_anchor=(1,1))
plt.suptitle('Candidatos por Gênero')

plt.show()

"""### Disparidade de gênero por idade"""

idade_genero = df[df.ANO_ELEICAO == 2022].groupby(['NR_IDADE_DATA_POSSE', 'DS_GENERO']).SQ_CANDIDATO.count().reset_index().sort_values(by='NR_IDADE_DATA_POSSE', ascending=False).reset_index(drop=True)

idade_genero = idade_genero.pivot(index='NR_IDADE_DATA_POSSE', columns='DS_GENERO', values='SQ_CANDIDATO').reset_index().fillna(0).astype(int)

idade_genero = idade_genero.sort_values(by='NR_IDADE_DATA_POSSE').reset_index(drop=True)
idade_genero['NR_IDADE_DATA_POSSE'] = idade_genero['NR_IDADE_DATA_POSSE'].astype(int)

idade_genero.columns = ['Idade', 'Feminino', 'Masculino']

idade_genero

idade_melt = pd.melt(idade_genero, id_vars=['Idade'], value_vars=['Feminino', 'Masculino'])

idade_melt.columns = ['Idade', 'Gênero', 'Candidatos']

plt.figure(figsize = (20,6))
plt.title('Candidatos por idade e gênero', size=28)
sns.barplot(data=idade_melt, x="Idade", y='Candidatos', hue="Gênero", palette=['#ff6666', '#6666ff'])
# plt.xticks()
plt.show()

"""### Partidos com mais mulheres (%)"""

genero_partido = df[df.ANO_ELEICAO == 2022].groupby(['SG_PARTIDO', 'DS_GENERO']).SQ_CANDIDATO.count().reset_index().sort_values(by='SQ_CANDIDATO', ascending=False).pivot(columns='DS_GENERO', index='SG_PARTIDO', values='SQ_CANDIDATO').fillna(0).astype(int).reset_index()

genero_partido['pct_mulheres'] = (genero_partido['FEMININO']*100/(genero_partido['FEMININO']+genero_partido['MASCULINO'])).round(1)

genero_partido = genero_partido.sort_values(by='pct_mulheres', ascending=False).reset_index(drop=True)

genero_partido.columns = ['Partido', 'Mulheres', 'Homens', 'Não informado', 'Mulheres (%)']

genero_partido.insert(loc=0, column='Posição', value=pd.Series(genero_partido.index.values)+1)

genero_partido

"""## Escolaridade dos candidatos"""

escolaridade = df.groupby(['ANO_ELEICAO', 'CD_GRAU_INSTRUCAO', 'DS_GRAU_INSTRUCAO']).SQ_CANDIDATO.count().reset_index().sort_values(by='CD_GRAU_INSTRUCAO', ascending=True)

escolaridade['DS_GRAU_INSTRUCAO'] = escolaridade['DS_GRAU_INSTRUCAO'].str.capitalize()

escolaridade.columns = ['Eleição', 'Código', 'Grau de instrução', 'Número de candidatos']

escolaridade = escolaridade.pivot(index=['Código', 'Grau de instrução'], columns='Eleição', values='Número de candidatos').fillna(0).astype(int).reset_index().sort_values(by='Código', ascending=False)[['Grau de instrução', 2018, 2022]].reset_index(drop=True)

escolaridade['2018 (%)'] = (escolaridade[2018]/escolaridade[2018].sum()*100).round(1)

escolaridade['2022 (%)'] = (escolaridade[2022]/escolaridade[2022].sum()*100).round(1)

escolaridade_t = escolaridade.transpose().reset_index()[3:]

escolaridade_t.columns = ['Eleição'] + escolaridade['Grau de instrução'].to_list()

escolaridade_t = escolaridade_t.set_index('Eleição')

# create stacked bar chart for monthly temperatures
escolaridade_t.plot(kind='bar', stacked=True, color=['#000000', '#555555', '#555555', '#999999', '#999999', '#dddddd', '#dddddd', '#ffffff'])
 
# labels for x & y axis
plt.xlabel('Eleição', rotation=0)
plt.ylabel('% das candidaturas')
plt.xticks(rotation=0)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
 
# title of plot
plt.title('Grau de instrução dos candidatos\n')
plt.show()

escolaridade_t

escolaridade

escolaridade_partido = df.groupby(['ANO_ELEICAO', 'SG_PARTIDO', 'CD_GRAU_INSTRUCAO', 
                                   'DS_GRAU_INSTRUCAO']).SQ_CANDIDATO.count().reset_index().sort_values(by=['ANO_ELEICAO', 'SG_PARTIDO',
                                                                                                            'CD_GRAU_INSTRUCAO'], ascending=False)

escolaridade_partido[escolaridade_partido['ANO_ELEICAO'] == 2022].reset_index(drop=True)

"""### Partidos com mais diplomados (%)"""

escolaridade_partido = escolaridade_partido[(escolaridade_partido['DS_GRAU_INSTRUCAO'] == 'SUPERIOR COMPLETO') & (escolaridade_partido['ANO_ELEICAO'] == 2022)]

diplomados_partido = escolaridade_partido[escolaridade_partido['DS_GRAU_INSTRUCAO'] == 'SUPERIOR COMPLETO'].reset_index(drop=True)

diplomados_partido.columns = ['Eleição', 'Partido', 'Código', 'Grau de instrução', 'Candidatos com superior completo']

diplomados_partido = diplomados_partido[['Eleição', 'Partido', 'Candidatos com superior completo']]

# Cria um outro dataframe com os totais de candidatos, para fusão

ranking_partidos_merger = ranking_partidos.reset_index()[['SG_PARTIDO', 2022]]

ranking_partidos_merger.columns = ['Partido', 'Total de candidatos']

diplomados_partido = diplomados_partido.merge(ranking_partidos_merger, how='left', on='Partido')

diplomados_partido['Percentual de diplomados'] =(diplomados_partido['Candidatos com superior completo']/diplomados_partido['Total de candidatos']*100).round(1)

diplomados_partido = diplomados_partido.sort_values(by='Percentual de diplomados', ascending=False).reset_index(drop=True)

diplomados_partido

"""# Recortes por profissão"""

profissoes = df.groupby(['ANO_ELEICAO', 'CD_OCUPACAO','DS_OCUPACAO']).SQ_CANDIDATO.count().reset_index().sort_values(by=['ANO_ELEICAO','SQ_CANDIDATO'], ascending=False).reset_index(drop=True)

# Quantidade de profissões diferentes no dataset

len(profissoes.DS_OCUPACAO.unique())

top10_2018 = profissoes[(profissoes['ANO_ELEICAO'] == 2018) & (profissoes['DS_OCUPACAO'] != 'OUTROS')].head(10).reset_index(drop=True)

top10_2022 = profissoes[(profissoes['ANO_ELEICAO'] == 2022) & (profissoes['DS_OCUPACAO'] != 'OUTROS')].head(10).reset_index(drop=True)

top10_2022.columns = ['Eleição', 'Código', 'Eleição 2022' , 'Candidatos']
top10_2018.columns = ['Eleição', 'Código', 'Eleição 2018' , 'Candidatos']
top10_2022 = top10_2022[['Eleição 2022', 'Candidatos']]
top10_2018 = top10_2018[['Eleição 2018', 'Candidatos']]
top10_profissoes = pd.concat([top10_2018, top10_2022], axis=1).reset_index()

top10_profissoes['Eleição 2018'] = top10_profissoes['Eleição 2018'].str.capitalize()
top10_profissoes['Eleição 2022'] = top10_profissoes['Eleição 2022'].str.capitalize()

"""### Top 10 profissões"""

top10_profissoes.columns = ['Posição', 'Eleição 2018', 'Candidatos', 'Eleição 2022', 'Candidatos']

# top10_profissoes['Posição'] = top10_profissoes['Posição']+1

top10_profissoes

# Agrupamentos por códigos de profissão

militar_ou_policia = [232, 233, 295, 921, 258] # 254 é vigilante (tirei)

religioso = [910]

profissionais_saude = [109, 111, 113, 115, 132, 243, 225, 229, 114, 118, 248, 117, 592]

# 109 agente de saúde, operador de equipamento médico, paramédico, fisioterapeuta, fono, terapeuta

professor = [142, 143, 265, 266, 230, 235]

profissoes[profissoes.CD_OCUPACAO.isin(profissionais_saude)]['DS_OCUPACAO'].str.capitalize().unique()

cd_militar_ou_policia = profissoes[profissoes.CD_OCUPACAO.isin(militar_ou_policia)].groupby(['ANO_ELEICAO']).SQ_CANDIDATO.sum().reset_index()
cd_militar_ou_policia['Profissão'] = 'Militar ou policial'

cd_religioso = profissoes[profissoes.CD_OCUPACAO.isin(religioso)].groupby(['ANO_ELEICAO']).SQ_CANDIDATO.sum().reset_index()
cd_religioso['Profissão'] = 'Sacerdote ou agente religioso'

cd_profissionais_saude = profissoes[profissoes.CD_OCUPACAO.isin(profissionais_saude)].groupby(['ANO_ELEICAO']).SQ_CANDIDATO.sum().reset_index()
cd_profissionais_saude['Profissão'] = 'Médico ou profissional de saúde'

cd_professor = profissoes[profissoes.CD_OCUPACAO.isin(professor)].groupby(['ANO_ELEICAO']).SQ_CANDIDATO.sum().reset_index()
cd_professor['Profissão'] = 'Professores'

profissoes_grupos = pd.concat([cd_militar_ou_policia, cd_religioso, cd_profissionais_saude, cd_professor])

profissoes_grupos.columns = ['Eleição', 'Candidatos', 'Ocupação']

"""## Por grupos de profissões"""

fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(9)
fig.text(0.04, 0.5, 'Número de candidatos', va='center', rotation='vertical')
fig.text(0.5, 0.04, 'Eleições', ha='center')

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

ax1.plot(['2018','2022'], cd_militar_ou_policia.SQ_CANDIDATO, marker='o')
ax1.set_ylim([0, cd_militar_ou_policia.SQ_CANDIDATO.max()*1.1])
ax1.title.set_text('Militares ou policiais')

ax2.plot(['2018','2022'], cd_religioso.SQ_CANDIDATO, marker='o')
ax2.set_ylim([0, cd_religioso.SQ_CANDIDATO.max()*1.1])
ax2.title.set_text('Sacerdotes ou agentes religiosos')

ax3.plot(['2018','2022'], cd_profissionais_saude.SQ_CANDIDATO, marker='o')
ax3.set_ylim([0, cd_profissionais_saude.SQ_CANDIDATO.max()*1.1])
ax3.title.set_text('Médicos e profissionais de saúde')

ax4.plot(['2018','2022'], cd_professor.SQ_CANDIDATO, marker='o')
ax4.set_ylim([0, cd_professor.SQ_CANDIDATO.max()*1.1])
ax4.title.set_text('Professores')

plt.suptitle('Candidatos por grupos de profissões', size=20)
plt.show()

"""# Dataframes para exportação
Daqui para baixo é só o código de exportação para o Flourish
"""

total_cand_2022 = total_candidatos[1]
total_historico_data = {'Eleição':[1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022], 
                        'Candidatos':[6623, 15040, 18049, 19263, 22537, 26161, 29085, total_cand_2022]}

total_historico = pd.DataFrame(data=total_historico_data)
total_historico

negros_partido = raca_ranking[['Partido', 'Parda', 'Preta', 'Todas', 'Pretos+Pardos (%)']]

negros_partido['Outras'] = negros_partido['Todas']-negros_partido['Preta']-negros_partido['Parda']

negros_partido = negros_partido[['Partido', 'Preta', 'Parda', 'Outras', 'Pretos+Pardos (%)']]

negros_partido.insert(loc=0, column='Posição', value=pd.Series(negros_partido.index.values)+1)

negros_partido

ranking_indigenas = ranking_indigenas.reset_index(drop=True)

ranking_indigenas = ranking_indigenas[['Partido', 'Indígena', 'Todas', 'Indigenas (%)']]

ranking_indigenas.insert(loc=0, column='Posição', value=pd.Series(ranking_indigenas.index.values)+1)

ranking_indigenas.columns = ['Posição', 'Partido', 'Indígenas', 'Todos', 'Indígenas (%)']

negros_ranking.insert(loc=0, column='Posição', value=pd.Series(negros_ranking.index.values)+1)

negros_ranking.columns = ['Posição', 'Partido', 'Pretos', 'Pardos', 'Todos', 'Pretos e pardos (%)']

top10_profissoes.columns = ['Posição', 'Eleição 2018', 'Candidatos', 'Eleição 2022', 'Candidatos']

top10_profissoes['Posição'] = top10_profissoes['Posição']+1

# Formulas para criar coluna de índice numérico iniciada por 1

# dfx['Posição'] = pd.Series(dfx.index.values)+1

# dfx.insert(loc=idx, column='Posição', value=pd.Series(dfx.index.values)+1)

escolaridade_exp = escolaridade.transpose().reset_index()

escolaridade_exp.columns = escolaridade_exp.iloc[0]

escolaridade_exp.columns = ['Eleição', 'Superior completo', 'Superior incompleto',
       'Ensino médio completo', 'Ensino médio incompleto',
       'Ensino fundamental completo', 'Ensino fundamental incompleto',
       'Lê e escreve', 'Não divulgável']

escolaridade_exp = escolaridade_exp[1:3]

ranking_partidos_exp = ranking_partidos.reset_index()

total_2022 = ranking_partidos[2022].sum()
total_2018 = ranking_partidos[2018].sum()

total_2022 = '{:,}'.format(total_2022).replace(',', '.')
total_2018 = '{:,}'.format(total_2018).replace(',', '.')

ranking_partidos_exp.columns = ['Partido', 'Eleições 2018', 'Eleições 2022']

ranking_partidos_exp

# Ajeita a tabela de raça para incluir porcentagens

raca_2018 = raca[raca['Eleição'] == 2018].reset_index(drop=True)
raca_2022 = raca[raca['Eleição'] == 2022].reset_index(drop=True)
raca_2018['Candidatos (%)'] = (raca_2018['Candidatos'] / total_candidatos[0]*100).round(1)
raca_2022['Candidatos (%)'] = (raca_2022['Candidatos'] / total_candidatos[1]*100).round(1)
raca = pd.concat([raca_2018, raca_2022]).reset_index(drop=True)

genero_2018 = genero[genero['Eleição'] == 2018].reset_index(drop=True)
genero_2022 = genero[genero['Eleição'] == 2022].reset_index(drop=True)
genero_2018['Candidatos (%)'] = (genero_2018['Candidatos'] / total_candidatos[0]*100).round(1)
genero_2022['Candidatos (%)'] = (genero_2022['Candidatos'] / total_candidatos[1]*100).round(1)
genero = pd.concat([genero_2018, genero_2022]).reset_index(drop=True)

genero



diplomados_partido = diplomados_partido[['Partido', 'Candidatos com superior completo', 'Total de candidatos', 'Percentual de diplomados']]

diplomados_partido.columns = ['Partido', 'Candidatos com diploma superior', 'Total',
                              'Diplomados (%)']

diplomados_partido['Candidatos sem diploma superior'] = diplomados_partido['Total']-diplomados_partido['Candidatos com diploma superior']

diplomados_partido = diplomados_partido[['Partido', 'Candidatos com diploma superior', 'Candidatos sem diploma superior', 'Diplomados (%)']]

diplomados_partido.insert(loc=0, column='Posição', value=pd.Series(diplomados_partido.index.values)+1)

diplomados_partido



# Outros recortes

"""# Outros recortes

## Geral de profissões
"""

# Guia de codigos de profissao

# df[['CD_OCUPACAO', 'DS_OCUPACAO']].drop_duplicates().sort_values(by='CD_OCUPACAO').reset_index(drop=True).to_csv('guia_profissoes.csv', index=False)

profissao_compara = df.groupby(['DS_OCUPACAO', 'ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

profissao_compara.replace('VEREADOR', 'SENADOR, DEPUTADO E VEREADOR', inplace=True)

profissao_compara.replace('SENADOR', 'SENADOR, DEPUTADO E VEREADOR', inplace=True)

profissao_compara.replace('DEPUTADO', 'SENADOR, DEPUTADO E VEREADOR', inplace=True)

profissao_compara.replace('PROFESSOR DE ENSINO FUNDAMENTAL','PROFESSOR DE ENSINO DE PRIMEIRO E SEGUNDO GRAUS', inplace=True)

profissao_compara.replace('PROFESSOR DE ENSINO MÉDIO','PROFESSOR DE ENSINO DE PRIMEIRO E SEGUNDO GRAUS', inplace=True)

profissao_compara = profissao_compara.groupby(['DS_OCUPACAO', 'ANO_ELEICAO']).SQ_CANDIDATO.sum().reset_index()

profissao_compara = profissao_compara.pivot(index='DS_OCUPACAO', columns='ANO_ELEICAO', values='SQ_CANDIDATO').fillna(0).astype(int).reset_index()

profissao_compara['Variação'] = ((profissao_compara[2022]/profissao_compara[2018]-1)*100).round(1)

profissao_compara = profissao_compara.sort_values(by='Variação', ascending=False).reset_index(drop=True)

profissao_compara['Soma'] = profissao_compara[2018]+profissao_compara[2022]

# profissao_compara.sort_values(by='Soma', ascending=False).head(50).sort_values(by='Variação', ascending=False).reset_index(drop=True)

"""## Policiais e Militares"""

policia_milico = [232, 233, 295, 921, 258, 254]

policia_milico = df[df['CD_OCUPACAO'].isin(policia_milico)].reset_index(drop=True)

policia_milico = policia_milico.groupby(['DS_OCUPACAO', 'ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

#.pivot(index='DS_OCUPACAO', columns='ANO_ELEICAO', values='SQ_CANDIDATO')

policia_milico.columns = ['Ocupação', 'Eleição', 'Candidatos']

policia_milico['Ocupação'] = policia_milico['Ocupação'].str.title()

policia_milico #.to_csv('militares_policiais.csv', index=False)

"""### Checa policiais federais"""

len(df[(df.ANO_ELEICAO == 2018) & (df.NM_URNA_CANDIDATO.str.contains('FEDERAL'))].NM_URNA_CANDIDATO)

df[df.NM_URNA_CANDIDATO.str.contains('FEDERAL')].NM_URNA_CANDIDATO.to_list()



"""## Nomes identitários"""

militares = ['ALMIRANTE', 'CAPITÃO', 'CAPITÃ', 'TENENTE', 'SARGENTO', 'SOLDADO',
             'CABO', 'MARINHEIRO', 'MARECHAL', 'GENERAL', 'CORONEL', 'MAJOR', 
             'ASPIRANTE' 'FUZILEIRO', 'RECRUTA', 'CADETE', 'TAIFEIRO', 'SUBOFICIAL',  
             'CAP.', 'CEL.', 'MAL.', 'TEN.', 'GEN.', 'GAL.', 'MAJ.', 'CAP.', 'SGT.', 
             'ALTE.', 'SOLDADA', 'SARGENTA', 'CORONELA', 'GENERALA']

policiais = ['DELEGADO', 'DELEGADA', 'POLICIAL', 'POLÍCIA', 'PM', 'DEL.']

medico_enfermeiro = ['DOUTOR', 'DOUTORA', 'DR ', 'DR.', 'DRA.', 'ENFERMEIR', 
                     'DENTISTA', 'PSICÓLOG', 'SAÚDE', 'FISIOTERAP', 'FONOAUDI']

ensino = ['PROFESSOR', 'PROF.', 'PROFA.', 'PROF ', 'PROFA ']

religiao = ['PASTOR ', 'PASTORA ', 'PADRE ', 'PE.', 'BISPO', 'APÓSTOLO', 
            'MISSIONÁRI', 'DIÁCON', 'CARDEAL', 'MONGE', 'VIGÁRIO', 'RABINO',
            'MONJA', 'FREIRA', 'IRMÃ', 'FREI ', 'FRADE', 'IRMÃO']

empty_df = df[df['NM_URNA_CANDIDATO'].str.contains("XXXXXXXXXXXXXXX")]

nomes_policiais = empty_df

for i in policiais:
    nomes_policiais = pd.concat([nomes_policiais, df[df['NM_URNA_CANDIDATO'].str.contains(i, regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_policiais = nomes_policiais.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_policiais['Referências no nome'] = 'Policiais'
gr_policiais

nomes_militares = empty_df

for i in militares:
    nomes_militares = pd.concat([nomes_militares, df[df['NM_URNA_CANDIDATO'].str.contains(i, regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_militares = nomes_militares.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_militares['Referências no nome'] = 'Militares'
gr_militares

nomes_saude = empty_df

for i in medico_enfermeiro:
    nomes_saude = pd.concat([nomes_saude, df[df['NM_URNA_CANDIDATO'].str.contains(i, regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_saude = nomes_saude.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_saude['Referências no nome'] = 'Profissionais de saúde'
gr_saude

nomes_bombeiro = empty_df

nomes_bombeiro = pd.concat([nomes_bombeiro, df[df['NM_URNA_CANDIDATO'].str.contains('BOMBEIR', regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_bombeiro = nomes_bombeiro.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_bombeiro['Referências no nome'] = 'Bombeiros'
gr_bombeiro

nomes_professor = empty_df

for i in ensino:
    nomes_professor = pd.concat([nomes_professor, df[df['NM_URNA_CANDIDATO'].str.contains(i, regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_professor = nomes_professor.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_professor['Referências no nome'] = 'Professores'
gr_professor

nomes_religiao = empty_df

for i in religiao:
    nomes_religiao = pd.concat([nomes_religiao, df[df['NM_URNA_CANDIDATO'].str.contains(i, regex=False)].reset_index(drop=True)]).reset_index(drop=True)

gr_religiao = nomes_religiao.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_religiao['Referências no nome'] = 'Religiosos'
gr_religiao

nomes_referencias = pd.concat([gr_professor, gr_religiao, gr_militares, gr_policiais, gr_bombeiro, gr_saude]).reset_index(drop=True)

nomes_referencias.columns = ['Eleição', 'Candidatos', 'Referências no nome']

nomes_referencias

"""## Nomes com 'Lula e Bolsonaro'"""

nomes_bolsonaro = df[df['NM_URNA_CANDIDATO'].str.contains('BOLSONARO', regex=False)].reset_index(drop=True)

nomes_bolsonaro = nomes_bolsonaro.drop_duplicates()

gr_bolsonaro = nomes_bolsonaro.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_bolsonaro['Referência'] = 'Bolsonaro'

nomes_lula = df[df['NM_URNA_CANDIDATO'].str.contains('LULA', regex=False)].reset_index(drop=True)

nomes_lula = nomes_lula.drop_duplicates()

gr_lula = nomes_lula.groupby(['ANO_ELEICAO']).SQ_CANDIDATO.count().reset_index()

gr_lula['Referência'] = 'Lula'

lula_nomes = nomes_lula[['NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'DS_CARGO', 'ANO_ELEICAO', 'SG_PARTIDO', 'SG_UF']].drop_duplicates().reset_index(drop=True)

bolsonaro_nomes = nomes_bolsonaro[['NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'DS_CARGO', 'ANO_ELEICAO', 'SG_PARTIDO', 'SG_UF']].drop_duplicates().reset_index(drop=True)

nomes_lula_bolsonaro_numeros = pd.concat([gr_lula,gr_bolsonaro])
nomes_lula_bolsonaro_numeros

nomes_lula_bolsonaro = pd.concat([lula_nomes, bolsonaro_nomes]).reset_index(drop=True)

"""## Mudança de raça"""

df.DS_COR_RACA.unique()

# list_1 =  ['BRANCA','PARDA','PRETA','AMARELA','NÃO INFORMADO', 'INDÍGENA']
# list_2 =  ['BRANCA','PARDA','PRETA','AMARELA','NÃO INFORMADO', 'INDÍGENA']
#  
# for i in list_1:
#     for j in list_2:
#         print(f'"{i}{j}":"{j}", ', end="")

replacer_cor = {"BRANCABRANCA":"BRANCA", "BRANCAPARDA":"PARDA", "BRANCAPRETA":"PRETA", "BRANCAAMARELA":"AMARELA", "BRANCANÃO INFORMADO":"NÃO INFORMADO", "BRANCAINDÍGENA":"INDÍGENA", "PARDABRANCA":"BRANCA", "PARDAPARDA":"PARDA", "PARDAPRETA":"PRETA", "PARDAAMARELA":"AMARELA", "PARDANÃO INFORMADO":"NÃO INFORMADO", "PARDAINDÍGENA":"INDÍGENA", "PRETABRANCA":"BRANCA", "PRETAPARDA":"PARDA", "PRETAPRETA":"PRETA", "PRETAAMARELA":"AMARELA", "PRETANÃO INFORMADO":"NÃO INFORMADO", "PRETAINDÍGENA":"INDÍGENA", "AMARELABRANCA":"BRANCA", "AMARELAPARDA":"PARDA", "AMARELAPRETA":"PRETA", "AMARELAAMARELA":"AMARELA", "AMARELANÃO INFORMADO":"NÃO INFORMADO", "AMARELAINDÍGENA":"INDÍGENA", "NÃO INFORMADOBRANCA":"BRANCA", "NÃO INFORMADOPARDA":"PARDA", "NÃO INFORMADOPRETA":"PRETA", "NÃO INFORMADOAMARELA":"AMARELA", "NÃO INFORMADONÃO INFORMADO":"NÃO INFORMADO", "NÃO INFORMADOINDÍGENA":"INDÍGENA", "INDÍGENABRANCA":"BRANCA", "INDÍGENAPARDA":"PARDA", "INDÍGENAPRETA":"PRETA", "INDÍGENAAMARELA":"AMARELA", "INDÍGENANÃO INFORMADO":"NÃO INFORMADO", "INDÍGENAINDÍGENA":"INDÍGENA"}

mraca = df[['ANO_ELEICAO', 'DS_COR_RACA', 'NR_CPF_CANDIDATO']].drop_duplicates()

mraca

mraca = mraca.groupby(['NR_CPF_CANDIDATO', 'ANO_ELEICAO']).DS_COR_RACA.sum().reset_index()

mraca

mraca_t = mraca.pivot(index='NR_CPF_CANDIDATO', columns='ANO_ELEICAO', values='DS_COR_RACA').dropna()

gera_listao = mraca_t

gera_listao = gera_listao.replace(replacer_cor)

gera_listao = gera_listao[gera_listao[2018] != gera_listao[2022]].reset_index()

CPFs_mudaraca = gera_listao.NR_CPF_CANDIDATO.to_list()

listao_raca = df[df['NR_CPF_CANDIDATO'].isin(CPFs_mudaraca)]

df.columns

df.DS_SITUACAO_CANDIDATO_TOT.unique()

listao_raca = listao_raca[['NR_CPF_CANDIDATO', 'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'DS_CARGO',
                    'NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'DS_COR_RACA', 'SG_PARTIDO', 'SG_UF']]

listao_raca.DT_GERACAO.unique()

listao_raca = listao_raca[['NR_CPF_CANDIDATO', 'ANO_ELEICAO', 'DS_CARGO', 'NM_CANDIDATO',
             'NM_URNA_CANDIDATO', 'DS_COR_RACA', 'SG_PARTIDO', 'SG_UF']].sort_values(by=['NR_CPF_CANDIDATO', 'ANO_ELEICAO'])

listao_raca = listao_raca.reset_index(drop=True)

listao_raca.to_csv('mudancas_de_raca.csv', index=False)

mraca_t = mraca_t.replace(replacer_cor)

mraca_t = mraca_t[mraca_t[2018] != mraca_t[2022]]

mraca_t['Mudança'] = mraca_t[2018].astype(str) + ' > ' + mraca_t[2022].astype(str)

mraca_t

# aqui cria a tabela para fucar



mraca_exp= mraca_t.groupby(['Mudança']).count().reset_index()

mraca_exp

separa_colunas = pd.DataFrame(mraca_exp['Mudança'].str.split(' > ').tolist(), columns=['Declaração em 2018', 'Declaração em 2022'])

mraca_exp = pd.concat([mraca_exp, separa_colunas], axis=1)

mraca_exp[' '] = '→'

mraca_exp = mraca_exp[['Declaração em 2018', ' ', 'Declaração em 2022', 2018]]

mraca_exp.columns = ['Raça declarada em 2018', ' ', 'Raça declarada em 2022', 'Candidatos']

mraca_exp['Raça declarada em 2018'] = mraca_exp['Raça declarada em 2018'].str.title()
mraca_exp['Raça declarada em 2022'] = mraca_exp['Raça declarada em 2022'].str.title()

mraca_exp = mraca_exp.sort_values(by='Candidatos', ascending=False).reset_index(drop=True)

"""# Mulheres majoritário"""

mulheres_cargo = df[['DS_GENERO','DS_CARGO','ANO_ELEICAO', 'SQ_CANDIDATO']]

distrital_estadual = {'DEPUTADO DISTRITAL':'DEPUTADO ESTADUAL/DISTRITAL', 'DEPUTADO ESTADUAL':'DEPUTADO ESTADUAL/DISTRITAL'}

mulheres_cargo['DS_CARGO'] = mulheres_cargo['DS_CARGO'].replace(distrital_estadual)

mulheres_exclui = ['1º SUPLENTE', '2º SUPLENTE']

mulheres_cargo = mulheres_cargo[(mulheres_cargo['ANO_ELEICAO'] == 2022) & (mulheres_cargo['DS_CARGO'] != '1º SUPLENTE') & (mulheres_cargo['DS_CARGO'] != '2º SUPLENTE')]

mulheres_cargo = mulheres_cargo.groupby(['DS_CARGO', 'DS_GENERO']).SQ_CANDIDATO.count().reset_index()

mulheres_cargo['DS_CARGO'] = mulheres_cargo['DS_CARGO'].str.title()

mulheres_cargo['DS_GENERO'] = mulheres_cargo['DS_GENERO'].str.title()

mulheres_cargo.columns = ['Cargo disputado', 'Gênero', 'Candidatos']

# mulheres_cargo.to_csv('mulheres_cargo.csv', index=False)

def show_me(x):
    print(x.head(4),'\n...\n',x.tail(4), '\n\n', '*'*70, '\n')

"""# Exporta tabelas"""

from google.colab import files

exporta_itens = [(mraca_exp,'mudancas_raca.csv'),
                 (nomes_lula_bolsonaro, 'nomes_lula_bolsonaro.csv'),
                 (nomes_lula_bolsonaro_numeros, 'nomes_lula_bolsonaro_numeros.csv'),
                 (diplomados_partido, 'escolaridade_partido.csv'),
                 (escolaridade_exp, 'candidatos_escolaridade.csv'),
                 (genero, 'candidatos_genero.csv'),
                 (genero_partido, 'genero_partido.csv'),
                 (mulheres_cargo, 'mulheres_cargo.csv'),
                 (idade_genero, 'idade_genero.csv'),
                 (negros_partido, 'negros_partidos.csv'),
                 (profissoes_grupos, 'profissoes_grupos.csv'),
                 (raca, 'candidatos_raca.csv'),
                 (ranking_indigenas, 'indigenas_partidos.csv'),
                 (ranking_partidos_exp, 'candidatos_partido.csv'),
                 (top10_profissoes, 'profissoes_top10.csv'),
                 (total_historico, 'total_historico.csv'),
                 (nomes_referencias, 'nomes_referencias.csv'),
                 (policia_milico, 'militares_e_policiais.csv'),
                 (profissao_compara, 'profissao_compara.csv')]

for i in exporta_itens:
    i[0].to_csv(i[1], index=False)
    files.download(f"/content/{i[1]}")

for i in exporta_itens:
    print(i[1],'\n')
    show_me(i[0])

