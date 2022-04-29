# House Rocket
## 1 - Questão de negócio
1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
2. Uma vez o imóvel comprado, qual o melhor momento para vendê-los e por qual preço?
---
## 2 - Entendimento do negócio
1. Produto final:
   - Relatório com sugestões de imóveis e valores para compra
   - Relatório com sugestões de imóveis e valores para venda
2. Ferramentas:
   - Python 3.10
   - Visual Studio Code
   - Jupyter Notebook
3. Bibliotecas Python:
   - Pandas
   - Numpy
   - Streamlit
   - Scipy
---
## 3 - Planejamento
1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
   1. Coletar no Kaggle - [House Sales in King County, USA](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction)
   2. Limpeza dos dados
      - Converter datas para datetime
      - Remover datas erradas
      - Remover outliers
   2. Agrupar imóveis por região (zipcode)
   3. Definição das hipóteses para gerar insights (avionáveis e não acionáveis)
      - Fazer uma afirmação
      - Comparar duas variáveis
      - Comparar com um valor base (mediana dos preços dos imóveis por região)
        - H1: Imóveis que possuem vista para água, são 30% mais caros, na média.
        - H2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.
        - H3: Imóveis sem porão possuem sqft_lot, são 50% maiores do que com porão.
        - H4: O crescimento do preço dos imóveis YoY (Year over Year) é de 10%
        - H5: Imóveis com 3 banheiros tem um crescimento MoM (Month over Month) de 15%
   4. Sugerir compra dos imóveis que estão abaixo do preço mediano da região e em boas condições e os com vista para água
   5. Criação de hipóteses
      
   6. Filtrar e criar visualizações para responder as perguntas
   7. Definir quanto a empresa pretende lucrar com a solução
   8. Avaliar se o objetivo foi alcançado

| **Cód Imóvel** | **Região** | **Preço do Imóvel** | **Mediana da Região** | **Condições** |  **Status** |
|:--------------:|:----------:|:-------------------:|:---------------------:|:-------------:|:-----------:|
|      12345     |    44086   |        450000       |         500000        |       3       |   Comprar   |
|      12347     |    44086   |        750000       |         500000        |       3       | Não Comprar |
|      12349     |    44086   |        150000       |         500000        |       1       | Não Comprar |

2. Uma vez o imóvel comprado, qual o melhor momento para vendê-los e por qual preço?
   1. Com os dados já tratados e organizados
   2. Agrupar imóveis por região e estação do ano
   3. Dentro de cada região e estação do ano, calcular a mediana do preço
      1. Se preço de compra for maior que mediana da região + sazonalidade, preço de venda igual a preço de compra + 10%
      2. Se preço de ompra for menor que mediana da região + sazonalidade, preço de venda igual a preço de compra + 30%
   4. Explorar os dados para identificar o impacto dos atributos nos algoritmos de Machine Learning.

| **Cód Imóvel** | **Região** | **Temporada** | **Mediana da Região** | **Preço de Compra** | **Preço de Venda** |
|:--------------:|:----------:|:-------------:|:---------------------:|:-------------------:|:------------------:|
|      12345     |    44086   |     Verão     |         800000        |        450000       |       585000       |
|      12347     |    44086   |    Inverno    |         400000        |        500000       |       550000       |

---
Criar visualizações para responder a cada uma das 10 hipóteses do negócio
Construir uma tabela com as recomendações de compra ou não compra
Construir uma tabela com recomendações de venda com acrescimo de 10 ou 30%
Fornecer as hipóteses e as tabelas no Streamlit
Transformar o projeto em um portfolio
Salvar no github
Escrever o README (AULA 54)

   
   