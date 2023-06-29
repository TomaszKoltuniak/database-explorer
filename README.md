# Database explorer
It's a python flask based web app database explorer made for the EU Mobility Sverige company.

## How to run
1. Clone the repository
```
gh repo clone TomaszKoltuniak/database-explorer
```

2. Install the requirements
```
python3 pip install -r requirements.txt
```

3. Set the environment variables in the .env example file and change it's name to .env
```
Google Cloud Console -> APIs & Services -> Credentials -> OAuth 2.0 Client IDs
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
```
4. Run the main file app.py

5. Open the https://localhost:5000 in your browser

6. Keep in mind that each time you log in using a new account, you will need to manually change their privileges within a database.