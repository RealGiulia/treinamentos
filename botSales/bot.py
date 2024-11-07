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

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

from gpt_integrator import GPT
import re
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

    bot = WebBot()

    ia = GPT()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.FIREFOX

    # Uncomment to set the WebDriver path
    bot.driver_path = GeckoDriverManager().install()

    # Opens the BotCity website.
    bot.browse("https://intelliauto-dev-ed.develop.lightning.force.com/lightning/o/Case/list?filterName=00Baj00000IIjAuEAL")
    
    # Implement here your logic...
    login =  bot.find_element("#username", By.CSS_SELECTOR)
    login.click()
    bot.paste("giulia@intelliauto.adm")

    pwd = bot.find_element("#password", By.CSS_SELECTOR)
    pwd.click()
    bot.paste("Bl@cksumm3r")

    print("Login Done!")
    # Wait 3 seconds before closing
    bot.wait(3000)

    login_btn = bot.find_element("#Login", By.CSS_SELECTOR)
    login_btn.click()

    bot.wait(8000)

    # List of business units
    business_units = [
        'Engineering and Design',
        'Project Management',
        'Manufacturing and Production',
        'Software Development',
        'Sales and Marketing',
        'Customer Support and Service'
    ]

    

    table = bot.find_element(".slds-table > tbody:nth-child(3)", By.CSS_SELECTOR)
    cases = table.find_elements_by_tag_name("tr")
    for case in cases:
        number = case.find_element_by_tag_name("th").text
        infos = case.find_elements_by_tag_name("td")
        name = infos[2].text
        matter = infos[3].text
        date =infos[6].text
        priority = infos[5].text

        statement = """Based on the matter of this issue tha my client has reported, tell me, shortly and directly, the 
                     Business unit of my company is responsible for that one? """
        title = f"the matter is {matter};"

        business_info = f"The Business Units available are: {business_units};"

        complete_statement =  statement + title + business_info

        response = ia.get_gpt_answer(complete_statement)
        print(response["message"])

        
        pattern = r'\*\*(.*?)\*\*'

        matches = re.findall(pattern, response["message"])
        print(matches)

        #TODO: Integrar com Datapool
        
                

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
