# AskMate

## Description

This web application is a forum where users can register, log in, ask questions, provide answers, and engage in discussions. It is built using Python with the Flask framework.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To set up the Flask Forum on your local machine, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Jaystar1003/AskMate.git
   cd AskMate

2. Install dependencies using pip:
    pip install -r requirements.txt

3. Set up the database:
    flask db init
    flask db migrate
    flask db upgrade

4. Run the application:
    flask run

The Flask Forum will be accessible at http://localhost:5000 by default.

## Usage

1. Register a new account or log in if you already have one.
2. Explore existing questions and answers.
3. Ask new questions, provide answers, or comment on existing posts.
4. Edit or delete your own questions and answers.
