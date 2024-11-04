"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from webdriver_manager.firefox import GeckoDriverManager
from botcity.plugins.googlesheets import BotGoogleSheetsPlugin
# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    credenciais = "resources\\credentials.json"
    bot_planilha = BotGoogleSheetsPlugin(credenciais, "1lCU5rEhTJ7Pl6nVNSbXJTfI0BU2Ry6Ss3tG4ZcNqS_c")

    bot_planilha.add_row(["NOME MOEDA", "VALOR EM R$"])

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.FIREFOX

    # Uncomment to set the WebDriver path
    bot.driver_path = GeckoDriverManager().install()

    # Opens the BotCity website.
    bot.browse("https://www.google.com/")

    # Implement here your logic...
    bot.wait(2000)
    try:
        barra_pesquisa = bot.find_element("#APjFqb", By.CSS_SELECTOR)
        barra_pesquisa.click()
    except Exception as error:
        maestro.error(task_id=execution.task_id, exception=error)

    bot.paste("cotação Dólar em real")
    bot.enter()

    bot.wait(1000)

    valor_moeda = bot.find_element(".SwHCTb", By.CSS_SELECTOR)
    print(f" A cotação do dólar em real é de ->> R${valor_moeda.text}")

    bot_planilha.add_row(["Dólar", f"R${valor_moeda.text}"])
    maestro.new_log_entry(
            activity_label="bot-cotacao",
            values={
                "moeda": "Dólar",
                "valor": f"R${valor_moeda.text}"
            }
        )
    
    moedas = ["Euro", "Libra esterlina", "Yên japonês"]

    for moeda in moedas:

        limpador = bot.find_element(".ExCKkf", By.CSS_SELECTOR)
        limpador.click()
        bot.wait(500)
        bot.paste(f"Cotação {moeda} em real")
        bot.enter()

        bot.wait(1000)

        valor_moeda = bot.find_element(".SwHCTb", By.CSS_SELECTOR)
        print(f" A cotação do dólar em real é de ->> R${valor_moeda.text}")
        bot_planilha.add_row([f"{moeda}", f"R${valor_moeda.text}"])

        maestro.new_log_entry(
            activity_label="bot-cotacao",
            values={
                "moeda": moeda,
                "valor": f"R${valor_moeda.text}"
            }
        )

        new_item = DataPoolEntry(
        values={
            "moeda": moeda,
            "valor": f"R${valor_moeda.text}"
        }
        )

        # Obtendo a referência do Datapool
        datapool = maestro.get_datapool(label="moedas")

        # Adicionando um novo item
        datapool.create_entry(new_item)


    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    maestro.alert(
        task_id=execution.task_id,
        title="Automação finalizada",
        message="Automação finalizada com sucesso",
        alert_type=AlertType.INFO
    )

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
