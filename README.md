# DailySnaps
DailySnaps is a Django based News website that retrieves news according to user's choice from various sources using endpoints NewsAPI.

## Features
This is a **Django-based website** that displays top news and related news using **NewsAPI**.

1. User preferred news sections
2. Categorical search of news
3. Top news
4. News viewing of various websites
5. Filter by keyword
6. Save user's loved articles.
7. Tokenized Signup with confirmation in console(on local machine) or email.
8. Dark Mode view

## Getting Started
Follow these instructions to get a copy running on your local machine for
development and testing purposes

### Prerequisites.
Anaconda, Python 3.6, git and Virtual Environment (Conda environment of Anaconda preferred)

### Installing

1. Open up Terminal, and go into the directory where you want your local copy,
e.g.
```
cd projects
```

2. Download a copy
```
git clone https://github.com/RITIKHARIANI/DailySnaps.git
```

3. Install a virtual environment
```
conda create --name djangoenv
```

4. Start the environment in the projects folder.
```
conda activate djangoenv
```

5. Install Django and its requirements using pip
```
pip install -r requirements.txt
```

7. Generate a secret key for your django app using
```
python
```
  **then run python and type**
```
from django.utils.crypto import get_random_string
```
  **then**
```
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
```
  **then**
```
get_random_string(50, chars)
```
  **and lastly**
```
quit()
```

8. Copy this result and in your website/website/settings.py file replace
```
SECRET_KEY = os.environ.get('DAILYSNAPS')
```
  **with**
```
SECRET_KEY = 'your newly generated secret key here'
```

9. In the directory that contains 'manage.py' file, run the following to set up the database
```
python manage.py makemigrations news
```

10. When this has completed, run these migrations
```
python manage.py migrate
```

11. Create a user profile to login with
```
python manage.py createsuperuser
```

12. Create an account on newsapi.org and insert its API key in views.py
```
newsapi = NewsApiClient(api_key='API_KEY')
```

13. Once you have followed the instructions to create a user, then run the server
```
python manage.py runserver
```

14. If there were no errors anywhere, you can now go to http://localhost:8000/
in your browser to view a local copy of DailySnaps

### Signup Usage

Once you fill in the details and click Signup button, look inside your terminal/console. There will be a uniquely generated link. Copy paste that onto your broswer's address bar and press enter. You will automatically be redirected to the website with you logged in.

### Future Work

1. Integrate it with Machine Learning Recommendation Systems based on user's saved articles.
2. Make it mobile compatible
3. Include a Share button to Share news among various social network platforms
4. Make Ratings for articles
5. Password Change Option
6. Confirmation through Email

### Major Contributors:
* Aditya Verma: https://github.com/adiver26
* Rahul Raman: https://github.com/Aiden-Python
* Ritik Hariani: https://github.com/RITIKHARIANI
* Romaanchan Skanda: https://github.com/Prix4Houdini

Special Thanks:
* Sourav Tecken: https://github.com/souravtecken
