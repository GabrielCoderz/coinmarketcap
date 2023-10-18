<h1 align="center">Projeto em Engenharia de dados</h1>

- Objetivo:

Extrair as informações mais atuais das criptomoedas, realizar uma transformação e carregar em um banco de dados, juntamente com um processo de orquestração para permitir agendamentos de extração de dados.

- Tecnologias:

Python: Linguagem de programação para extração dos dados da API coinMarketCap.
Airflow: Orquestra todo o fluxo de pipeline dos dados, desde a extração até o carregamento no banco.
EC2: Se trata de uma máquina virtual da AWS a qual servirá para hospedar todo o pipeline com o Airflow.
Postgres: Um banco de dados relacional que servirá para armazenar os dados extraídos e transformados.

- Processo: