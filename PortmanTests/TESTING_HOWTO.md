# This is a README file for Portman Agent tests

## Setting up the local database for testing (PostgreSQL):
### 1. Install PostgreSQL on your local machine.
### 2. Install DBreaver or some other db management tool.  
### 3. Create a **new user** with the name "portman" and a password of your own preference.
- You can use the following command to create a new role "portman" with a password "portman":
  ```postgresql
    CREATE ROLE portman WITH LOGIN PASSWORD 'portman';
  ```
### 4. Create a **new database** with the name "portman".
- You can use the following command to create a new database:
  ```postgresql
  CREATE DATABASE portman;
  ```
### 5. Grant all privileges to the user "portman" on the database "portman".
- You can use the following command to grant all privileges to the user "portman":
  ```postgresql
  GRANT ALL PRIVILEGES ON DATABASE portman TO portman;
  ```
### 6. Create two new table with the names "voyages" & "arrivals" in the database "portman".
- You can use the following commands to create a new table once you've connected to the database "portman":
  ```postgresql
  CREATE TABLE IF NOT EXISTS voyages (
    portCallId INTEGER PRIMARY KEY,
    imoLloyds INTEGER,
    vesselTypeCode TEXT,
    vesselName TEXT,
    prevPort TEXT,
    portToVisit TEXT,
    nextPort TEXT,
    agentName TEXT,
    shippingCompany TEXT,
    eta TIMESTAMP NULL,
    ata TIMESTAMP NULL,
    portAreaCode TEXT,
    portAreaName TEXT,
    berthCode TEXT,
    berthName TEXT,
    etd TIMESTAMP NULL,
    atd TIMESTAMP NULL,
    passengersOnArrival INTEGER DEFAULT 0,
    passengersOnDeparture INTEGER DEFAULT 0,
    crewOnArrival INTEGER DEFAULT 0,
    crewOnDeparture INTEGER DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

  ```postgresql
  CREATE TABLE IF NOT EXISTS arrivals (
    id SERIAL PRIMARY KEY,
    portCallId INTEGER,
    eta TIMESTAMP NULL,
    old_ata TIMESTAMP NULL,
    ata TIMESTAMP NOT NULL,
    vesselName TEXT,
    portAreaName TEXT,
    berthName TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
    
Now you have a database "portman" with a table "voyages" and a table "arrivals" in it. You can now run the tests.

## The following steps are required to run the tests (quick start):
1. Install required packages/libraries needed for testing: ```pip install -r requirements.txt```
2. Run the a separate test: ```pytest PortmanTests/test_portman.py::TestPortman::test_get_db_connection -v```
3. For running all the test cases, run the following command: ```pytest PortmanTests/test_portman.py -v```
4. For listing all the test cases, run the following command: ```pytest --collect-only -v```
5. For running all the test cases and generating a report, run the following command: ```pytest PortmanTests/test_portman.py -v --html=report.html```

# If quick start didn't work:

## List installed python versions
py -0

## Initialize the virtual environment with a different value (optional, if python version is lower than 3.13 and higher than 3.9)
py -3.12 -m venv myenv

## Start (activate lol) the initialized virtual environment
.venv\Scripts\activate

### 1. Install required packages/libraries needed for testing:
```bash
pip install -r requirements.txt
```

### 2. After installing the required packages, run the following command to execute ONE (1) test case, for example testing database connection:
#### (Note: You can replace the test case name with any other test case name)
#### (Note: You need to have a local PostgreSQL database running on your machine to run this test case)
```bash
pytest PortmanTests/test_portman_mock_db.py::TestPortman::test_get_db_connection -v
```

## 3. For running all the test cases, run the following command:
```bash
pytest PortmanTests/test_portman_mock_db.py -v
```

## 4. For listing all the test cases, run the following command:
```bash
pytest --collect-only -v
```

## 5. For running all the test cases and generating a report, run the following command:
```bash
pytest PortmanTests/test_portman_mock_db.py -v --html=report.html
```
