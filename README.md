# Raspberry Pi robot

## intro

Obstacle avoiding raspberry pi robot, with distributed software architecture, at the moment this readme just gives an overview of what the hardware and software does. Soon more information will be added on both how the software works and how it was designed.

<img src="robot.jpg" alt='the robot' width='400px'/>

This is a rewrite of a project that was mainly written in nodejs. there are quite a few things i have already done in that project and others that i just need to reimplement.

There are parts of this project that aren’t completed this will probably always be the case. This is a passion project, it is something I plan to continuously experiment with refactor and add to. Although there is much in an uncompleted state there is also much that can run and works brilliantly.

## Associated libraries

This library composes other robotics libraries i wrote.

### Buildhat-alternative

an alternative library to the official library for the build hat, that overcomes some of its issues with speed control. i use this for speed control of motors. This is the main library for controlling the library and there is more info about it in the readme.

https://github.com/gregorianrants/buildhat-alternative

### Robonet

a library for communication between nodes on robot and across lan using zeromq

https://github.com/gregorianrants/robonet

### composed-robot-desktop

communicates with robot via robonet. will be used for viewing output of camera, and intensive data processing and other things best done of pi. so far i am using for outputting a plot of encoder readings.

https://github.com/gregorianrants/composed-robot-desktop

## Software Architecture

Multiple Nodes running on separate processes both on robot and off robot across the network

Publisher Nodes register their node_name and topic with a manager node.

Subscriber nodes that are interested in listening to a topic and/or node_name get the address that the topic/nodes are publishing on from the manager node. The nodes then communicate directly with each other in peer to peer fashion using events.

I previously used this system to communicate between nodes written in different languages. I now only use python.

Nodes can be composed in diverse ways to create behaviors. vs code tasks are used to launch suites of nodes and run behaviors.

## Obstacle avoidance

here is a video of the robot doing obstacle avoidance

<a href="https://1drv.ms/v/s!Aom8i-zBShxvrOkKXISSJo1OxN6IYw?e=2Tu53M" title="Link Title"><img src="image.png" alt="Alternate Text" /></a>

this uses 2 nodes that run on the raspberry pi and the hub node that allows them to know how to communicate.

all three programs can be run at once using vs code tasks see .vscode/tasks.json the task for this behavior is avoid-group

## where i am going with this

next up is use computer vision to locate lego wheels drive up to the wheels then push them to a dro off location. this will use the subsumption architecture. I will also need to add odometry using encoders. I will calibrate the camera and use arduco markers of know location to correct the location drift.
