
# MusicStore
STATUS 2024.10.20: 	Note: MS Copilot AI used as assisting development tool in this work.

Final release of MusicStore for TSOHA_2024 P1
1. UI menus navbars implemented and tested
2. Security improvements: Mitigation of SQLi, XXS and RSRF-attacks, input validations and sanity checks, session checks 
3. Use of HTTPS with self signed server certificate.
4. Database designed and improvement done: idexing of important searhes, use of join-table for shopping cart content, populated and tested
5. Two roles of users: customers and store managers. Store manager can test his store by using also a customer account
   (needs to be logged in for customer account also)
6. Dashbords for customer and manager roles
7. Basic listings of database tables implemented in store manager dashboard. Campaign and sales report not use their planned view (in the user story doc).
   iInstead they output the basic productgroup and product listings for UI-testing purposes.
8.Installation and configuration guides for Linux and Windows environment separately done.
9. User Stories document with reporting db-view-scripts done and enclosed as .pdf.
10. gitignore done.
Note: Remember that the system uses self signed certificate, this means that your browser alerts you, just accept to continue with risk, its safe.

Added 2024_10_06: Commit: Customer and Store Manager registrations, logins and logouts, small Customer and Store Manager Dashboards, security improvements: SQLi XXS, CSRF, .env/secret config, input-forms validations, new db tables normalized joinin table for shoppingcart and products, Product table foreig keys reduced essentially.

STATUS 2024.10.06: 	Note: MS Copilot AI used as assisting development tool in this work.
1. Customer and Store Manager registrations logins and logout implemented and tested. Added forms-input validations with regular expressions and input sanitazion (tested functionality).
2. Security improvement: Mitigation of SQLi, XXS and RSRF-attacks (works).
3. Small Customer (tested) and Store Manager (almost fully tested, some known problems) dashboards.
4. More effective database solution: new normalized shoppingcartproduct table, which solves the earlier shopping cart capacity limitation and reduces FK-complexity.
   This speeds up shopping cart and sales functionalities.
5. Used indexin of db-tables, which essentially speeds up the realtime sales functions of the MusiStore.
6. Next: taking under development the realtime sales functions and reporting based on sql-views for the Store Manager Dashboard.

Music Store System Installation and Configuration Guide, v2 for Linux
SEE ATTACHED FORMATTED .PDF VERSION (in app-directory in this MusicStore-repo)
This document should provide a comprehensive guide for setting up the Music Store System on a Linux platform, including detailed steps for installation, configuration, and database setup.  The guide is designed for IT students withbasic   knowledge of Flask, Python, HTML, and databases.

Index:
Introduction
Prerequisites
Installing Python and Flask
Setting Up the Music Store Application
Configuring PostgreSQL Database
Creating and Populating the Database
Running the Application
Directory Structure
User Interface Overview
Using .env Files

1. Introduction
The Music Store System is a web application built using Flask, a web framework for Python.
This guide will walk you through the steps to install and configure the application on a Linux environment.

3. Prerequisites
Before you continue, please, ensure you have the following installed on your system:
Python 3.8 or newer
PostgreSQL
Git for cloning the repository

5. Installing Python and Flask
Install Python:
Open a terminal.
Update the package list:
sudo apt update
Install Python:
sudo apt install python3 python3-venv python3-pip
Install Flask:
Create a virtual environment:
mkdir myproject
cd myproject
python3 -m venv venv
Activate the virtual environment:
source venv/bin/activate
Install Flask:
pip install Flask

6. Setting Up the Music Store Application
Clone the repository:
If you have Git installed, you can clone the repository:
git clone <repository_url>
cd music_store
Install Dependencies:
Ensure your virtual environment is activated and install the required packages:
pip install -r requirements.txt

7. Configuring PostgreSQL Database
Install PostgreSQL:
Download and install PostgreSQL:
sudo apt install postgresql postgresql-contrib
Create a Database:
Switch to the PostgreSQL user:
sudo -i -u postgres
Open the PostgreSQL prompt:
psql
Create a new database:
CREATE DATABASE MStore_v1;
Create the schema:
CREATE SCHEMA mstore_v1;

