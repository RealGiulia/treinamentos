# Projeto BotSales - Automação no Salesforce + ChatGPT

### Projeto para ser utilizado em treinamentos, no qual é automatizado a captação de solicitações de contatos registrados no Salesforce, seguido da classificação da área de negócio responsável pelo atendimento do caso.

- A automação demo tem como objetivo mostrar aos usuários de nossa plataforma como é possível utilizar os recursos que disponibilizamos no orchestrator para gerenciar e monitorar a automação.


## Pré-requisitos:
1) Instalar o pacote openai no seu ambiente:
    `` pip install openai ``

2) Criar uma API Key
3) Adicionar a API Key nas variáveis de ambiente do seu computador

**Saiba como criar e instalar a API Key nas variáveis de ambiente pelo link: https://platform.openai.com/docs/api-reference/authentication**


## Sobre o projeto:
- O projeto foi criado com o intuito de mostrar aos clientes que utilizam a plataforma Salesforce  que é possível utilizar o framework web botcity para fazer as manipulações no site, e, posteriormente, utilizar o datapool como uma forma de gerenciar processos em lotes.
Utilizando o Template web de projetos, além dos arquivos padrões do template, temos também o arquivo * *gpt_integrator.py* *, o qual irá fazer requisições para a API do ChatGPT.
- Abaixo, você irá compreender como os módulos estão divididos e todas as funções disponíveis, além de compreender a lógica do código.


## Módulo _gpt_integrator.py_:

- O módulo foi feito para realizar a integração com a API do ChatGPT, e permitir que o desenvolvedor faça as requisições HTTPs à API.O módulo consiste na importação do pacote openai, e instanciar a classe OpenAI, além de configurar os parâmetros para realizar a requisição.

- Método get_gpt_answer: 
O método será responsável por enviar uma mensagem e retornar a resposta da LLM, referente à pergunta enviada.
 _-parametros:
  _message (str): String contendo a mensagem a ser enviada ao gpt.

- Retornos:
 _response(dict): Dicionário contendo as informações da resposta devolvida e Status da requisição: Se a requisição for executada com sucesso, o status vai ser “OK”. Caso haja alguma inconsistência ao executar a requisição e ocasionar uma exceção, o status será “FAILED”. A estrutura do dicionário também contém o par chave-valor "message", a qual receberá o seu valor de acordo com a resposta da API.

 Obs.: É possível utilizar o módulo para auxiliar em outras automações. Veja o formato que a resposta é devolvida, assim é possível você utilizar RegEx para extrair o texto de acordo com o necessário, e até fazer ajustes nas perguntas para refinar a resposta mais assertiva.

 - No projeto, iremos utilizar a ferramenta para indicar qual será a área de negócio responsável pelo contato enviado no Salesforce. Iremos enviar o título da solicitação de contato, e passar as áreas de negócio que temos disponíveis. Por fim, iremos pedir para ele indicar qual das áreas de negócios especificadas deve ser acionada para tratar o caso.
	
 - Nos testes aplicados durante o desenvolvimento, o padrão de resposta retornado pelo ChatGPT é a indicação da área de negócio entre dois asteriscos. Sendo assim, para extrair o texto entre os dois asteriscos, utilizei a RegEx para realizar a extração. A RegEx está como:

``` 
    pattern = r'\*\*(.*?)\*\*' 
    message =  completion.choices[0].message.content
    matches = re.findall(pattern, response["message"])
```

 - O retorno do método será a variável response, um dicionário coms as chaves * *status* * e * *message* *. Veja um exemplo:

    ``response = {"status": "OK", "message": message}``

## Módulo _bot.py_:

#### O módulo bot.py é o responsável por executar todo o fluxo da automação. Nele, iremos fazer login no Salesforce, obter as informações de todos os casos, e para cada caso obtido, vamos indicar a unidade de negócio responsável por ele, por meio da integração com o módulo _gpt_integrator.py_. 

 - Iniciamos com os imports dos módulos, Inicialização das classes, e definição de nome e usuário do portal do Salesforce.

    > **Importante**: Substitua os valores das variáveis usr e pwd pelos correspondentes de usuário e senha.

 - Em seguida, iniciamos com toda a obtenção das informações na tabela de casos do Salesforce. Note que estamos utilizando o Framework web Botcity, simplificando as manipulações na DOM do site.

 - No passo-a-passo abaixo, veja o que o código estará executando:

    1. **Importação de Bibliotecas**:
    - O código importa várias bibliotecas necessárias para o funcionamento do bot, como `botcity.web` para automação web, `botcity.maestro` para integração com o BotCity Maestro, e `webdriver_manager` para gerenciar o WebDriver do Firefox.

    2. **Configuração do Bot**:
    - O bot é configurado para rodar no navegador Firefox e não em modo headless (sem interface gráfica).

    3. **Abertura do Navegador e Login**:
    - O bot abre uma página do Salesforce e realiza o login usando as credenciais fornecidas (`usr` e `pwd`).

    4. **Aguarda e Navega**:
    - Após o login, o bot espera alguns segundos para garantir que a página carregue completamente.

    5. **Busca e Processamento de Casos**:
    - O bot localiza uma tabela de casos na página e extrai informações de cada caso, como número, nome, assunto, data e prioridade.

    6. **Integração com GPT**:
    - Para cada caso, o bot utiliza uma integração com um modelo GPT para determinar a unidade de negócios responsável pelo caso, com base no assunto do problema relatado.

    7. **Exibição de Resultados**:
    - O bot imprime a resposta do GPT e extrai a unidade de negócios mencionada na resposta.
    - Inserimos no log o número do caso e o status da resposta do GPT.
    - Adicionamos no Datapool o caso, nome do requisitante, assunto e unidade de negócio responsável

    8. **Finalização**:
    - O bot finaliza a execução e fecha o navegador.
    - Altera o status da automação como "Finalizado".
    - Envia alerta caso haja casos que não foram processados.

