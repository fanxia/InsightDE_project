# Zoo-Tube   (Insight Data Engineering Project 2019B)

## Table of Contents
1. [Project Overview](README.md#project overview)
1. [Pipeline](README.md#pipeline)
1. [Running Instruction](README.md#instructions)
1. [Questions?](README.md#questions?)

## Project Overview

### Zoo-Tube: Jump to your favorite animal!

If you want to see your favorite bear in an hourly long video, and avoid wasting time to watch through the whole video.
My application will offer you a quick summary of animals shown up in the video and provides the links that you can jump to see your favorite animal with one click. The 30 mins long video can be processed within one minutes, you can use this as a quick preview. Further, with available ML models, this idea can be extrapolated to applications like instant check of long surveillance video to find endangered animals, to find suspects.; quick investigate for drug, weapon usage in movie; and more area. 

### Video demo

[demo link]()

### Approach

- YOLO + Cloud Computing
- YOLO is object detection application in Neural Network model Darknet. It can detect animals in image. Refer to [here](https://pjreddie.com/darknet/yolo/).
- Cloud Computing helps to scale up the computing ability. Here, AWS EC2 serviced are used to launch kubernetes cluster.

## Pipeline
![Alt text](AnimalTag/pics/pipeline.png)

## Running Instruction

### Repo directory structure

The Zoo-Tube directory is structured in this way:

    ├── README.md
    ├── Zoo-Tube
        ├── src
        │   └── anitag_app.py
    	│   └── publisher.py
    	│   └── consumer.py
    	│   └── config.json 
        ├── k8scluster
    	│   └── deployment.yml
	│   └── service.yml	
        ├── dockerimage
        │   └── Dockerfile
        ├── test


### System Setup Procedure

1 Build consumer docker image


2 Deploy consumer to k8s cluster on AWS


3 Build app server with publisher


### System Running


# Questions?
Email me at fanxia08@gmail.com