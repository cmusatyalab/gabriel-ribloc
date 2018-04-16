# RibLoc Wearable Cognitive Assistance

This cognitive assistant helps train a surgeon to use RibLoc medical kit for
fixating broken ribs. It mainly uses Faster-RCNN with VGG to detect objects in
the video frames to recognize user states and provides feedback.

# What's in this repo

  * start_demo.sh: helper script to run the demo
  * model: a directory containing the DNN's prototxt and model files. The trained models can be downloaded from [here](https://storage.cmusatyalab.org/gabriel-model/ribloc). The md5sum is acc6bc44993f16108b7b8fbe8c291a23.
  * images_feedback: feedback images to be displayed on the mobile device
  * ribloc: the main executable
  * task.py: the procedures of the workflow
  * ikea_cv.py: provides an interface to detect objects in the current frame using Faster-RCNN
  * soundpub.py/soundsub.py: audio instruction publisher and subscriber. They are used in a demo to let audience hear what the instructions the user is hearing. 
