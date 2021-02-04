# oauth
The PHP script is from [here](https://www.oauth.com/oauth2-servers/accessing-data/create-an-application/). 

## General Setup
Go to https://github.com/settings/developers, create a new OAuth App, and put your client ID and client secret in an .env file.

Contents of your env file should be:
```
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

## Setup for PHP app
Run the index.php file
```
php -S localhost:8000
```

## Setup for Python app
Install pip requirements
```
pip3 install -r requirements.txt
```

Run the index.py file
```
python3 index.py 
```

## Final step
View http://localhost:8000/ in your browser!
