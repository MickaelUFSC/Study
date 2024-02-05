# Study
Foi um projeto realizado durante uma semana de intensivo de django.
O projeto consiste em uma plataforma de auxilio a estudos.
Ela permite cadastrar perguntas de variadas categorias (matematica, portugues, etc) e gerar desafios com as questões criadas.
os desafios são formas de responder as perguntas criadas anteriormente de forma aleatória.
Ao fim, é possível ver um relatório de desempenho sobre acertos e erros de cada categoria.


Para testar:
1) Tenha o python instalado;
2) Crie uma pasta e clone esse repositório dentro dela (se usa o VScode, abra um terminal dentro da pasta e rode "git clone "link do repositório")
3) Abra o ambiente virtual caminhando até seu local de instalação e executando o arquivo Ativate "venv/Scripts/Activate.ps1"
4) Por fim digite no terminal "python manage.py runserver"

observações.
Se o ambiente virtual der problema, crie um novo ambiente seguindo os passos abaixo:
1) pip install virtualenv
2) virtualenv venv
3) venv/Scripts/Activate.ps1
4) pip install django
5) pip install pillow
6) python manage.py makemigration (puxa os itens que ainda não estão no banco de dados)
7) python manage.py migrate (cria o banco de dados com os arquivos faltantes)
8) python manage.py runserver (executa o site em modo localhost)
