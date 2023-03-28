# Inventory-Manager-Bot
A repository containing code for inventory manager robot that validates item placement and availability.

# How It Works:
The main app that users interface with is the Label Generator Interface. Before making labels, it requires the user to login to the database used for inventory management and the folder destination to store generated labels. Afterwards, the user must fill in all the necessary parameters and generate a label, which is recorded into the database.

## Boot Up:
The follow GUI is the main application that users will use:

![main_app](https://user-images.githubusercontent.com/42896783/228388579-3289c95d-ee44-488a-9f78-157df9b58431.png)

## Connecting to SQL Database:
The user will have to press the menu button on the top-left and connect to the database. This will open another GUI window where the user can login to the PostgreSQL database. Once connected, at any point when the user generates labels, it will be recorded into the database.

![menu](https://user-images.githubusercontent.com/42896783/228389254-e6779866-cbb2-4ae2-961d-3b291afe0c62.png)

![database_login](https://user-images.githubusercontent.com/42896783/228389055-333ea623-ca83-4288-a700-8d35e6f88f64.png)

## Generating a Label:

Now the user can fill in the parameters in the main app. The user must fill in all parameters before a label is generated. They must also define the folder destination to send the generated label. After pressing the "Generate Label" button on the bottom-right, it will show a preview of the label. As well as sending the record of the information to the SQL database. In the folder destination, the user can print out the label and attach it to the package.

![label](https://user-images.githubusercontent.com/42896783/228389854-5054c6e2-b722-42d4-a985-70b38787e149.png)

## Checking Out:
The user will have to press the menu button on the top-left and run the checkout app. This will open another GUI window where the user can connect to a camera. Once connected, the user can create a snapshot with the label in view to decode the QR code. This will get the product number and will send a query to the database for the estimated checkout date. Once the user confirms the product number, they can check out the product number and this will update the database with the timestamp.

![checkout](https://user-images.githubusercontent.com/42896783/228390579-9cc735c2-9df0-47e9-b0fe-13a2c20c5849.PNG)
