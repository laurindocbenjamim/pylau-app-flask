@echo off

REM Function to check if the virtual environment is activated
SETLOCAL ENABLEDELAYEDEXPANSION


:: Check if the .env_app directory exists in the current path
IF not exist ".env_app\" (
    echo The .env directory does not exist in the current path.
    echo Creating the .env_app directory...
    ::mkdir .env
    python -m venv .env_app
    
    IF exist ".env_app\" (
        call .env_app\Scripts\activate.bat
        echo The .env_app directory has been created successfully.
        
    ) ELSE (
        echo Failed to create the .env_app directory.
    )
) ELSE (
    echo The .env_app directory already exists in the current path.
)

::call .env\Scripts\activate.bat

set FLASK_ENV=testing

REM Function to install missing packages

:: Open VSCode
call code .
echo _______ Installation has finished.
echo 1. To install the libraries
echo 2. To run the application
echo 3. To install the libraries and run the application
echo 4. To stop the process
set /p resp=": "

IF "%resp%"=="1" (
    REM _______ Installing the application libraries
    echo Installing the libraries...
    python -m pip install --upgrade pip 
    python -m pip install -r requirements.txt
) ELSE IF "%resp%"=="2" (
    REM Running and Debugging the application...
    echo Running the Application...
    python -m flask db init
    python -m flask db stamp
    python -m flask db migrate
    python -m flask db upgrade
    :: python app.py  
    python -m flask run --debug 
) ELSE IF "%resp%"=="3" (
    REM _______ Installing the application libraries
    echo Installing the libraries...
    python -m pip install --upgrade pip 
    python -m pip install -r requirements.txt
    echo Running and Debugging the application...
    python -m flask db init
    python -m flask db stamp
    python -m flask db migrate
    python -m flask db upgrade
    :: python app.py  
    python -m flask run --debug
) ELSE IF "%resp%"=="4" (
    echo Process stopped by the user.
)

ENDLOCAL
