# dvc-project-template
DVC project template

## STEPS -

### STEP 01- Create a repository by using template repository

### STEP 02- Clone the new repository

### STEP 03- Create a conda environment after opening the repository in VSCODE

```bash
conda create --prefix ./env python=3.7 -y
```

```bash
conda activate ./env
```
OR
```bash
source activate ./env
```

### STEP 04- install the requirements
```bash
pip install -r requirements.txt
```

### STEP 05- initialize the dvc project
```bash
dvc init
```

### STEP 06 - Dags hub Experiments- ML FLow
```
MLFLOW_TRACKING_URI=https://dagshub.com/deepak2009thakur/Hotel-Booking-Dataset-mlflow-dvc.mlflow \
MLFLOW_TRACKING_USERNAME=deepak2009thakur \
MLFLOW_TRACKING_PASSWORD=09a89198ee7cb39d44891d982e04cef1c388d58a \
python script.py
```

![Alt text](image.png)

## Hotel Booking Dataset

The online hotel reservation channels have dramatically changed booking possibilities and customers’ behavior. A significant number of hotel reservations are called-off due to cancellations or no-shows. The typical reasons for cancellations include change of plans, scheduling conflicts, etc. This is often made easier by the option to do so free of charge or preferably at a low cost which is beneficial to hotel guests but it is a less desirable and possibly revenue-diminishing factor for hotels to deal with.

# Installation

To run my app on your local machine, do the following steps.

## Step 1 :

I have written the Code with Python 3.9.17. If you don't have Python installed you can find it here.
If you are using a lower version of Python you can upgrade using the pip package, kindly ensure that you have the latest version of pip.

## Step 2 :

If you want the current version of my repository to be in your github, you can do forking my repository visiting https://github.com/aakashsyadav1999/Hotel-Reservations-Dataset-mlflow.git

Clone my repository to your local machine by running the following command. Before doing this, you have to install git on your machine and make sure you are having proper internet connection.

For Windows OS user, open git bash and run the following command.

git clone https://github.com/aakashsyadav1999/Hotel-Reservations-Dataset-mlflow.git

For Linus OS user, open Terminal and run the following command.

git clone https://github.com/aakashsyadav1999/Hotel-Reservations-Dataset-mlflow.git

If you don't want to mess up with all these things, you can just download the zip file of my GitHub repository by clicking here and extract it to any file location as your wish and then use it.

Now we have done with the downloading of my whole project.

## Step 3 :

After downloading the whole repo, get into the main folder by hit the following command in git bash for Windows OS users and Terminal for Linux OS users.

cd Hotel-Reservations-Dataset-mlflow

## Step 4 :

Now we are going to install all the dependency libraries for this project. Before that you must have Python 3.9.17 and latest version of pip.

To install all the dependency libraries in a single command, run the following command.

pip install -r requirements.txt

## Step 5 :

After installing all the dependency libraries, you are ready to run my app on your local machine.

To launch my app on your local machine, hit the following command.

python ml_projects.py

## Run

Now you have successfully launched my app on your local machine.

To view my app, hit the following URL in any of the browser such as Chrome, FireFox, etc..,

## http://127.0.0.1:5000 - For welcome page

## http://127.0.0.1:5000/predictdata - for prediction site
