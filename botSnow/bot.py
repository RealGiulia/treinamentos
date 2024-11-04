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

import time
# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from pyshadow.main import Shadow
# Disable errors if we are not connected to Maestro

from selenium import webdriver
from pyshadow.main import Shadow
from datetime import datetime
BotMaestroSDK.RAISE_NOT_CONNECTED = False

from webdriver_manager.chrome import ChromeDriverManager


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()

    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()
    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")
    print("Starting execution...")

    # Set driver configuration
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    shadow = Shadow(driver)

    # Open page and insert credentials
    shadow.driver.get("https://dev258555.service-now.com/now/nav/ui/classic/params/target/u_tech_products_list.do")
    time.sleep(5)

    name_input = driver.find_element(By.ID, "user_name")
    name_input.send_keys("admin")
    pwd_input = driver.find_element(By.ID, "user_password")
    pwd_input.send_keys("iYy=FO3x1dN=")
    time.sleep(2)
    login_btn =driver.find_element(By.ID, "sysverb_login")
    login_btn.click()
    time.sleep(5)

    # Handle Shadow DOM elements and Iframe
    frame = shadow.find_element_by_xpath('//*[@id="gsft_main"]')
    shadow.chrome_driver.switch_to_frame(frame)

    # Getting table elements
    table = driver.find_element(By.XPATH,'//*[@id="u_tech_products_table"]/tbody')
    rows = table.find_elements(By.TAG_NAME, "tr")
    for item in rows:
        try:
            fields = item.find_elements(By.TAG_NAME, "td")
            name = fields[2].get_property("innerText")
            category = fields[3].get_property("innerText")    
            cost_price = fields[4].get_property("innerText")
            gtin = fields[5].get_property("innerText")
            id = fields[6].get_property("innerText")
            price = fields[7].get_property("innerText")
            quantity = fields[8].get_property("innerText")
            supplier_code = fields[9].get_property("innerText")

            print("Insert log entry for product... ")
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

            # Getting the Datapool reference
            datapool = maestro.get_datapool(label="tech-store-dw")

            # Adding a new item
            datapool.create_entry(new_item)

            print("Sending products info for Datapool")
            new_item = DataPoolEntry(
                values={
                    "name": name,
                    "price": price,
                    "amount": quantity,
                    "cost_price": cost_price,
                    "gtin": gtin,
                    "supplier_code": supplier_code,
                    "id": id,
                    "Category": category
                }
            )

            # Getting the Datapool reference
            datapool = maestro.get_datapool(label="tech-store")
            # Adding a new item
            datapool.create_entry(new_item)

        except Exception as error:
            context =  "Could not registem product %s because an error occured " % name
            maestro.alert(
            task_id=execution.task_id,
            title="Warning Alert",
            message="Could not register product.",
            alert_type=AlertType.WARN
            )

            # Registering error on maestro
            maestro.error(task_id=execution.task_id, exception=context)
            pass

        print("Sending alerts of all products registered on maestro")
        maestro.alert(
            task_id=execution.task_id,
            title="Info Alert",
            message="All products Created successfully",
            alert_type=AlertType.INFO
            )
            

    # Flagging execution as finished
    print("Finishing execution")

    # List of emails, if not using, pass an empty list
    emails = ["giulia.real@botcity.dev"]
    # List of usernames, if not using, pass an empty list
    users = []

    subject = "Automation Finished"
    body = "Hello, your automation was executed successfully"

    maestro.message(emails, users, subject, body, MessageType.TEXT)
    driver.close()
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Automation was executed successfully")


if __name__ == '__main__':
    main()
