# flask_training_app
### Bank management system

This API demonstrates the basic CRUD operations for a banking customer.

Operations supported by API are:
1. Register customer account
2. Customer Login
3. Get customer account details
4. Update/Delete customer details
5. Add Loan
6. Get Loan details
7. Delete Loan Details

Requirements:

    Python 3.9
    MongoDB Community Server 4.4.1

After getting the latest code from github repository, you can install the python package dependencies using:

    pip install -r requirements.txt

Payload -- Add Customer

{
    "username": "johndoe",
    "password": "Blue123",
    "name": "John Doe",
    "accountType": "savings",
    "address": "1 Main Street",
    "state": "Test",
    "pan": "aaaaa5678a",
    "contactNo": "1234567890",
    "dob": "10-18-2020",
    "country": "India",
    "emailAddress": "test@tt.co"
}

Payload -- Update Customer

{
    "username": "johndoe123",
    "contactNo": "1234567890",
    "accountNumber": 1003,
    "dob": "10-14-2020",
    "password": "Blue123"

}

Payload -- Loan 

{
"username": "test",
"loanType": "Personal",
"loanAmount": 100000, 
"Date": "11.11.2020",
"interestRate": 10.5,
"duration": 3  
  }
