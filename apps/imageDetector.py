# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from PIL import Image
import imutils
import time
import cv2
import os
from os.path import dirname, join
import streamlit as st
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN

def app():
    model = tf.keras.models.load_model('mask_detector.model')
    st.write("""
            #  Detecting Face Mask in an Image
            """
            )
    st.write("Upload an `image` to detect whether people are wearing masks or not!")
    file = st.file_uploader("Please upload an image file", type=["jpg", "png","jpeg"])

    if file is not None:
        img = Image.open(file)
        frame = np.array(img)
        def detect_and_predict_mask(frame, faceNet, maskNet):
            # grab the dimensions of the frame and then construct a blob
            # from it
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                (104.0, 177.0, 123.0))

            # pass the blob through the network and obtain the face detections
            faceNet.setInput(blob)
            detections = faceNet.forward()
            print(detections.shape)

            # initialize our list of faces, their corresponding locations,
            # and the list of predictions from our face mask network
            faces = []
            locs = []
            preds = []

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the detection
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > 0.4:
                    # compute the (x, y)-coordinates of the bounding box for
                    # the object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # ensure the bounding boxes fall within the dimensions of
                    # the frame
                    (startX, startY) = (max(0, startX), max(0, startY))
                    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                    # extract the face ROI, convert it from BGR to RGB channel
                    # ordering, resize it to 224x224, and preprocess it
                    face = frame[startY:endY, startX:endX]
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face = cv2.resize(face, (224, 224))
                    face = img_to_array(face)
                    face = preprocess_input(face)

                    # add the face and bounding boxes to their respective
                    # lists
                    faces.append(face)
                    locs.append((startX, startY, endX, endY))

            # only make a predictions if at least one face was detected
            if len(faces) > 0:
                # for faster inference we'll make batch predictions on *all*
                # faces at the same time rather than one-by-one predictions
                # in the above `for` loop
                faces = np.array(faces, dtype="float32")
                preds = maskNet.predict(faces, batch_size=32)

            # return a 2-tuple of the face locations and their corresponding
            # predictions
            return (locs, preds)
        def detect_and_predict_mask_mtcnn(frame, faceNet, maskNet):
            result_list = faceNet.detect_faces(frame)
            faces = []
            locs = []
            preds = []
            for result in result_list:
                x1, y1, width, height = result['box']
                # bug fix
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                # extract the face
                face = frame[y1:y2, x1:x2]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                # add the face and bounding boxes to their respective
                # lists
                faces.append(face)
                locs.append((x1, y1, x2, y2))
            if len(faces) > 0:
                faces = np.array(faces, dtype="float32")
                preds = maskNet.predict(faces, batch_size=32)
            return (locs, preds)



        # load our serialized face detector model from disk
        # prototxtPath = r"C:\\Users\\Aradhya\Desktop\\Face_Mask_Detection\\apps\\face_detector\\deploy.prototxt"
        # weightsPath = r"C:\\Users\\Aradhya\\Desktop\\Face_Mask_Detection\\apps\\face_detector\\res10_300x300_ssd_iter_140000.caffemodel"
        # prototxtPath = join(dirname(__file__), "deploy.prototxt")
        # weightsPath = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel")
        # faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        faceNet = MTCNN()
        # load the face mask detector model from disk
        maskNet = load_model("mask_detector.model")

        # # initialize the video stream
        # print("[INFO] starting video stream...")
        # vs = VideoStream(src=0).start()
        # # vs = cv2.VideoCapture('videos/TimesSquare.mp4')

        # # loop over the frames from the video stream
        # while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            # frame = vs.read()
            # _,frame = vs.read()
        frame = imutils.resize(frame, width=400)

            # detect faces in the frame and determine if they are wearing a
            # face mask or not
        # (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        (locs, preds) = detect_and_predict_mask_mtcnn(frame, faceNet, maskNet)

        totalFaces = len(locs)
        facesWithMask = 0
            # loop over the detected face locations and their corresponding
            # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            if mask > withoutMask:
                label = "Mask"
                facesWithMask+=1
            else:
                label = "No Mask"
            # label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (255, 0, 0)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

            # show the output frame
        # cv2.imshow("Frame", frame)
        st.write(""" #### Total number of people detected:  """, totalFaces)
        st.text("")
        st.write(""" #### Number of people wearing masks:  """, facesWithMask)
        st.text("")
        st.text("")
        st.image(frame)
            # key = cv2.waitKey(1) & 0xFF

            # # if the `q` key was pressed, break from the loop
            # if key == ord("q"):
            # 	break


    