8. Creating and Populating the Database
Creating Tables:
Within the mstore_v1 schema, create tables for your application:
CREATE TABLE mstore_v1.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE mstore_v1.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

Populating Tables:
Insert initial data into the tables: 
(This is just an EXAMPLE, not the MStore_v1 db)
INSERT INTO mstore_v1.users (username, email, password) VALUES
('john_doe', 'john@example.com', 'securepassword'),
('jane_doe', 'jane@example.com', 'anothersecurepassword');
INSERT INTO mstore_v1.products (name, price, stock) VALUES
('Guitar', 199.99, 10),
('Piano', 499.99, 5);
See db-documents in my MusicStore repo.

7. Running the Application
Starting the Flask Application:
Ensure your virtual environment is activated.
Run the application:
flask run

8. Directory Structure
An overview of the directory structure of the project.
See the GIT MusicStore repo structure.

9. User Interface Overview
Provide an overview of the user interface and its features.
TBD later on...

10. Using .env Files
Benefits of Using .env Files:
Security: .env files help keep sensitive information like database credentials,
API keys, and other configuration details out of your source code
Environment-Specific Configurations: They allow you to easily switch between
different configurations for development, testing, and production environments without changing your code.
Simplified Configuration Management: By centralizing configuration settings
in a single file, .env files make it easier to manage and update configurations.

How to Use .env Files:
Create a .env File: In the root directory of your project, create a file named .env.
Add Environment Variables: Add your environment-specific variables in the format KEY=VALUE. 
For example: ( look also .env file in repo MusicStore)
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/MStore_v1
Load Environment Variables: Use a library like python-dotenv to load these variables into your application. Install it using:
pip install python-dotenv
Then, in your Python  application, load the variables:
from dotenv import load_dotenv
import os
load_dotenv()
database_url = os.getenv('DATABASE_URL')

---END OF INSTALLATION ANS CONFIGURATION GUIDE FOR LINUX---

# MusicStore
Added 2024_09_24: Commit: Mainmenu navbar, new routes and related templates, partly tested also.

MusicStore_v1  2024_09_22 Status report/ Thy / MS Copilot used as an AI-assistant
- user stories done
- database with schema created and populated with testdata set
- MusicStore Flask application fw configured, coded and tested: OK
- some routes controllers and related templates coded, testing is going on,
  but not working routes yet: see module tree
- Music Store System Installation and Configuration Guide, v1 done, see Readme.md
- main navigation menu on the landing page coded, UI-structure and consistent style is designed
- Customer and Store Manager dashboards are coded and are part of this commit
- all the simplier dashboard listings with CRUD-functionality are coded (not part of this commit)
- all the customer related shopping cart reporting and store sales and profitability reports
are coded as sql-views, python controllers and html views, but are not committed in this delivery.

Here is Configuration and installation guide for the testers:
MORE READABLE VERSION IS IN APP-DIRECTORY ABOVE README !

2024.09.22
Music Store System Installation and Configuration Guide, v1

Welcome to the Music Store System installation and configuration guide.
This document will help you set up the Music Store application on Windows 10 or 11.
The guide is designed for IT students with basic knowledge of Flask, Python, HTML, and databases.

Index:
Introduction
Prerequisites
Installing Python and Flask
Setting Up the Music Store Application
Configuring PostgreSQL Database
Creating and Populating the Database
Running the Application
Directory Structure
User Interface Overview

1. Introduction
The Music Store System is a web application built using Flask, a web framework for Python.
This guide will walk you through the steps to install and configure the application on a Windows environment.

2. Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.8 or newer
PostgreSQL
Git for cloning the repository

3. Installing Python and Flask

Install Python:
Download the latest version of Python from the official website.
Run the installer and ensure you check the option to add Python to your system PATH.

Install Flask:
Open Command Prompt-tool in Windows and create a virtual environment:
mkdir myproject
cd myproject
python -m venv venv

Activate the virtual environment:
venv\Scripts\activate

Install Flask:
pip install Flask

4. Setting Up the Music Store Application

If you have Git installed, you can clone the repository:
git clone https://github.com/tihyyti/MusicStore.git
cd music_store (your local repo in your PC)

Install Dependencies:
Ensure your virtual environment is activated and install the required packages:
pip install -r requirements.txt

