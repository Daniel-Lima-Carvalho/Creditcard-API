# Creditcard-API
Creditcard API

## 🟢 GET - List all creditcards

###### Request Path
```
/api/creditcards/
```
###### Request Headers
`Authorization` Token **{token}**

###### Response Example
```
{
    "count": 4,
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
