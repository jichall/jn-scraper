# JN Scraper

A aplicação é um simples scraper de conteúdo atrelado a uma aplicação Django que
serve para os usuários os produtos encontrados na página. Uma informação mais
detalhada pode ser vista em **doc/requirements.pdf**, acabei fazendo uma
documentação enquanto estava desenvolvendo a aplicação e não vi que existia um
requisito para escrever um README.md.

# Implementação

A implementação se dividiu em etapas pois eu não tinha conhecimento de quais
ferramentas seriam utilizadas no projeto. Para o projeto ser bem sucedido pensei
que deveria primeiro realizar a extração de informação (_scraping_) da página
para posterior persistência e disponibilização via Django.

A primeira coisa que foi feita é umas inspeção na página destinada a ser
utilizada como fonte para a extração de dados. Após a visualização dos
elementos procurei por palavras chave que os tornavam únicos. A seguinte
estrutura que identificava todos os produtos foi encontrada:

``` html
<ul class="products ...">
  <li class="... product ...">
    <a class="woocommerce-LoopProduct-link woocommerce-loop-product__link">
      <img class="attachment-woocommerce_thumbnail ..." src="">
      <img class="attachment-woocommerce_thumbnail ..." src="">
      <h2 class="woocommerce-loop-product__title">
        <span class="ellip">text ellipsed?</span>
        <span class="ellip-line">text ellipsed 2?</span>
      </h2>
      <span class="price">
        <span class="woocommerce-Price-amount amount">
          <span class="woocommerce-Price-currencySymbol">R$</span>
          "49,90"
        </span>
      </span>
    </a>
  </li>
  ...
</ul>
```

Procurei estruturar a estrutura encontrada em notação de objetos JavaScript
(JSON). Observei que um produto poderia ter mais de uma imagem e defini,
por fim, o seguinte objeto:

``` json
o = {
  'name'  : '',
  'img'   : ['', '...', ''],
  'price' : '44,90'
}
```

Após essa etapa, a primeira ferramenta que busquei compreender foi a _Scrapy_,
este framework possibilita a realização da extração de informação de páginas web
de uma maneira bem fácil utilizando seletores CSS ou a linguagem XPath. Para um
contraste entre **Scrapy**, **BeautifulSoup** e **lxml** acesse [1].

Após a compreensão da ferramenta desenvolvi a aplicação para a extração das
informações, localizado na paste **src/jn-scraper/scraper**. As informações
poderiam ser extraídas e exportadas para um arquivo JSON facilmente, o código
abaixo denota como era feita a extração.

``` python
for product in response.css('li.product'):
    product['title'] = product.css('h2.woocommerce-loop-product__title::text').get()
    product.['price'] = product.css('span.price > span::text').get()
    product['images'] = product.xpath('.//img/@src').getall()
```

A integração entre a extração da informação e o Django, entretanto, foi mais
complicada e tomou bastante tempo e ela não foi realizada por completo, detalhe
explicado com mais profundidade no tópico das dificuldades. Para integrar as
duas ferramentas primeiro eu tive que utilizar um plugin, o `scrapy-djangoitem`,
que faz a equivalência dos modelos entre o **Django** e o **Scrapy**.

Essa equivalência, no entanto, dificulta a persistência de alguns objetos que
dependem a criação de outros para serem indexados, como as imagens dos produtos.
O código para a persistência dos objetos extraídos pode ser visto abaixo,
pode-se observar que não difere drasticamente do código anteriormente mostrado e
as únicas diferenças são a utilização dos modelos definidos pelo plugin
mencionado que alteram a maneira de como são atribuídos os valores dos dados
extraídos.

``` python
for product in response.css('li.product'):
            p = Product()
            i = Image()

            # The title is not encoded in UTF-8.
            p['name'] = product.css('h2.woocommerce-loop-product__title::text').get()
            p['price'] = product.css('span.price > span::text').get()

            images = product.xpath('.//img/@src').getall()
            for image in images:
                pi = p.objects.get(name=p['name'])
                i['item'] = pi
                i['src'] = image

            yield p

            for p in ProductItem.objects.all():
                for img in images[p.name]:
                    i = Image()
                    i['item'] = p
                    i['src'] = img
                    yield i
```

A segunda etapa se concretizou pela implementação da interface de acesso aos
dados extraídos, servindo uma página para fácil acesso das informações. As
informações eram extraídas e inseridas de acordo com os modelos definidos pela
aplicação **scraper_app**. O tamanho do framework Django e a minha inexperiência
com este fez com que o  desenvolvimento dessa etapa ficasse mais oneroso e
demandasse mais tempo. O código que foi desenvolvido não tem suas
responsabilidades totalmente separadas, principalmente quando se trata das
páginas definidas na pasta **templates/**, que são as páginas servidas ao
cliente.

A aplicação contém três páginas para acesso das informações, ao iniciá-la
utilizando o Makefile no diretório raíz o usuário pode acesar a URL
`localhost:8000` para encontrar a página inicial. A API RESTful foi
definida de forma que existem dois _endpoints_ de acesso as informações
extraídas.

1. `/products` que retorna todos os produtos extraídos
2. `/products/<id>` que retorna somente um produto dado o seu ID no banco de dados
3. `/json` que retorna todos os produtos extraídos no formato JSON

Após a implementação da API um bug estava ocorrendo ao utilizar o `make`
pois não parecia que a primeira instrução definida na regra `all` se realizava
dado que quando eu tentava visualizar todos os produtos que foram extraídos a
página não retornava nada. Ao fazer cada comando por vez é possível ver que a
página retorna corretamente os dados, ainda não compreendi o porquê no entanto.
Pode ser algo relacionado com cache (?).

Após a criação dessas regras e para fazer a aplicação um pouco mais fácil de ser
executada em outras máquinas decidi criar um container docker, testando dessa
forma a aplicação em um ambiente externo à máquina local. Não tive tempo,
entretanto, de escolher a melhor imagem docker e construí a imagem do
`jn-scraper` com base na imagem do Ubuntu 18.04. Para executar a imagem basta
construí-la com `make docker` e utilizar a instrução `docker run` para iniciar
a imagem em modo interativo.


# Dificuldades

A maior dificuldade foi a não familiaridade com o ambiente Django, o qual tem
uma pequena curva de aprendizado que infelizmente prejudicou o avanço da
implementação de uma interface mais polida para o usuário.

Além desta também houve a dificuldade de integração entre as duas bases de
código, o problema dos módulos estarem em diferentes diretórios dificultou a
inclusão e tive de circunscrever este problema adicionando ao caminho de
importação o diretório que continha o módulo desejado.

# Referências

[1] https://docs.scrapy.org/en/latest/faq.html
