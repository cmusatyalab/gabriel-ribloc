# RibLoc Wearable Cognitive Assistance

[![Docker pull status](https://img.shields.io/docker/pulls/cmusatyalab/gabriel-ribloc.svg)](https://hub.docker.com/r/cmusatyalab/gabriel-ribloc)

This cognitive assistant helps train a surgeon to use [RibLoc](https://acuteinnovations.com/product/ribloc/) medical kit for
fixating broken ribs. It mainly uses Faster-RCNN with VGG to detect objects in
the video frames to recognize user states and provides feedback.

## Demo Videos

[![Ribloc Demo
Video](http://img.youtube.com/vi/DANM2W1gVEI/0.jpg)](https://youtu.be/DANM2W1gVEI)

[![Ribloc Demo Video](http://img.youtube.com/vi/YRTXUty2P1U/0.jpg)](https://youtu.be/YRTXUty2P1U)

## What's in this repo

  * [ribloc](ribloc): the core python module for Ribloc Gabriel Server
    * model: a directory containing the DNN's prototxt and model files. The trained models can be downloaded from [here](https://storage.cmusatyalab.org/gabriel-model/ribloc-model.zip). 
    * images_feedback: feedback images to be displayed on the mobile device
  * [android-client](android-client): phone client.
  * [Dockerfile](Dockerfile): Dockerfile for building the Ribloc server container.

## How to Run

### Server

```bash
docker run -it --rm --gpus all -p 9099:9099 cmusatyalab/gabriel-ribloc:latest
```

### Client

Use Android Studio to compile and install [android-client](android-client). Note
that Google Play Services are needed for speech recognition.
