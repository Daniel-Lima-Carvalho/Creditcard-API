# Creditcard-API
Creditcard API

## How do I get set up?

1 - Pull the project to your local machine and open the terminal in the project root folder.</br>

2 - Create a virtual environment in the project root and activate it.

Linux
        
        apt-get install python3-venv
        
        python3 -m venv venv
        
        source venv/bin/activate

Windows

        python -m venv venv
    
        venv\Scripts\activate
        
3 - Intall python dependencies from requirements.txt.

Linux
        
        pip3 install -r requirements.txt

Windows

        pip install -r requirements.txt
    
4 - Create a secret key with the following command.
        
Linux
        
        python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Windows
        
        python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
        
5 - Create your .env file in root folder with your secret key generated before

        SECRET_KEY={YOUR-SECRET-KEY}

6 - Excute migrations.

Linux

        python3 manage.py migrate

Windows 
        
        python manage.py migrate

7 - Create a superuser.

Linux

        python3 manage.py createsuperuser

Windows       

        python manage.py createsuperuser
        
8 - Run the project.

Linux
        
        python3 manage.py runserver 0.0.0.0:8000
  
Windows
     
        python manage.py runserver 0.0.0.0:8000

9 - Create API Token.

- Enter in the root link
- Login with your created user
- Go to AUTH TOKEN > Tokens > ADD TOKEN
- Choose the user and created your API Token

## How do I use the API?

## 🟢 GET - List creditcards

###### Request Path
```
/api/creditcards/
```
###### Request Headers
`Authorization` Token **{token}**

###### Response Example
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "exp_date": "2023-04-30",
            "holder": "Fulano 1",
            "number": "4593840058437546",
            "cvv": 123,
            "brand": "visa",
            "id": 1
        },
        {
            "exp_date": "2023-04-30",
            "holder": "Fulano 2",
            "number": "4593840058437546",
            "cvv": 123,
            "brand": "visa",
            "id": 2
        }
    ]
}
```

## 🟢 GET - Get single creditcard 

###### Request Path
```
/api/creditcards/1
```
###### Request Headers
`Authorization` Token **{token}**

###### Response Example
```
{
    "exp_date": "2023-04-30",
    "holder": "Fulano",
    "number": "4593840058437546",
    "cvv": 123,
    "brand": "visa",
    "id": 1
}
```

## 🟡 POST - Create creditcard 

###### Request Path
```
/api/creditcards/
```
###### Request Headers
`Authorization` Token **{token}**

###### Request Body Example
```
{
    "exp_date": "04/2023",
    "holder": "Fulano",
    "number": "4593840058437546",
    "cvv": "123"
}
```
###### Response Example
```
{
    "success": true,
    "message": "Creditcard created successfully!"
}
```

## How to run tests?

        python manage.py test