5. Configuring PostgreSQL Database
Install PostgreSQL:
Download and install PostgreSQL from the official website.
Create a Database:
Open pgAdmin and use the SQL-request tool there to create a new database:
CREATE DATABASE MStore_v1;
Create the schema mstore_v1 with pgAdmin.

Set Up the Database Schema:
Define the search path for non-public schemas:
ALTER DATABASE MStore_v1 SET search_path TO public, mstore_v1;

6. Creating and Populating the Database

Create Tables:
Use the provided SQL scripts in your local repository to create
the necessary tables in the MStore_v1 schema:
With pgAdmin-tool load the db creation script (cloned from GIT)
from your local repository and run it.
Check that 6 tables with columns and primary and foreign keys are created
(from left side menu and under mstore_v1 schema).

Populate with Test Data:

Insert test data (using pgAdmin sql-inquiries) into the tables using the SQL script provided
or a database management tool.

7. Running the Application

Set Up Environment Variables:
Create a .env file in the project root with the following content:
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/MStore_v1

Edit the app/config.py file according to you local PostgreSQL db parameters:
# app/config.py
imports here:
...
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/MStore_v1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = "development"
    FLASK_APP = "app"
    FLASK_DEBUG = True
    SECRET_KEY = "your secret key"

Edit the your PostgreSQL db MStore_v1 password here and
calculate a secret key for your system and edit it in Class Config.
(ask from e.g. MS copilot how to calculate the secret key)

Run the Application with BASH-terminal:
CD ...yourLocalRepo/app/python3 run.py

8. Directory Structure (under construction, not up to date))

music-store/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── home.py
│   │   ├── customer.py
│   │   ├── store_manager.py
|   |
│   └── templates/
│       ├── home.html
│       ├── custodashboard.html
│       ├── manager_dashboard.html
│       ├── customer_shopping_carts.html
│
├── static/
│   ├── css/
│   ├── js/
│
├── .env (optional?)
|---config.py (needed)
├── requirements.txt
├── run.py
└── README.md

9. User Interface Overview

The Music Store application consists of several key components:
Navigation: Provides links to different sections of the application.
Dashboards: Displays key metrics and information for customers and store managers.
Shopping Module: Allows customers to view and manage their shopping carts.

------------------------------------------------------------------------------------

TSOHA 2024_09_08 / Thy / MS Copilot used as an AI-assistant
The final subset of user stories to be implemented for the excercise,
which will be delivered in october-24, should be selected from this document during next phase.

MusicStore-system, User stories, MSus_v1 (Please, see more readable .pdf-version of this, which can be found from this repository also.)

These user stories outline the key functionalities and acceptance criteria for registering and operating stores, store managers, customers, product groups and products in the MusicStore database.

The core concept of MusicStore system is the ShoppingCart-entity.

Story 1: Customer Registration

As a new user, I want to register as a customer,
so that I can create an account and start shopping.

Acceptance Criteria:
The registration form should include fields for custoName, custoPassw, custoEmail, custoPhone, and custoStatus.
The system should validate that custoName, custoPassw are unique.
	- The system should  save custoPssw field in a hashed format.
The system should allow optional fields for custoEmail and custoPhone.
The system should set custoStatus to FALSE by default.
Upon successful registration, custoStatus is set  to TRUE the customer should receive a confirmation message.
The system should set custoBlocked to FALSE by default.

User Story 2: Store Manager Registration

As a store owner, I want to register as a store manager,
so that I can manage my store’s information and customer service operations.

Acceptance Criteria:
The registration form should include fields for storeManagerName, storeManagerPssw, storeName, storeTaxId, storePhone, storeEmail, storeAddress,  and storeLogoUrl.
The system should validate that storeName, storeManagerName,  storeManagerPssw, storeTaxId,  storePhone, storeEmail and storeAddress are entered.
	- The system should  save storeManagerPssw field in a hashed format.
The system should allow optional field for storeLogoUrl.
The system should link the store manager to a Customer record (for making purchases as a customer) using storeManager_id.
Upon successful registration, the store manager should receive a confirmation message.

Here is an example of how a password can be hashed by using the  PostgreSQL’s crypt function:

