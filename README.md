# Parking Lot Monitor

|Name               |Student Number|
|-------------------|--------------|
|Mustafa Abdulmajeed|101013246     |
|Thomas Bryk        |101008746     |
|Yupeng Guo         |100967808     |
|Parfait Kingwaya   |101000644     |

## Summary
The project our group chose is the Parking Lot Monitor project, The goal of this project is to be able to monitor the state of a parking lot by identifying vacant parking spaces and notifying when there’s no available parking space. We plan to accomplish this by mounting one or more cameras in a parking area and monitor its state throughout the day and update the status in real time. The resulting program in a real-time system could continuously track a parking lot and label parking spots, which could be used to create a digital map with parking availability in real time.

## Background   
Finding a parking spot can be a daunting task especially during rush hours. Students at Carleton University also tend to struggle with this. Shopping malls and underground parking lots also bring this problem to light, hence why we chose it. It would be very beneficial and convenient to be able to pinpoint available parking spaces in a given compound. This system could help valets and numerous parking lot compounds in many different cities.

This problem can be solved by implementing machine learning models using openCV. There are two main steps in our parking lot detection model:
1. Detecting the position of all available parking spot
2. Identified if a parking space is vacant or occupied
3. Update the status of the parking lot

In specific, we first need to identify the parking spot using edge detection technology, such as canny edge detector which uses multi-stage algorithms to detect a wide range of edges in images. After detecting the edge, we need to extract ROI (region of interest) which are all available parking spot. We can use object detection to identify which is a vacant spot or an occupied.  Another option is to use a common technique called Background subtraction that will help identify the foreground and background(empty parking space). A combination of those techniques could be useful as well in order to accomplish this task.

## The Challenge
One of the main challenges of this project is finding the best angles for the cameras to be mounted in order to properly monitor a parking lot or a space. How would it handle cars of the same colour if they were to be parked too close to each other? Would it be able to estimate depth and figure out that this blob of colour is occupying two spaces? Another problem that comes with this is if the cars hide the lines of the parking lot. This would be a challenge if we used the lines as guidelines to which slots are vacant and which are not. 

Another challenge presented is the lighting of the environment; it would change based on the day and may interpret colours differently based on the weather and the time of day. However, we could limit the scope of the project to only day-time scanning as parking lots tend to get more vacant during the night time.

We will utilize OpenCV to create models to recognize the vacancies. We could also utilize a previous database of recordings of an occupied vs a vacant one to decide which lots are empty. We could also use the approach of hard coding a parking map for a certain lot to estimate the locations.


## Goals and Deliverables
We plan to create a system that utilizes a camera to monitor a parking lot. Success for this project is being able to detect what a vacant parking space looks like and what a taken one looks like. Once we get the status being able to upload to a database or update a tracking device to notify the user of the changes. Being able to accomplish this is what we believe will give us the grade we desire.

If we have enough time and resources we want to have a network of cameras monitoring a bigger surface area of a given parking lot. Having a graphical user interface to showcase a mapped out parking lot and clearly show which parking space is available.

We will provide a recording of our experiment in order to demonstrate that it works. The recording will consists of a series of screen captures of the logging of the parking spaces and the video feed from the cameras. We will show the live updates as the events of video where occurring from cars parking and leaving.

In terms of realisticness, this project depends mostly on the data that we use to create our model. If the cars entering and leaving the lot are consistent, then our model will be able to handle them based on the data. If we have an underperforming model, we will also use Background Subtraction technique to help the performance of our system.

## Schedule

|Week \ Assignments|Mustafa|Thomas|Parfait|Yupeng|
|---|---|---|---|---|
|Week 1: Feb 1 - 7|Researching Webcam module|Research Raspberry Pi|Python on Pi|Research data sets for parking lots|
|Week 2: Feb 8 - 14|Implementation of webcam with Pi|Implementation of webcam with Pi|Implementation of webcam with Pi|Implementation of webcam with Pi|
|Week 3 Feb 15 - 21 |Implementation of webcam with Pi|Implementation of webcam with Pi|Implementation of webcam with Pi|Implementation of webcam with Pi|
|Week 4 Feb 22 - 28|Algorithm implementation|Algorithm implementation|Algorithm implementation|Algorithm implementation|
|Week 5 Feb 29 - Mar 7|Algorithm implementation|Algorithm implementation|Algorithm implementation|Algorithm implementation|
|Week 6 Mar 8 - 14 |Algorithm implementation|Algorithm implementation|Algorithm implementation|Algorithm implementation|
|Week 7 Mar 15 - 21|Testing|Testing|Testing|Testing|
|Week 8 Mar 21 - 27|Validation|Validation|Real-life test|Real-life test|
|Week 9 Mar 28 - Apr 3|Preparing for demo|Preparing for demo|Preparing for demo|Preparing for demo|
|Week 10 Apr 4 - 10|Demo|Demo|Demo|Demo|

- For Week 1, we will research the necessary configurations for this project, such as hardware and software we could use.
- For Weeks 2 and 3, we will start implementation on getting data from the camera and integrating it with the Pi. If this is done early then we can start early for the algorithm.
- Weeks 4 - 6 will consist of getting the algorithm to work with our camera feed, which will be the challenge of this project.
- Week 7 will consist of testing the code to see if it does what it needs to.
- Week 8 will consist of validation of the project against real-life data from parking spaces around us, such as Carleton parking or Greenboro park and ride.
- Week 9 is when we will start preparing for the demonstration.
- Week 10 will be the demo week, where we will present our results.

## Setup

Create a Python Virtual environment

activate the environment
```
pip install tensorflow==1.13.1 (deprecated)
pip install keras (deprecated)
pip install numpy
pip install opencv-python
pip install imutils
```

Since I had issues with pushing large files to the repo I added them to Google drive in zip files.

## Running the App
Download the video captured by Thomas (link should be in the messenger)

Once thats done download the zip files that contain the modified imageai library that I modified to suit our needs
and the moldels needed to run the app. They can be found using this link https://drive.google.com/drive/folders/1j3qLyzkak_tzWeucJeeHMKfMUPS69g4a?usp=sharing

To download the video for the recorded parking lot you can get it at the following link: https://drive.google.com/drive/folders/1Ex2g7yv8H5dU3r-5FOIbnxB2GeYZ-cDw?usp=sharing

Follow these steps:
1. Open your terminal then run the following commands in the path you want to load the project
```
git init
git remote add origin https://github.com/ducongo/parking-a-lot.git
git pull origin master
```
2. Once that's done, unzip the zip files you retrieved from google drive at the root of the project.
3. Then you will need to create a new directory called input were you will store the inout video you download.
4. When all that's done, run the following command to test run the app. Before running the app, make sure you have a folder called 'input' where you will place the parking lot recording
```
python parking_monitoring_final.py
```

If you want the app to stop running on windows you need to press ctrl + pause button to kill opencv windows that runs on different threads.
