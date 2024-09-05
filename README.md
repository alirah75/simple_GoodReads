## Requirements

- Python 3.9+
- MySQL

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alirah75/simple_GoodReads.git
   cd simple_GoodReads

   
## Create a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install the dependencies:

pip install -r requirements.txt

## Set up the environment variables:

    Create a .env file in the root directory with the following variables:

MYSQL_USER=your_mysql_username

MYSQL_PASSWORD=your_mysql_password

MYSQL_SERVER=localhost

MYSQL_PORT=3306

MYSQL_DB=your_database_name

SECRET_KEY=your_secret_key

## Run migrations:

    Use Alembic to generate and apply the migrations:

alembic upgrade head

## Run the application:

uvicorn main:app --reload
