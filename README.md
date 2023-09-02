# Giftly online store

## Our final project for SDA done by

1) Kaarel - KaarelF
2) Erich - Erjokul
3) Demi - ddemip
4) Natalja - nataljj


This is a website for selling fun little gifts to other people. Gifts are sorted into categories, so there is 
something for everyone.

### Main features

* User and admin panels – user can view products by categories and subcategories, admin can add and delete them.

* Functioning weather widget that shows the temperature in Tallinn.

* Bootstrap static files included

* Account creating and updating functionality

* Gift ordering system that accepts payment by card and mobile phone

* Project runs on MySQL

## Running this app

You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
You'll also need to have [MySQL Workbench installed](https://dev.mysql.com/downloads/workbench/).
Both these programs are available on all major operating systems.

#### Clone the repository

In PyCharm click "Get from VCS". In the text box, enter the following address: https://github.com/ddemip/giftly.git
You can also start new project and activate virtual environment. First navigate to chosen folder using cd on windows
and ls on Linux/Mac. Then enter following command.

For Windows:

.\venv\Scripts\activate

For macOS/Linux:

source venv/bin/activate

#### Building the app:

To build the app, run docker compose up --build in Terminal. Default website is http://127.0.0.1:8000

### Applying migrations to add items to database and make it easier to change items there.

To apply migrations enter manage.py migrate in Terminal.

### Stumbling upon bugs on website:

If by chance there are any performance issues or things missing, let us know. We'll try our best to fix them.


