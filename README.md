# Creditcard-API
Creditcard API

## How do I get set up?

1 - Pull the project to your local machine and open the terminal in the project root folder.</br>

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
