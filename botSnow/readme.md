# Automação Service Now

## Objetivo do Projeto

Este projeto tem como objetivo demonstrar ao público a possibilidade de utilizar as funcionalidades de logs, erros e alertas do Orchestrator para gerenciar e monitorar a sua automação. A automação exemplificada neste projeto realiza o login em um sistema web, extrai dados de uma tabela e registra essas informações no BotCity Maestro.

## Passo-a-Passo da Automação

1. **Instalação de Dependências**:
   - Certifique-se de instalar todas as dependências necessárias usando:
     ```bash
     pip install --upgrade -r requirements.txt
     ```

2. **Importação de Bibliotecas**:
   - O código importa várias bibliotecas essenciais para a automação, incluindo:
     ```python
     import time
     from botcity.web import WebBot, Browser, By
     from botcity.maestro import *
     from pyshadow.main import Shadow
     from selenium import webdriver
     from datetime import datetime
     from webdriver_manager.chrome import ChromeDriverManager
     ```

3. **Configuração do Bot**:
   - Desativa erros se não estiver conectado ao Maestro:
     ```python
     BotMaestroSDK.RAISE_NOT_CONNECTED = False
     ```

4. **Função Principal (`main`)**:
   - **Inicialização do Maestro**:
     - Obtém a instância do Maestro e a execução da tarefa com parâmetros.
     ```python
     maestro = BotMaestroSDK.from_sys_args()
     execution = maestro.get_execution()
     ```
   - **Configuração do Driver**:
     - Instala e configura o driver do Chrome:
     ```python
     driver_path = ChromeDriverManager().install()
     driver = webdriver.Chrome(driver_path)
     shadow = Shadow(driver)
     ```
   - **Abertura da Página e Login**:
     - Abre a página de login e insere as credenciais:
     ```python
     shadow.driver.get("https://dev258555.service-now.com/now/nav/ui/classic/params/target/u_tech_products_list.do")
     time.sleep(5)
     name_input = driver.find_element(By.ID, "user_name")
     name_input.send_keys("admin")
     pwd_input = driver.find_element(By.ID, "user_password")
     pwd_input.send_keys("iYy=FO3x1dN=")
     time.sleep(2)
     login_btn = driver.find_element(By.ID, "sysverb_login")
     login_btn.click()
     time.sleep(5)
     ```
   - **Manipulação de Shadow DOM e Iframe**:
     - Encontra e muda para o iframe necessário:
     ```python
     frame = shadow.find_element_by_xpath('//*[@id="gsft_main"]')
     shadow.chrome_driver.switch_to_frame(frame)
     ```
   - **Extração de Dados da Tabela**:
     - Itera sobre as linhas da tabela, extraindo informações de cada produto:
     ```python
     table = driver.find_element(By.XPATH, '//*[@id="u_tech_products_table"]/tbody')
     rows = table.find_elements(By.TAG_NAME, "tr")
     for item in rows:
         fields = item.find_elements(By.TAG_NAME, "td")
         name = fields[2].get_property("innerText")
         category = fields[3].get_property("innerText")
         cost_price = fields[4].get_property("innerText")
         gtin = fields[5].get_property("innerText")
         id = fields[6].get_property("innerText")
         price = fields[7].get_property("innerText")
         quantity = fields[8].get_property("innerText")
         supplier_code = fields[9].get_property("innerText")
     ```
   - **Registro de Produtos no Maestro**:
     - Cria entradas de log e adiciona novos itens ao DataPool do Maestro:
     ```python
     maestro.new_log_entry(
         activity_label="products-register",
         values={
             "id": id,
             "product_name": name,
             "status": "REGISTERED"
         }
     )
     new_item = DataPoolEntry(
         values={
             "name": name,
             "entry-time": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
         }
     )
     datapool = maestro.get_datapool(label="tech-store-dw")
     datapool.create_entry(new_item)
     ```
   - **Tratamento de Erros**:
     - Captura e registra erros, enviando alertas de aviso ao Maestro:
     ```python
     except Exception as error:
         context = "Could not register product %s because an error occurred " % name
         maestro.alert(
             task_id=execution.task_id,
             title="Warning Alert",
             message="Could not register product.",
             alert_type=AlertType.WARN
         )
         maestro.error(task_id=execution.task_id, exception=context)
         pass
     ```
   - **Envio de Alertas e Finalização**:
     - Envia alertas informativos sobre o sucesso da execução e finaliza a tarefa no Maestro:
     ```python
     maestro.alert(
         task_id=execution.task_id,
         title="Info Alert",
         message="All products Created successfully",
         alert_type=AlertType.INFO
     )
     emails = ["giulia.real@botcity.dev"]
     users = []
     subject = "Automation Finished"
     body = "Hello, your automation was executed successfully"
     maestro.message(emails, users, subject, body, MessageType.TEXT)
     driver.close()
     maestro.finish_task(
         task_id=execution.task_id,
         status=AutomationTaskFinishStatus.SUCCESS,
         message="Automation was executed successfully"
     )
     ```

5. **Execução da Função Principal**:
   - A função `main` é chamada para iniciar o processo:
     ```python
     if __name__ == '__main__':
         main()
     ```

## Conclusão

Este projeto exemplifica como utilizar o BotCity Maestro para gerenciar e monitorar automações, aproveitando funcionalidades como logs, tratamento de erros e alertas. Isso permite um controle mais eficiente e uma melhor visibilidade das execuções automatizadas.
