![Logo](https://github.com/kashsuks/Sustaina/blob/7fa904ba090a71971992ffeff5a298209fba2248/logo.png)
 
# Sustaina
 
A desktop app that aims to combat unsustainable clothing purchases
 
## Purpose
 
The purpose of this project is to make users more aware of sustainable clothing and make them accountable for their actions. In turn, they will be more responsible and consider where their clothing is sourced from.
 
## Features
 
- Mobile device like interface
    - Built using python3 but to replicate an Iphone experiece
- Cross device access
    - By using a database, multiple users are able to contribute
- Uploading and searching for clothes
- A chrome extension that also shows whether  a piece of clothing is sustainable or not
 
 
## License
 
This project uses the [MIT](https://choosealicense.com/licenses/mit/) license
 
 
## Environment Variables
 
To run this project, you will need to add the following environment variable to your .env file
 
`DATABASE_URL`
 
This Database URL is the external URL under your online deployement
 
**To use the shared/universal URL, please contact email: ksukshavasi@gmail.com with the Subject: Sustaina DB URL**

## Requirements
- **Python 3.8+**
- **Pip package manager**
- **Web Browser**

## Run Locally (For the Client Sided App)
 
1)  Clone the project
 
```bash
git clone https://kashsuks/sustaina
```
 
2) Go to the project directory
 
```bash
cd sustaina
```
 
3) Install dependencies
 
```bash
pip3 install -r requirements.txt
```
 
4) Run the file
 
```bash
python3 main.py
```
 
## Run Locally (For the Chrome Extension)
 
1) Clone the project
 
```bash
git clone https://kashsuks/sustaina
```
2) Go to Chrome (or any [Chromium](https://www.chromium.org/Home/) based browser)
 
3) Enable developer mode in the settings
 
4) Load Unpacked
 
5) Choose the `/chrome-extension` sub-directory
 
## Authors
 
- [@kashuks](https://www.github.com/kashsuks)
 
 
## Tech Stack
 
**Client:** Python3, Tkinter, Psycopg2
 
**Database:** PostgreSQL hosted on [Render](https://render.com/)
 
**Chrome Extension:** HTML, CSS, and Javascript
 
## Known Bugs / Errors
 
- The Database URL is being called from local storage.
    - For example, if you change the Database URL in the `.env` file, it still uses the old one
    - **The fix**
        - Use `unset DATABASE_URL` in the terminal in the same directory and the root of the project

- The Database is a free 30 day instance of Render DB running PostrgeSQL meaning, after 1 month, the DB will expire
    - **The Fix**
        - Get a new instance of your database from [Render](https://render.com/) and use its `External Database URL`