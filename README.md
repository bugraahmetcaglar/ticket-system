# WATER WORKS TROUBLE TICKET MANAGEMENT SYSTEM
Application prepared for users to create faults and for administrators to monitor and fix these faults.


#Before Launch Project

**Download Postgresql : https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1257371**
<br>You dont need to install stackbuilder.

**You will be automatically connected to the database. Do not change any connection settings.**


**CREATE SUPER USER**
<br>Before launch the project:
<br>Write these commands on terminal: <br>`cd wvenv/Scripts` then, <br>`activate.bat`

Return main folder which has manage.py file:


`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser` you have to create a super user with this command. After all of these:

**Run Project**
<br>`python manage.py runserver`
