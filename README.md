# Face_Mask_Detection
This is a computer vision machine learning project to detect whether people are wearing face masks or not in image and video datasets.

### Run locally
1. Clone the repository on your local machine using `git clone https://github.com/aradhya-gupta/Face_Mask_Detection.git` .
2. Install all dependencies using `pip install -r requirements.txt`. If some dependency is still missing, do `pip install dependency_name`.
3. Type `streamlit run app.py` in your terminal to run the web interface locally.
4. In the case of videos, the web interface helps for realtime video stream from the primary webcam of your local machine. To check for a video file stored locally run the command `python detect_mask_video.py`. Before running the command, make sure that the correct file path is provided in detect_mask_video.py.

### Repository Contents
- **app.py**: base file for the streamlit web interface
- **train_mask_detector.py**: file to train the model for detecting face masks
- **mask_detector.model**: model to detect face masks
- **detect_mask_video.py**: file to detect masks in a video file
