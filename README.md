# bplmm
BENEFIT PACKAGE LIBRARY MANAGEMENT SYSTEM DOCUMENTATION

#INSTALLATION
**Bold text**Clone the repository

   ```cmd
   git clone https://github.com/Philhealth-Joc/bplmm.git

**Bold text**After cloning, activate your vritaul environment

   ```cmd
   venv\Scripts\activate

**Bold text**Install Dependencies

   ```cmd
   pip install -r requirements.txt

   ```cmd
   npm install
   
**Bold text**Run the migrations and seeders to set up the database schema.

    ```cmd
   python manage.py migrate

   these following command will run the files located in the 'management/commands' directory, these files serve as seeders of the validation rules and codes that are use to simulate the process of adding of codes as part of ICD or RVS rule located in the forms for adding them. 

   ```cmd
   py manage.py claimvalidationinfoseeder
   py manage.py rvscodeseeder
   py manage.py spccodeseeder
 
**Bold text**Create a superuser to access the Django admin interface.

    ```cmd
    python manage.py createsuperuser

Once the superuser has been created, I normally add two user groups in the    Groups table namely 'Encoder' and 'Approver' and set their permisions respectively.

