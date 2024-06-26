
# BENEFIT PACKAGE LIBRARY MANAGEMENT SYSTEM DOCUMENTATION

## Setting up the Application
Clone the repository

```cmd
git clone https://github.com/Philhealth-Joc/bplmm.git
```

Activate your Virtual Environment

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
py manage.py makemigrations
py manage.py migrate
```

These following command will run the files located in the 'management/commands' directory, these files serve as seeders of the validation rules and codes to the database that are used to simulate the process of adding validation rules and codes as part of ICD or RVS rules found in each form for saving an ICD or RVS

```cmd
py manage.py claimvalidationinfoseeder
py manage.py rvscodeseeder
py manage.py spccodeseeder
```

Create a superuser to access the Django admin interface.
```cmd
python manage.py createsuperuser
```

Once the superuser has been created, it is advisable to add two user groups in the **Groups** table namely **'Encoder'** and **'Approver'**, and set their permissions respectively.

## Add Initial Users
Since the authentication of the application has been set up, pages are only available to authenticated users.
Using the access of the superuser you created, access the admin panel and create 2 users. One user as an **Approver** and another as an **Encoder**.

## Running the Application

To run the application, open a Command Prompt in VS Code.
Navigate to the directory where your virtual environment is located and have it activated.
Navigate back to your project's directory and run the following command.

```cmd
py manage.py runserver
```

Open another Command Prompt in VS Code terminal.
Navigate to the directory where your virtual environment is located and have it activated.
Navigate back to your project's directory and run the following command.

```cmd
npm run dev
```

## Tailwind CSS Installation
Run the following command the install Tailwind CSS as a dev dependency using NPM:

```cmd
npm install -D tailwindcss
```

Create a tailwind.config.js file:

```cmd
npx tailwindcss init
```

Configure the template paths using the content value inside the Tailwind configuration file:

```cmd
module.exports = {
  content: [
      './templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Import the Tailwind CSS directives inside the input.css file:

```cmd
/* static/src/input.css */

@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Flowbite Installation

Install Flowbite as a dependency using NPM:

```cmd
npm install flowbite
```

Require Flowbite as a plugin inside the tailwind.config.js file:

```cmd
module.exports = {

    plugins: [
        require('flowbite/plugin')
    ]

}
```

Include Flowbite inside the content value of the tailwind.config.js file:

```cmd
module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

# HTMX Installation

Install django-htmx using pip

```cmd
pip install django-htmx
```

Add 'django_htmx' to your INSTALLED_APPS in your settings.py file:

```cmd
INSTALLED_APPS = [
    ...
    'django_htmx',
]
```

Add the HTMXMiddleware to your MIDDLEWARE in settings.py:

```cmd
MIDDLEWARE = [
    ...
    'django_htmx.middleware.HtmxMiddleware',
]
```

Create a **htmx.min.js** file inside **static/js/** directory
download the **htmx.min.js** code from this website https://unpkg.com/browse/htmx.org@1.9.12/dist/htmx.min.js
Paste the code to the js file you created then add the following script at the bottom of your layout template.
```cmd
<script src="{% static 'js/htmx.min.js' %}" defer></script>
```


## Files and Folder Structure
As this was an exploratory Django project, I tried to apply the repository pattern in the codebase which basically separates each concern. From handling HTTP requests to handling logic and data preparations to the actual database operations. For this application, a Service and Repository layered approach was used. **Please note that this might not be the actual/proper way of implementing this pattern/approach in Django.**

### Views/Controller
Aside from the **views.py** file in the app, there is a **model_views** folder which contains other folders namely: **acr, drg, z_benefits**, the **acr** folder then contains the model-specific views file for the models **ACR_GROUPS** => **group_view.py**, **ACR_GROUPS_ICDS** => **icd_view.py**, **ACR_GROUPS_RVS** => **rvs_view.py**, these files then handles every HTTP request that is concerned specifically to a model.

### Services
Handling of HTTP requests was separated from some of the business logic and the preparation of data to be saved in the database. Service classes are located in the **Services** folder. The files located in the folder are the following **group_service.py**, **icd_service.py**, **rvs_service.py**, and the **auth_Service.py** for the authentication. Defined in the service classes is the way how the data are prepared and some of the logic and validations needed to save them in the  database.

A service class has a constructor that accepts an instance of the repository class of a related model, in this case, the service class for the model **ACR_GROUPS_RVS** accepts an instance of a repository class which will be the instance of this class **ACR_GROUPS_REPOSITORY**
```cmd
class ACR_GROUPS_RVS_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository  
```

This is how the service class is instantiated in the view file of a **ACR_GROUPS_RVS** model.
```cmd
GROUPS_SERVICE = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
```

Using **GROUPS_SERVICE**, you can easily call a function from the service class to a view file.

```cmd
 GROUPS_SERVICE.create_temp(data, request)
```

The functions from the repository class can then be accessed through the **repository** which is the instance of the repository class passed in as a parameter of the service class constructor in the view file.

```cmd
return self.repository.create_main(self.to_icd_array(data, group_id))
```


### Repositories
The actual database operations are also separated through repository classes which are located in each model-specific repository file. There is nothing really complicated about it, for now, each model-specific repository class just includes functions that invoke the **save()** method in order to save an object to the database. The **save()** method is used for both adding and editing an object in the database. 
Separating the logics and functions that actually touches the database is somehow a good practice, especially for large-scale applications. This prevents unnecessary code revisions whenever there is a need to change a database or a database operation within the application. This also promotes the reusability of methods that execute database queries. Overall it promotes single responsibility and separation of concern thus making the application easier to test. 

Sample repository class, from **ACR_GROUPS_REPOSITORY**
```cmd
class ACR_GROUPS_REPOSITORY:
    def create_main(self, data):
        acr_groups = ACR_GROUPS(**data)
        acr_groups.save()
        return acr_groups

    def create_temp(self, data):
        acr_groups_temp = ACR_GROUPS_TEMP(**data)
        acr_groups_temp.save()
        return acr_groups_temp
```

## Decorators
There are custom decorators made for this app, **approver_required** and **encoder_required**, the functions for this decorators are found in the **decorators.py** file.

**@encoder_required**
```cmd
def encoder_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Encoder').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
```

**@approver_required**
```cmd
def approver_required(function):
    @login_required
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Approver').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
```

## Some Things Worth Noting:

1. Avoid adding raw CSS styles in the **style.css** file as it changes each time that resources get watched and compiled through **npm run dev**. Instead, you can add your CSS styles in the **input.css** file.
2. Some of the view functions does not have custom decorator tags yet especially the newly created ones in the **icd_view.py**.
3. Some of the background images, and colors used in the HTML templates as custom tailwind classes are found in the **tailwind.config.js** file

```cmd
  theme: {
    extend: {
      backgroundImage: {
        'image': "url('/static/images/image.png')",
        'logo': "url('/static/images/images_Philhealth_Logo.png')",
        'loginBg': "url('/static/images/images_Philhealth_Logo.png')",
        'bgImage': "url('/static/images/philhealth-bg.png')",
        'miniBg' : "url('/static/images/miniBG.jpg')",
      },

      width:{
        '85': '85%'
      },

      zIndex: {
        '100': '100',
      }
    },

    colors: {
      'themeColor': '#156913',
      'primary': '#43B02A',
    }
  },
  plugins: [
    require('flowbite/plugin'),
  ],
```
4. It is better to put all the functions that touch the database in the repository class such as getting and filtering objects which I failed to do so.
5. Some of the HTML templates were not properly organized and do not have uniform naming patterns.
6. The **main2.html** is a layout template inside the **layouts** folder is for testing purposes only.

