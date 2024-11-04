# Import for the Desktop Bot
from botcity.core import DesktopBot

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

    bot = DesktopBot()    # bot.browse("http://www.botcity.dev")

    # Implement here your logic...
    bot.wait(10000) # todo check/activate window
    
    # Opens Products Tab
    if not bot.find( "newProducts", matching=0.97, waiting_time=10000):
        not_found("newProducts")
    bot.click()
        
    
    # Activates Item Number text box
    if not bot.find( "itemNumber", matching=0.97, waiting_time=10000):
        not_found("itemNumber")
    bot.click_relative(131, 13)
    
    
    # Input Item number
    bot.paste("123456")
    bot.tab()

    # Inputs Name
    bot.paste("Keyboard")
    bot.tab()

    # Inputs Category
    bot.paste("Computer accessories")
    bot.tab()

    # Inputs GTIN
    bot.paste("555874")
    bot.tab()

    # Inputs Code
    bot.paste("B7899Z1")
    bot.tab()

    # Description with delay between each keystroke in ms.
    bot.kb_type("Backpack made with sintetical material", 100)
    bot.tab()

    # Inputs Price
    bot.control_a()
    bot.paste("199.99")
    bot.tab()

    # Inputs Cost Price
    bot.control_a()
    bot.paste("80.00")
    bot.tab()

    # Saves current item
    if not bot.find( "Save", matching=0.97, waiting_time=10000):
        not_found("Save")
    bot.click_relative(147, 77)
    
    
    # Close tab to start registering new products
    bot.control_w()


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

