# bakeli_training
QUIZZ WEBSITE WITH MACHINE LEARNING INTEGRATED

# TAKE ON THE PROJECT
## NB: OS used is WINDOWS 10. Be carefull with some commands if you use and other OS search the equivalent  
1- Install the virtual environment with Python 3.8 
  
2- Activate the virtual environment  
&nbsp;&nbsp;&nbsp;&nbsp;`py -3.8 -m venv name_of_your_venv`  
  
3- Clone the project and go inside the project with cd command  
&nbsp;&nbsp;&nbsp;&nbsp;`git clone url_of_project`  
  
3- Install the packages from requirements file  
&nbsp;&nbsp;&nbsp;&nbsp;`pip install -r requirements`   
  
4- Create a postgreSQL database  
  
5- Modify in settings file the informations to connect to the database according to yours 
  
6- Migrate models  
&nbsp;&nbsp;&nbsp;&nbsp;`py.exe manage.py makemigrations`  
&nbsp;&nbsp;&nbsp;&nbsp;`py.exe manage.py migrate`  
  
7- Run the server  
&nbsp;&nbsp;&nbsp;&nbsp;`py.exe manage.py runserver`    






# This is the development part

Database PostgreSQL is in local and the website also

To take on the project
  Follow the step we have described in the maion part 
  After create your database in pgAdmin 4
  Go to settings, modify the database information
  Make the followings commands  

    py manage.py makemigrations  
    py manage.py migrate  

  After that everything is settle so run the server with the following command and enjoy :)  
    
    py manage.py runserver  


## NB: 
    Make sure you give some data. And your parcours specify the domain and the category.  
    The questions for a category must be filled before you test the website if else you will get some error because there no data.
    

  
