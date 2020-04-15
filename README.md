# parking-a-lot


# Setup

Create a Python Virtual environment

activate the environment
>pip install tensorflow==1.13.1 (deprecated)

>pip install keras (deprecated)

>pip install numpy

>pip install opencv-python

>pip install imgutils

Since I had issues with pushing large files to the repo I added them to Google drive in zip files.

# To run the app 
download the video captured by Thomas (link should be in the messenger)

Once thats done download the zip files that contain the modified imageai library that I modified to suit our needs
and the moldels needed to run the app. They can be found using this link https://drive.google.com/drive/folders/1j3qLyzkak_tzWeucJeeHMKfMUPS69g4a?usp=sharing

To download the video for the recorded parking lot you can get it at the following link: https://drive.google.com/drive/folders/1Ex2g7yv8H5dU3r-5FOIbnxB2GeYZ-cDw?usp=sharing

Follow these steps:
Open your terminal then run the following commands in the path you want to load the project

> git init

>git remote add origin https://github.com/ducongo/parking-a-lot.git

>git pull origin master

Once thats done unzip the zip files you retrieved from google drive at the root of the project.

Then you will need to create a new directory called input were you will store the inout video you download.

When all thats done run the following command to test run the app
Before running the app, make sure you have a folder called 'input' where you will place the parking lot recording

> python parking_monitoring_final.py

If you want the app to stop running on windows you need to press ctrl + pause button to kill opencv windows that runs on different threads.