INSERT INTO Customer (custoName, custoPassw, custoEmail, custoPhone, custoStatus, custoBlocked)
VALUES (
    'Matti Koskela',
    crypt('mypassword', gen_salt('bf')),
    'matti.koskela@outlook.com',
    '040545321',
    TRUE,
    FALSE
);


These user stories outline the key functionalities and acceptance criteria for logging in and out for both customers and store managers in the MusicStore.

User Story 3: Customer Login

As a registered customer, I want to log in to my account,
so that I can access my shopping cart, view my order history,
and manage my account details.

Acceptance Criteria:
The login form should include fields for custoName and custoPassw.
The system should validate the credentials against the stored hashed password.
If the credentials are correct, the customer should be redirected to their account dashboard.
If the credentials are incorrect, an error message should be displayed.
The system should update the last login timestamp upon successful login.

User Story 4: Customer Logout

As a logged-in customer, I want to log out of my account,
so that I can ensure my account is secure when I am not using it.

Acceptance Criteria:
The customer should be able to log out by clicking a “Logout” button.
Upon logging out, the customer should be redirected to the homepage.
The system should invalidate the current session to prevent unauthorized access.

User Story 5: Store Manager Login

As a registered store manager, I want to log in to my store management account, so that I can manage store information, inventory, and customer orders.

Acceptance Criteria:
The login form should include fields for storeManagerName and storeManagerPssw.
The system should validate the credentials against the stored hashed password.
If the credentials are correct, the store manager should be redirected to the store management dashboard.
If the credentials are incorrect, an error message should be displayed.
The system should update the last login timestamp upon successful login.

User Story 6: Store Manager Logout

As a logged-in store manager,
I want to log out of my store management account,
so that I can ensure the store’s information is secure when I am not managing it.

Acceptance Criteria:
The store manager should be able to log out by clicking a “Logout” button.
Upon logging out, the store manager should be redirected to the homepage.
The system should invalidate the current session to prevent unauthorized access.

User Story 7: Customers' shopping cart view on the Customer dashboard

As a registered customer,
I want to list my ShoppingCart headers as a table,
so that I can view my ShoppingCarts categorized by their status and sorted by the most recent dates.

Acceptance Criteria:
The table should display ShoppingCart headers categorized by cartStatus (open, closed, delivered).
Each category should list ShoppingCarts sorted by the most recent dates at the top.
The table should include columns for cartEditedTime, cartPurchasedTime, and cartDeliveryTime.
Clicking on a cart_id in the cartHeader should display the details of the selected ShoppingCart.
The user should be able to close the details view.
This table should be part of the Customer dashboard.

SQL View for the Customer ShoppingCart view on the Customer Dashboard

CREATE VIEW CustomerShoppingCartHeaders AS
SELECT
    sc.id AS cart_id,
    sc.cartCustomer_id AS customer_id,
    sc.cartStatus AS cart_status,
    sc.cartEditedTime AS edited_time,
    sc.cartPurchasedTime AS purchased_time,
    sc.cartDeliveryTime AS delivery_time,
    sc.cartTotal AS total_amount
FROM
    ShoppingCart sc
WHERE
    sc.cartCustomer_id = customer_id, -- the actual user ID
ORDER BY
    sc.cartStatus,
    CASE
        WHEN sc.cartStatus = FALSE THEN sc.cartEditedTime
        WHEN sc.cartStatus = TRUE AND sc.cartDeliveryTime IS NULL THEN       	sc.cartPurchasedTime
        WHEN sc.cartStatus = TRUE AND sc.cartDeliveryTime IS NOT NULL THEN	  	sc.cartDeliveryTime
    END DESC;

Following essential sql-statements and clause are used:
SELECT Statement:
Selects relevant columns from the ShoppingCart table, including cart_id, customer_id, cart_status, current_time, edited_time, purchased_time, delivery_time, and total_amount.

WHERE Clause:
Filters the results to include only the ShoppingCarts of the current user (replace CURRENT_USER_ID with the actual user ID).

ORDER BY Clause:
Orders the results by cartStatus and the respective timestamps in descending order to ensure the most recent dates are at the top.
This view will provide a comprehensive list of ShoppingCart headers for the customer, categorized by their status and sorted by the most recent dates.
