# Piezoelectric Sensor Machine Learning Training and Deployment Module

This code trains a machine learning algorithm to detect and alert the user about anomalies in Piezoelectric Sensor values indicating cutting blade damage

## Scripts

* **Script 1**: main.py trains the model and determines a threshold value
* **Script 2**: live-data.py deploys the model on real world data received through LabVIEW and alerts the user

## Getting Started
### Libraries
* **Numpy**: required for data analysis
* **Tensorflow**: machine learning algorithm

## Usage

To get started run the main.py code with a training xml to develop the model that will detect anomalies. Next, when running the LabVIEW code, the data should stream to the python script live-data.py
and alert when there is an anomaly.
