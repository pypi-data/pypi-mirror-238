SDK for working with the MTHMR CashBack application.

Functional:

- add customers data
- add transactions data
- read customers data
- read data on accrued cashbacks

Examples of using:

```python
from mthmr import mthmr_query

URL = "issued when connecting to the application"
Token = "issued when connecting to the application"

# Adding Customers:
#   "customer_id" - your internal customer_id

dataCustomers=[
   {
     "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
     "age": 50,
     "gender": "Male",
     "location": "Riyadh"
   },
   {
     "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d2",
     "age": 32,
     "gender": "Female",
     "location": "Riyadh"
   }
]
addCustomers = mthmr_query.add_customers(URL, Token, dataCustomers)

# Reading Customers:

customers = mthmr_query.get_customers(URL, Token)

# Adding Transactions:

# "customer_id" - your internal customer_id
# "transaction_id" - unique transaction ID
# "description" - description of the transaction
# "date" - transaction date GMT
# "merchant_id" - merchant ID,
# "category_id" - category ID,
# "amount" - transaction amount
# "location" - transaction location

dataTransactions=[
  {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac12001",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_id": 123,
    "category_id": 5,
    "amount": 100,
    "location": "Riyadh"
   },
   {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac120003",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_id": 123,
    "category_id": 5,
    "amount": 150,
    "location": "Riyadh"
   }
]
addTransactions = mthmr_query.add_transactions(URL, Token, dataTransactions)

# Receiving CashBack data:

# date_from = "2023-01-01"
# date_to = "2023-02-01"

cashBack = mthmr_query.get_cashbackpayments(URL, Token, date_from, date_to)

```