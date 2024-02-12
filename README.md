# Dshop developed by PyMasters

## Rules of engagement
Good reading on working with code changes and pull request is https://google.github.io/eng-practices/. It contains both views - change author and reviewer.

### Rules

1. Do not commit directly to `master` or `dev`. Both branches are protected.
2. Use pull request to add your work. Make pull request to `dev` branch.
   - After creating pull request use "reviewers" option on far right of the screen to request review from "akademiait/dshop" team, or you can request review from certain team member directly by mentioning their name.
      ![image](https://github.com/akademiait/Dshop/assets/989256/a5886335-b537-4a23-8655-1bcaba5c67ae)
   - One of the team members (or multiple) will perform code review and approve the pull request or requst changes.
   - If changes are requested, all comments have to be in constructive and friendly manner, as shown in https://google.github.io/eng-practices/review/reviewer/comments.html
   - It's a good thing to comment on the good parts of code with "Nice work" or something similar.
4. As this is a learning project, pair programming is most welcome. Jump on Zoom or google meet and work together: https://www.youtube.com/watch?v=wu6BOT-eMgc&t=105s&ab_channel=devmentor.pl
5. Code quality and automated tests will be run and required to pass before pull request can be merged. 
6. At least one approval by other team member is required before pull request can be merged.
7. After pull request is approved and code quality + tests are passed, pull request is merged by the author.
8. It is author responsibility to watch over pull request, bump if there is no code review done, fix issues and merge pull request.

#### How to Set up

Clone repository to specific folder (ex. Dshop):
```
git clone https://github.com/akademiait/Dshop.git
```
You need to have installed Poetry package. If you don't have, please install using this command:
```
pip install poetry
```
Navigate to Dshop folder by command:
```
cd Dshop
```
Set poetry global option, to use project folder as place to hold Virtual environment (recommended):
```
poetry config virtualenvs.in-project true
```
Install virtual environment, using current dependencies:
```
poetry install
```
Copy file env-template to .env file using command:
```
# linux/mac
cp env-template .env

# windows
copy env-template .env
```
Start poetry virtual environment
```
poetry shell
```

Update local .env file as needed

Create admin account to access admin site:

```
# linux/mac
# to apply db changes
./manage.py migrate 
./manage.py createsuperuser

# windows
# to apply db changes
python manage.py migrate
python manage.py createsuperuser
```


Run project:
```
# linux/mac
# to apply db changes
./manage.py migrate 
# to start project
./manage.py runserver

# windows
# to apply db changes
python manage.py migrate
# to start project
python manage.py runserver
```

Load data from fixtures:
```
python manage.py loaddata fixtures_products.json
```

Open web browser and navigate to localhost address:  http://127.0.0.1:8000/ 

---
#### Payment system integration
Stripe was used to implement the payment system.

Steps according to which the implementation was performed:
https://testdriven.io/blog/django-stripe-tutorial/

**To create an account at Stripe, follow the instructions below:**
1. Register for a Stripe account: https://dashboard.stripe.com/register
2. Navigate to the Dashboard.Ensure that the account is in the Test mode. 
3. Click on "Developers"
4. Click on "API keys"
5. Copy API keys to .env file:

   `STRIPE_PUBLISHABLE_KEY = '<your test publishable key here>'`

   `STRIPE_SECRET_KEY = '<your test secret key here>'`
6. Specify an "Account name" within your "Account settings" at https://dashboard.stripe.com/settings/account 
7. Create a product (Click "Products" and then "Add Product")
8. Add a product name, enter a price, and select "One time"
9. Click "Save product"
10. For testing purposes you can use the cards listed at this link https://stripe.com/docs/testing#cards

---

### In case of problems with starting the project:
1. Check the env-template file and update the local .env file if necessary
2. Run `poetry install`
