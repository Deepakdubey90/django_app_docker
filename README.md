# Dkango app with docker 


### Virtualenv
```
# installing virtualenv
pip install virtualenv

# create a virtualenv
virtualenv -p python3 venv

# activate virtualenv
. env/bin/activate
```

### Install app
```
# install the scheduler backend along with all the python dependencies
make install
```

### Migrations 
```
make makemigration
```

### Migrate 
```
make migrate
```

### Run app
```
# run webapp
make run
```

### Run test cases
```
# run test cases
make test
```
