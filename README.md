# Extracted-String-Processor-Microservice
This is a microservice I wrote as part of a larger start-up project. The microservice 
is an extracted string processor that organizes and stores data in PostgreSQL.


## Main Systems and Functionality
The program runs in a docker container and waits for a start command. It then pulls 
data from MongoDB, cleanses it, and then inserts it into our main tables in PostgreSQL. 


## Technology Stack
- Python
   - Primary language used for string manipulation and database insertions
- Postgres
   - Used to store data within tables in our relational database
- MongoDB
   - Used to pull data from the previous microservice