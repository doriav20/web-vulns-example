@REM Initialize venv
python -m venv venv

@REM Install dependencies
venv\Scripts\activate & pip install -r requirements.txt
