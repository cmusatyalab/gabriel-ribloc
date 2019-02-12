# RibLoc Wearable Cognitive Assistance

This cognitive assistant helps train a surgeon to use [RibLoc](https://acuteinnovations.com/product/ribloc/) medical kit for
fixating broken ribs. It mainly uses Faster-RCNN with VGG to detect objects in
the video frames to recognize user states and provides feedback.

# What's in this repo

  * start_demo.sh: helper script to run the demo
  * model: a directory containing the DNN's prototxt and model files. The trained models can be downloaded from [here](https://storage.cmusatyalab.org/gabriel-model/ribloc). The md5sum is acc6bc44993f16108b7b8fbe8c291a23.
  * images_feedback: feedback images to be displayed on the mobile device
  * ribloc: the main executable
  * task.py: the procedures of the workflow
  * ikea_cv.py: provides an interface to detect objects in the current frame using Faster-RCNN

# How to Run

## Server

```bash
nvidia-docker run --rm -it --name sandwich \
-p 0.0.0.0:9098:9098 -p 0.0.0.0:9111:9111 -p 0.0.0.0:22222:22222 \
-p 0.0.0.0:8080:8080 -p 0.0.0.0:7070:7070 \
cmusatyalab/gabriel-ribloc:latest
```