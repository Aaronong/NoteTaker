# thepriceisright   

### JP Morgan Chase Project  
Group: ExceptionHandlers  
  
Members: 
* Gabrielle Taylor @gabriellet  
* Jackie Lin @fennilin  
* Leon Song @ls3233  
* Aaron Ong @Aaronong    

### Build Status     
![Travis CI Build Status](https://travis-ci.org/gabriellet/thepriceisright.svg?branch=master)   
See current build information [here](https://travis-ci.org/gabriellet/thepriceisright).

### Usage
First, clone the JPM [Exchange Server](https://github.com/gabriellet/exchange_simulator). While in the `exchange_simulator` directory, run this server from the command line using `python server.py`. Then in a separate terminal, while in the `thepriceisright` directory, run the app using `python manage.py runserver`. After this, start your preferred browser and go to [http://localhost:8000](http://localhost:8000). Enjoy!

### Framework Versions
Python 2.7  
Django 1.10.2  
Bootstrap 3.3.7  

### Testing Dependencies
Six 1.1.0   
Mock 2.0.0   

### Testing
`./manage.py test`
OR if you want to test something specific
`./manage.py test <appname>.tests.TestClass.TestMethod`

### Database Migrations
`python manage.py makemigrations`
`python manage.py migrate`

