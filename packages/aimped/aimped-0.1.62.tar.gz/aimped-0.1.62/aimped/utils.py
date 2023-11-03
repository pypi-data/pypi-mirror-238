import json
import logging


def get_logger(log_file='Kserve-Glowol.log', log_level=logging.DEBUG):
    """Returns the logger object for logging the output of the server.
    Parameters:
    ----------------
    log_file: str
        The name of the log file to which the logs will be written.
    log_level: int
        The logging level (e.g., logging.DEBUG, logging.INFO, logging.ERROR).  
    Returns:
    ----------------
    logger: logging.Logger
        The configured logger object.
    """
    # Create a FileHandler for writing logs to the specified log_file.
    f_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    # Define a log message format.
    formatter = logging.Formatter('[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    # Set the formatter for the file handler.
    f_handler.setFormatter(formatter)
    # Set the logging level for the file handler.
    f_handler.setLevel(log_level)
    # Get the root logger.
    logger = logging.getLogger()
    # Set the logging level for the logger itself.
    logger.setLevel(log_level)
    # Add the file handler to the logger.
    logger.addHandler(f_handler)
    return logger

############################################# INPUT LIMIT CHECKER #############################################
import os
import io
import base64

try:
    import cv2
    import PyPDF2
    from pydub import AudioSegment
except ImportError as e:
    print(f"Please install the required dependencies: {str(e)}")

class LimitChecker():

    def __init__(self):
        """LimitChecker class constructor"""
        pass
        
    def check_text(self, text_input, input_limit=5000):
        """ Checks if the text input is within the limit"""
        try:
            size = 0
            # text_input is a string
            if isinstance(text_input, str): 
                size = len(text_input)
            # text_input is a list of strings    
            elif isinstance(text_input, list): 
                size = sum(len(text) for text in text_input) 
            else:
                raise ValueError("Unexpected type for text_input. Expected string or a list of strings")
            return size <= input_limit  
        except:
            raise ValueError("An error occurred when processing text_input.")
            
    def check_audio(self, audio_input, input_limit=600, audio_format=""):
        """ Checks if the audio input is within the limit"""
        audio = None 
        if isinstance(audio_input, str):
            # If input_file is a string (file path)
            try:
                audio = AudioSegment.from_file(audio_input)
                duration_ms = len(audio)
                duration_seconds = duration_ms / 1000.0  # Convert to seconds
                return duration_seconds <= input_limit
            except Exception as e:
                error_message = f"Error getting duration of {audio_input}: {e}"
                logging.error(error_message)
                return None
        elif isinstance(audio_input, bytes):
            # If input_file is binary data
            try:
                audio = AudioSegment.from_file(io.BytesIO(audio_input))
                duration_ms = len(audio)
                duration_seconds = duration_ms / 1000.0  # Convert to seconds
                return  duration_seconds <= input_limit
            except Exception as e:
                error_message = f"Error getting duration from binary data: {e}"
                logging.error(error_message)
                return None
        elif audio_format == "base64":
            # If input_file is base64 encoded
            try:
                audio = AudioSegment.from_file(base64.b64decode(audio_input))
                duration_ms = len(audio)
                duration_seconds = duration_ms / 1000.0
                return duration_seconds <= input_limit
            except Exception as e:
                error_message = f"Error getting duration from base64 data: {e}"
                logging.error(error_message)
                return None
        else:
            error_message = "Unsupported input type. Please provide a file path (str) or binary data (bytes)."
            logging.error(error_message)
            return None
    

    def check_images(self, images_list, input_limit=4):
        """ Checks if the number of images input is within the limit"""
        try:
            size = len(images_list)
            logging.info(f"Number of images: {size}")
            return size <= input_limit
        except:
            raise ValueError("Please provide a correct image list input")
            
    def check_pdf(self, pdf_input, input_limit=10, pdf_format=""):
        """ Checks if the number of pages in the pdf input is within the limit"""
        try:
            pdfReader = None
            if isinstance(pdf_input, str):
                # if the input is a file path
                if os.path.isfile(pdf_input):
                    pdfFileObj = open(pdf_input, 'rb')
                    pdfReader = PyPDF2.PdfReader(pdfFileObj)
            elif isinstance(pdf_input, bytes):
                # if the input is bytes (binary)
                pdfFileObj = io.BytesIO(pdf_input)
                pdfReader = PyPDF2.PdfReader(pdfFileObj)
            elif pdf_format.lower() == "base64":
                # if the input is base64 string
                pdfFileObj = io.BytesIO(base64.b64decode(pdf_input))
                pdfReader = PyPDF2.PdfReader(pdfFileObj)
            else:
                raise ValueError("Unsupported input type. Please provide a file path (str), binary data (bytes), or base64 string")

            if pdfReader:
                return len(pdfReader.pages) <= input_limit
        except Exception as e:
            raise ValueError(f"Error processing PDF. {str(e)}.")
    
    def check_video(self, video_input, input_limit=600, video_format=""):
        """ Checks if the video input is within the limit"""
        try:
            video = None
            if os.path.isfile(video_input):
                video = cv2.VideoCapture(video_input)
                total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
                frames_per_second = video.get(cv2.CAP_PROP_FPS)
                video_length_in_seconds = total_frames / frames_per_second
                logging.info(f"Video length: {video_length_in_seconds}")
                return video_length_in_seconds <= input_limit
            elif video_format == "base64":
                video = cv2.VideoCapture(base64.b64decode(video_input))           
                return (video.get(cv2.CV_CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS) if video else 0) <= input_limit
        except:
            raise ValueError("Please provide a correct video input")
        finally:
            if video:
                video.release()
    
    def check_dicom(self, dicom_list, input_limit=1):
        """ Checks if the number of dicom files input is within the limit"""
        try:
            size = len(dicom_list)
            logging.info(f"Number of dicom files: {size}")
            return size <= input_limit
        except:
            raise ValueError("Please provide a correct dicom list")
         
         
# if __name__ == "__main__":
#     checker = LimitChecker()
#     text = "This is a text"
#     print("Text: {}".format(checker.check_text(text)))
#     audio = "audio.mp3"
#     print("Audio: {}".format(checker.check_audio(audio)))
#     images = ["image1.jpg", "image2.jpg"]
#     print("Images: {}".format(checker.check_images(images)))
#     pdf = "pdf.pdf"
#     print("PDF: {}".format(checker.check_pdf(pdf)))
#     video = "video.mp4"
#     print("Video: {}".format(checker.check_video(video)))
#     dicom = ["dicom1.dcm", "dicom2.dcm"]
#     print("Dicom: {}".format(checker.check_dicom(dicom)))