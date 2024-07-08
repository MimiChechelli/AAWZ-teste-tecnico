# deve ser instalada a biblioteca python-docx usando pip install python-docx no terminal

# biblioteca para ler arquivos doc
from docx import Document
import pandas as pd

# Caminho para o seu arquivo .docx
docx_path = 'Partnership.docx'

# Abrir o documento
doc = Document(docx_path)

# lista de informações dos socios
socios = []

# provavelmente existe alguma forma mais eficiente de fazer essa manipulçao porem nunca tinha feito isso antes 
for i, para in enumerate(doc.paragraphs):
    if i > 3 and i < 14:
        socios.append(para.text)

nomes = []
num_cotas = []

for socio in socios:
    primeiro_ponto = socio.find('.')
    primeira_virgula = socio.find(',')
    nome = socio[primeiro_ponto+2:primeira_virgula]
    ultimo_ponto = socio.rfind('cota')
    ultima_virgula = socio.rfind('de')
    n_cotas = socio[ultima_virgula+3:ultimo_ponto-1]
    nomes.append(nome)  # Remove espaços em branco extras
    num_cotas.append(n_cotas)


df = pd.DataFrame({
    'Nome': nomes,
    'Cotas': num_cotas
})

print(df)