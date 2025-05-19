# Extrator de Prova POSCOMP


Este projeto tem como objetivo automatizar a extração de questões e imagens das provas do POSCOMP, a partir de arquivos PDF. A ferramenta organiza o conteúdo de forma estruturada, facilitando o reaproveitamento para fins educacionais e análise.

## Funcionalidades

- Leitura de arquivos PDF contendo provas do POSCOMP
- Extração automática das questões com suas respectivas alternativas
- Detecção e associação de imagens às questões correspondentes
- Classificação das questões por área:
  - Matemática
  - Fundamentos da Computação
  - Tecnologia da Computação
- Geração de arquivos com estrutura padronizada (ex: JSON)

## Tecnologias Utilizadas

- Python 3
- Bibliotecas:
  - PyMuPDF (fitz) – leitura e análise de PDFs
  - re – uso de expressões regulares para identificação de padrões
  - os, json – manipulação de arquivos e dados estruturados

## Como executar o projeto

Siga os passos abaixo para executar o extrator localmente:

### 1. Clone o repositório

```bash
git clone https://github.com/Code-AldreySandre/Extrator_de_Prova_Poscomp.git
cd Extrator_de_Prova_Poscomp
```
### 2. (Opcional) Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate     # No Windows
```
### 3. Instale as dependências
```bash
  pip install -r requirements.txt
```
### 4. Coloque o PDF da prova no diretório PROVA (input/)
```bash
Crie um diretório input/ (caso ainda não exista) e coloque dentro dele o PDF da prova do POSCOMP que deseja extrair.
```
### 5. Execute o script principal
```bash
python_extractor.py
```
## Agradecimentos
Este projeto foi inspirado em iniciativas similares de extração de provas educacionais. Em especial:

- [ENEM_PDF_PARSER](https://github.com/caue-paiva/ENEM_PDF_PARSER) – Projeto de Caue Paiva para extração de questões do ENEM.
  
- Agradeço também ao [Laboratório de Inteligência de Dados (LID) da UFPA](https://ufpa.br/orgaos/laboratorio-de-inteligencia-de-dados/) pela oportunidade de crescimento acadêmico e incentivo à pesquisa aplicada.
