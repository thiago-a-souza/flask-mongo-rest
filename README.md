# flask-mongo-rest

Sample REST API using Flask and MongoDB

# Pre-requisites
- Docker 
- Python 3.7
- Pip

# Install

## Python dependencies

```
pip install -r requirements.txt
```
  
## Run MongoDB

```
docker run -p 27017:27017 mongo
```


## Run the application

```
cd src/
python app.py
```


# Testing 

**1.** Get country

```
curl localhost:5000/api/v1/resources/countries/BR
```

**2.** Delete country

```
curl -X DELETE localhost:5000/api/v1/resources/countries/AR
```

**3.** Update country

```
curl -X PUT localhost:5000/api/v1/resources/countries \
-H "Content-Type: application/json" \
--data '{"_id": "BR", "country":"Brasil", "capital":"Brasilia","phone":"+55"}' 
```

**4.** Add country

```
curl -X POST localhost:5000/api/v1/resources/countries \
-H "Content-Type: application/json" \
--data '{"_id": "TST", "country":"Testing", "capital":"TestingLand","phone":"+123"}' 
```
