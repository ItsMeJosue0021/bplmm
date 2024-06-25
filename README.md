
# BENEFIT PACKAGE LIBRARY MANAGEMENT SYSTEM DOCUMENTATION

## INSTALLATION
Clone the repository

```cmd
git clone https://github.com/Philhealth-Joc/bplmm.git
```

Install Dependencies

```cmd
venv\Scripts\activate
```

Install Dependencies

```cmd
pip install -r requirements.txt
```

Install npm
```cmd
npm install
```

Run the migrations and seeders to set up the database schema.

```cmd
python manage.py migrate
```

These following command will run the files located in the 'management/commands' directory, these files serve as seeders of the validation rules and codes that are use to simulate the process of adding of codes as part of ICD or RVS rule located in the forms for adding them. 

```cmd
py manage.py claimvalidationinfoseeder
py manage.py rvscodeseeder
py manage.py spccodeseeder
```

Create a superuser to access the Django admin interface.

```cmd
python manage.py createsuperuser
```

Once the superuser has been created, I normally add two user groups in the    Groups table namely 'Encoder' and 'Approver' and set their permisions respectively.

