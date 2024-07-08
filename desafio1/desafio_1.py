# bibliotecas usadas 
import pandas as pd

# calcular a comissão de cada vendedor 
dados_vendas = pd.read_csv("Vendas.csv")
dados_comissoes = pd.read_csv('Pagamentos.csv')

# tratando os dados 
dados_vendas['Valor da Venda'] = dados_vendas['Valor da Venda'].str.replace('R$ ', '', regex=False)
dados_vendas['Valor da Venda'] = dados_vendas['Valor da Venda'].str.replace('.', '', regex=False)
dados_vendas['Valor da Venda'] = dados_vendas['Valor da Venda'].str.replace(',', '.', regex=False)
dados_vendas['Valor da Venda'] = dados_vendas['Valor da Venda'].astype(float)

# Calcular a comissão básica de 10%
dados_vendas['Comissao'] = dados_vendas['Valor da Venda'] * 0.10

# calcular comissão marketing
dados_vendas['Marketing'] = dados_vendas.apply(lambda row: row['Comissao'] * 0.20 if row['Canal de Venda'] == 'Online' else 0, axis=1)

#calcular comissão gerente
dados_vendas['Gerente'] = dados_vendas.apply(lambda row: row['Comissao'] * 0.10 if row['Comissao'] >= 15000 else 0, axis=1)

#calcular comissão final por venda
dados_vendas['Comissao_Final'] = dados_vendas['Comissao'] - dados_vendas['Gerente'] - dados_vendas['Marketing']

# tabela final 
comissao_final = dados_vendas.groupby(['Nome do Vendedor'])[['Comissao','Comissao_Final']].sum()
comissao_final = comissao_final.reset_index()

# tratando os dados 
dados_comissoes['Comissão'] = dados_comissoes['Comissão'].str.replace('R$ ', '', regex=False)
dados_comissoes['Comissão'] = dados_comissoes['Comissão'].str.replace('.', '', regex=False)
dados_comissoes['Comissão'] = dados_comissoes['Comissão'].str.replace(',', '.', regex=False)
dados_comissoes['Comissão'] = dados_comissoes['Comissão'].astype(float)

# identificando pagamentos errados
comparacao_comissoes = pd.merge(comissao_final, dados_comissoes, on='Nome do Vendedor')
comparacao_comissoes = comparacao_comissoes.drop(comparacao_comissoes[comparacao_comissoes['Comissao_Final'] == comparacao_comissoes['Comissão']].index)

# - Saída Esperada: Uma lista dos pagamentos feitos incorretamente, indicando o vendedor, o valor pago erroneamente e o valor correto que deveria ter sido pago. 
comparacao_comissoes = comparacao_comissoes.rename(columns={'Comissão':'valor pago erroneamente','Comissao_Final':'valor correto'})
comparacao_comissoes = comparacao_comissoes.drop(columns=['Comissao','Data do Pagamento'], axis=1)
comparacao_comissoes.to_csv('Pagamentos errados.csv',index=False)
