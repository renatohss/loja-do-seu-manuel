# Loja do Seu Manuel / Mr Manuel's Shop
This API simulates a retail store system, with products, stocks and orders management.

## How to use it
- Create a Virtual Environment for Python dependencies and activate it
- Run ```pip install -r requirements.txt``` to install all dependencies needed
- Export Flask app using the command:
```export FLASK_APP='app.py'```
- Run Flask app using the command: 
```flask run```
- App will run on **localhost**, port **5000**

## Resources
### Add new object (product or order)
**Endpoint:** /new/?type=<orders or products>
**Method:** POST
**Request body:** JSON
**Request format:**
*Type orders:*
```
{
  "id": 4, // Order id code as int
  "date": "24/02/2019", // Date of the order creation
  "client": "Renato Silva", // Customer's name
  "status": "Novo", // Order status
  "shipping": 11.99, // Shipping Value
  "items": [ // Array with the items bought in this order
    {
      "id": 5, // Product Id
      "qty": 3, // Quantity bought
      "unit_price": 0, // Product's unit price - Set to zero as the system will look up for the item's price during the process
      "total_price": 0 // Total price of this product in this order - Set to zero as the system will calculate it
    },
    {
      "id": 3,
      "qty": 7,
      "unit_price": 0,
      "total_price": 0
    },
    {
        ...
    }
  ],
  "total_price": 0 // Total price of the whole order - Set to zero as the system will calculate it 
}
``` 

*Type products:*
```
{
	"id": 4, \\ Product Id
	"name": "Produto 4", \\ Product name
	"description": "Descrição do produto 4", \\ Product description
	"price": 99.99, \\ Product price
	"stock": 30, \\ Units in stock
	"details": ["semi-novo", "garantia estendida", "importado"] \\ Array with details from the product
}
```

### Retrieve an existing product or order
**Endpoint:** /get/?type=<orders or products>&id=<order or product id>
**Method:** GET
**Request Type:** JSON
**Request format:**