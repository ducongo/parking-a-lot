# parking-a-lot


# Setup

Create a Python Virtual environment

activate the environment
>pip install tensorflow==1.13.1

>pip install keras

>pip install imgutils

Since I had issues with pushing large files to the repo I added them to Google drive in zip files.

# To run the app 
download the video captured by Thomas (link should be in the messenger)

Once thats done download the zip files that contain the modified imageai library that I modified to suit our needs
and the moldels needed to run the app. They can be found using this link https://drive.google.com/drive/folders/1j3qLyzkak_tzWeucJeeHMKfMUPS69g4a?usp=sharing

Follow these steps:
Open your terminal then run the following commands in the path you want to load the project

< git init

>git remote add origin https://github.com/ducongo/parking-a-lot.git

<git pull origin master

Once thats done unzip the zip files you retrieved from google drive at the root of the project.

Then you will need to create a new directory called input were you will store the inout video you download.

When all thats done run the following command to test run the app

> python parking_monitoring.py

If you want the app to stop running on windows you need yo press ctrl + pause button to kill opencv windows that runs on different threads.

parking_monitoring.py is the main file for the logic of the monitoring process. We need to add logic to detect the state of a parking spot. The thread for scanning the parking lot runs every 10 secs because it is computationaly expensive to feed all the frames of the video through the model.
