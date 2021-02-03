# oauth
The PHP script is from [here](https://www.oauth.com/oauth2-servers/accessing-data/create-an-application/). 

## Setup
Go to https://github.com/settings/developers, create a new OAuth App, and put your client ID and client secret in an .env file.

Contents of your env file should be:
```
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

Finally, you can run this command from within this directory
```
php -S localhost:8000
```
