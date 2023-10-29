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
