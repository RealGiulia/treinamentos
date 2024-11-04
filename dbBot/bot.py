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
For CSV Plugin, visit: https://documentation.botcity.dev/plugins/csv/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
from botcity.plugins.csv import BotCSVPlugin

# Import needed libraries
import mysql.connector
import PyPDF2

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
    # SET Csv Plugin:
    # Instantiate the plugin
    bot_csv = BotCSVPlugin()
    # Read from a CSV File
    # Read PDF File:
    file_path =  r'resources\example.pdf'
    reader = PyPDF2.PdfReader(file_path)
    content = reader.pages[0].extract_text()
    print(content)

    # Write pdf content into .txt file
    file_txt = open('example.txt', 'w')
    file_txt.write(content)
    file_txt.close()


    file = open('example.txt', 'r')
    lines = file.readlines()
    
    invoice_number = lines[8].replace("admin@slicedinvoices.comInvoice Number ", '').replace('\n', '')
    invoice_date = lines[10].replace("Invoice Date ", '').replace('\n', '')
    service = lines[19].replace("1.00", '').replace('\n', '')
    order_number = lines[9].replace("Order Number ", '').replace('\n', '')
    order_number = int(order_number)
    hours = 1.00
    total_price = lines[23].replace("Total $", '').replace('\n', '')
    total_price = float(total_price)
    
    # Insert Data from PDF into CSV file
    bot_csv.read('write.csv')
    infos = [invoice_number,invoice_date, service, order_number, hours, total_price]
    bot_csv.add_row(infos)
    bot_csv.write('write.csv')

    # Connect with database
    config = {
            'user': 'root',
            'password': 'admin123',
            'host': 'localhost',
            'database': 'testdb',
            'raise_on_warnings': True
        }
    
    breakpoint()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(buffered=True)

    # Read first 5 lines of table
    query =  "SELECT * FROM dbo_products LIMIT 5;"
    cursor.execute(query)
    result =  cursor.fetchall()
    print(f"The result of query is -->>> {result}")

    # Update item om table
    update_statement = """UPDATE dbo_products
                            SET price = 69.99 
                            WHERE Id = 4;"""
    cursor.execute(update_statement)
    conn.commit()
    
    # Check if item is updated:
    # Retrieving data
    sql = '''SELECT * FROM dbo_products WHERE Id = 4'''
    cursor.execute(sql)
    result = cursor.fetchall()
    print(f"Updated item: {result}")

    # CREATE TABLE Invoices
    create_statement = """CREATE TABLE tb_invoices (
                                                    invoice_number VARCHAR(25),
                                                    order_number INT,
                                                    invoice_date VARCHAR(255),
                                                    service VARCHAR(255),
                                                    hours FLOAT,
                                                    total_price FLOAT
                                                    );"""
    cursor.execute(create_statement)
    
    # Check if table exists:
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)

    # INSERT new row in table invoices
    insert_statement = f"""INSERT INTO tb_invoices (invoice_number,order_number, invoice_date,service, hours, total_price)
                                VALUES ('{invoice_number}',{order_number}, '{invoice_date}','{service}', {hours},{total_price});"""
    print(insert_statement)
    cursor.execute(insert_statement)
    conn.commit()

    #Closing the connection
    conn.close()


if __name__ == '__main__':
    main()
