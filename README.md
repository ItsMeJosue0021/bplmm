
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

These following command will run the files located in the 'management/commands' directory, these files serve as seeders of the validation rules and codes to the database that are used to simulate the process of adding validation rules and codes as part of ICD or RVS rules located in each form for saving an ICD or RVS

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

## RUNNING THE APPLICATION

To run the application, open a Command Prompt in VS Code
Navigate to the directory where your virtual environment is located and have it activated
Navigate back to you project's directory and run the following command

```cmd
py manage.py runserver
```

Open another Commant Prompt in VS Code terminal
Navigate to the directory where your virtual environment is located and have it activated
Navigate back to you project's directory and run the following command

```cmd
npm run dev
```

## FILE AND FOLDER STRUCTURE

### Views
Aside from the **views.py** file in the app, there is a **model_views** folder which contains another folders namely: **acr, drg, z_benefits**, the **acr** folder then contains the model specific views file for the models **ACR_GROUPS** => **group_view.py**, **ACR_GROUPS_ICDS** => **icd_view.py**, **ACR_GROUPS_RVS** => **rvs_view.py**, these files then handles every HTTP request that are concerned specifically to a model.

### Services
Handling of HTTP request were separated from some of the business logic and the preparation of data to be saved in the database. Service classes are located in the **Services** folder. The files located in the folder are the following **group_service.py**, **icd_service.py**, **rvs_service.py** and the **auth_Service.py** for the authentication. Defined in the service classes are the way how the data are prepared and some of the logic needed to save them in the  database.

A service class has a constructor that accepts an instance of the repository class of a related model, in this case the service class for the model **ACR_GROUPS_RVS** accepts an instance of a repository class which will the instanc eof this class **ACR_GROUPS_REPOSITORY**
```cmd
class ACR_GROUPS_RVS_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository  
```

This how the service class is instanciated in the view file of a **ACR_GROUPS_RVS** model.
```cmd
GROUPS_SERVICE = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
```

Using **GROUPS_SERVICE**, you can easily call a function from the service class to view file.

```bash
 GROUPS_SERVICE.create_temp(data, request)
```


### Repositories
The actual database operations are also separated through repository classes which is located in each model specific repository file. There is nothing really complicated about it, repository classes just includes functions that invoke the **save()** method in order to save an object to the database.

