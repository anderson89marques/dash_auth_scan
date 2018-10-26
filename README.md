# dash_auth_scan
Biblioteca que permite a criação de projetos dash com múltiplas páginas, usando o conceito de `convenção-sobre-configuração`,
e permite também autenticação com o google.

```
This lib is developed at Geru Tecnologia e Serviços S.A.
```

## Instalação

```console
$ git clone https://github.com/anderson89marques/dash_auth_scan.git
$ cd dash_auth_scan
$ flit install --symlink --python python
```

# Convenção sobre Configuração: como a biblioteca funciona com módulos.

Para usar a dash_auth_lib é preciso seguir uma convenção 
Para conseguir criar as rotas automaticamente usando dash_auth_lib é preciso que as 
páginas dash estejam dentro do diretório chamado apps/ como mostrado abaixo
```
- app.py
- index.py
- apps
   |-- app1.py
   |-- app2.py
   |-- index.py
```

Além disso, é necessário que os módulos ```app1.py, app2.py, index.py``` tenham uma variável chamada ```layout``` para
que as rotas sejam criadas. Essa variável precisa ser código dash válido. Abaixo exemplo do módulo ```app1.py```. 

```python
import dash_html_components as html

layout = html.Div([
    html.Label("Página 1")
])
```
Assim o dash_auth_scan saberá que o nome do módulo python, que seguir essas conveções, deve se tornar o nome da rota.
Portanto, para o exemplo apresentado, as rotas criadas são: ```['/', '/app1', '/app2']```, pois o módulo index.py é mapeado para ```'/'```.

# Convenção sobre configuração: como a biblioteca funciona com pacotes.

O dash_auth_scan também permite a criação de rotas com vários níveis usando pacotes python junto com os módulos.
Veja o exemplo abaixo.

```
- app.py
- index.py
- apps
   |-- app1.py
   |-- app2.py
   |-- index.py
   |-- home
       |-- __init__.py 
       |-- account.py
```

O pacote ```home``` será o nome da path da url caso dentro do ```__init__.py``` tenha
a variável ```layout```, assim a rota criada será ```/home```. 
Dentro do pacote ```home``` foi adicionado o módulo ```account``` que segue a convenção do exemplo anterior,
ou seja, deve ter uma variável `layout` que represente codigo dash válido, diferença é que a 
path criada será ```/home/account```.

Em https://github.com/anderson89marques/dash_multipage_auth_example tem um exemplo mais completo. 