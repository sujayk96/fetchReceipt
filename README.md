# fetchReceipt
# Flask REST API Application


## Overview

Briefly describe what your Flask REST API application does and its main features.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

###Installation method 1: Docker install
If you would like to run the code directly using docker you can follow the below steps.

1. Clone the repo
```bash
git clone https://github.com/sujayk96/fetchReceipt.git
```
2. Build the docker image
```bash
docker build -t <my-image> .
```
use any name for the image
3. Run the docker container
```bash
docker run -p 4000:8000 <my-image>
```
4. Access the API
You can typically access it through a web browser by navigating to http://localhost:4000, where 4000 is the host port mapped in the docker run command.

5. Check out the APIs <br>


###Installation method 2: Plain install
If you would like to run the code with out docker.
1. Clone the repo
```bash
git clone https://github.com/sujayk96/fetchReceipt.git
```

2. Install pipenv if you don't have it installed
```bash
pip install pipenv
```

3. Create virtual env
```bash
pipenv shell
```

4. Install dependancies
```bash
pipenv install
```

5. Run Flask application
```bash
python receipt.py
```

6. Checkout the APIs.

Path1: Path: /receipts/process <br>
Method: POST <br>
Payload: Receipt JSON <br>
Response: JSON containing an id for the receipt.<br><br>
Path2: /receipts/{id}/points<br>
Method: GET<br>
Response: A JSON object containing the number of points awarded.<br>