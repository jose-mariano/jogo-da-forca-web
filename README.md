# Jogo da Forca web

## Introdução
O jogo da forca permite ao usuário testar sua habilidade de reconhecer palavras, mesmo que elas estejam com parte da palavra oculta.

## O jogo
Minha ideia foi construir um site onde o servidor envie palavras aleatórias para o cliente e o mesmo tente adivinha-las. Para isso o cliente pode utilizar
tanto o teclado do computador, quanto o teclado virtual do próprio site (feito para permitir que dispositivos mobile também consiguam acesso ao jogo).
Você conta com apenas a categoria da palavra para adivinha-lá. Além disso é permitido que você erre até 5 letras antes que seu personagem seja enforcado.
Boa sorte!

## Requisitos
- Ter o python 3.5 ou superior instalado.
- Instalar a biblioteca flask do python 3.

## Como jogar?
Primeiramente clone o repositório. Depois, estando dentro do repositório execute com o python 3 o arquivo server.py. Feito isso, abra seu navegador e acesse
a seguinte URL: http://127.0.0.1:5000/

## Adicionando novas categorias e palavras
Para adicionar novas palavras ou categorias, acesse a URL acima e no rodapé da página clique em "Cadastre novas palavras". Você será redirecionado para uma
nova página, nessa página estão todas as palavras atualmente cadastradas no banco de dados. Nessa nova página cline no menu que se encontra no lado superior
esquerdo da tela, na janela que irá abrir, clique em "Add items". Pronto, tendo adicionados as novas palavras e categorias, clique em "Save", que se encontra
abaixo de "Items to be added". Para retornar ao jogo, clique novamente no menu e em "Logout".
