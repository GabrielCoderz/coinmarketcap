<h1 align="center">Coin Market Cap</h1>

<h3>Objetivo:</h3>
<p>Extrair as informações mais atuais das criptomoedas, realizar uma transformação e carregar em um banco de dados, juntamente com um processo de orquestração para permitir agendamentos de extração de dados.<p>

<br/>
<div align="center">
  <img width="tamanho da imagem" title="titulo da imagem" src="https://github.com/GabrielCoderz/coinmarketcap/assets/59071043/b5a3946c-a019-43f4-9bd2-48ebc2e835f3"/>
</div>
<br/>

<h3>Tecnologias:</h3>

- <b>Python</b>: Linguagem de programação para extração dos dados da API coinMarketCap.
- <b>Airflow</b>: Orquestra todo o fluxo de pipeline dos dados, desde a extração até o carregamento no banco.
- <b>EC2</b>: Se trata de uma máquina virtual da AWS a qual servirá para hospedar todo o pipeline com o Airflow.
- <b>Postgres</b>: Um banco de dados relacional que servirá para armazenar os dados extraídos e transformados.

<h3>Processo:</h3>
