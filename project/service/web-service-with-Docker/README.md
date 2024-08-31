# Set up the web service with local model & docker 

1. Create the folder "web-service". The tree of the folder is 
```
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
├── __pycache__
│   └── predict.cpython-310.pyc
├── models
│   └── xgboost_time_series_energy.bin
├── predict.py
└── test.py
```

2. Install `pipenv` for creating the virtual environment.
    
    `sudo -H pip install -U pipenv`
3. Check the scikit-learn version when building the model.

    `pip freeze | grep scikit-learn`
   - `freeze`: show all the libraries that we currently have installed
4. Install the required version of scikit-learn (optional), flask and the python version in `pipenv`.
    
    `pipenv install scikit-learn==1.3.0 flask --python=3.10`
5. Activate the virtual environment
    
    `pipenv shell`
6. Write the Dockerfile.

7. Build docker image.

   `docker build -t energy-consumption-prediction-service:v1 .`
8. Run docker image

   `docker run -it --rm -p 9696:9696 energy-consumption-prediction-service:v1`

9. Open another terminal to run the `test.py` 
   
    `python test.py`

**Note**:

* `docker ps -a` to lists all containers on your system, both running and stopped. .

* `docker exec -it image_name bash` to run a command in a running container.




