# imageClassificationSagemaker
The objective of this project is to classify images as cycle or bike. The image classification model was trained and deployed as a sagemaker endpoint. 

lambda.py file has 3 functions with each funtion responsible for serializing an image, classifying an image and predicting the probabilities of each class respectively.

The three lambda functions were tied together as a step function and the step function in json format could be found in execution-detail.json file.
