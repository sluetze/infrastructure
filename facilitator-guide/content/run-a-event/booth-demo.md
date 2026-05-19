---
title: Booth demo
hero: "Booth demo"
description: "..."
icon: material/run
---
# Booth demo

Depending on the space available, you might not be able to run a full robot hackathon there. The robot primarily tries to gain attention.
Thus, it's recommended to complete the workshop in advance as preparation, and then use the booth time to showcase the technology and results. For the demo, you can use a customized version of the [`starter-app.py`](./booth-demo/starter-app.py) (located in this booth-demo folder), which simply turns the robot clockwise and performs a "happy dance" when it detects a Red Hat.

## Talking Points

### ONE Platform "From Core to Edge"

Say:

* Red Hat OpenShift is the Infrastructure everything runs on (Fully blown Openshift to Microshift on the Edge)
  * "Data Center Showcase". The Robot is:
    * Taking Photos (initiated from the starter-app)
    * Sending them to the Inference Endpoint at the Core
    * The response is used by the starter-app on the Core to make a movement decision
    * The Movement is send to the robot
  * "Edge Showcase". The Robot is:
    * Taking photos (intiated from the starter-app ON THE ROBOT)
    * Sending them to the Inference Endpoint, running on the Robot
    * The response is used by the starter-app on the ROBOT to make a movement decision
    * The movement is done afterwards

Show:

* The Starter App in DevSpaces and the "GUI" in another Tab. Configure DevSpaces in the way, that it shows the "current.jpg" and "current_boxes.jpg".
  * Start the Robot Run
  * Show the Happy - Dance when the Robot sees the Red Hat
* The intiation of the robot run via CLI
  * Start the Robot Run with the CLI
  * Show the Happy - Dance when the Robot sees the Red Hat

### (AI) Development

Say:

* Red Hat DevSpaces delivers the capabilities to develop on the same platform as the production environment
* Red Hat DevSpaces allows to connect to models for AI-assisted Development
* Red Hat OpenShift AI allows to train and re-train models
* Red Hat OpenShift Pipelines allows to build and package the Application and the model

Show:

* DevSpaces and the Continue Plugin (prepare it with some prompts already)
* Show the hosted Model
* Show the ML Training Pipeline
* Show Tekton Pipeline in Red Hat OpenShift

### AI Inferencing

Say:

* Red Hat OpenShift AI allows to host Models for inferencing (as used in the Showcase)
* We provide
  * validated models
  * ML-Pipelines and toolings to modify/finetune them
  * vLLM and llm-d for more efficient and sophisticated use-cases
* You can start small utilizing Red Hat AI Inferencing Server
* We provide special NVidia Day-0 Versions of our Software to allow bleeding-edge development and experiencing.

Show:

* Red Hat OpenShift AI Model hosting
