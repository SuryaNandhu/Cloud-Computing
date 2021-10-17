**Prerequisites**<br />
Install Flask using ```pip install Flask``` <br />
Pull the latest dynamodb-local using ```docker pull amazon/dynamodb-local```

**Working steps**<br />
Clone the repository <br />
Run the ```docker run -p 8000:8000 amazon/dynamodb-local``` command <br />
Open another command prompt, move to the project directory and run the ```python flask_start.py``` command <br />
Open ```http://localhost:5000/form``` in your browser
