import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image
from skimage.transform import radon
from google.cloud import vision_v1
from pkg_resources import resource_filename
from idvpackage.ocr_utils import *
from idvpackage.common import *
from idvpackage.sau_id_extraction import *
import face_recognition
import tempfile
from scipy.spatial.distance import cosine
from PIL import Image, ImageEnhance
import json
from googletrans import Translator
from google.oauth2.service_account import Credentials
import pycountry
import sys
from itertools import permutations

class IdentityVerification:

    def __init__(self, credentials_string):
        """
        This is the initialization function of a class that imports a spoof model and loads an OCR
        reader.
        """
        #self.images = images
        # credentials_path = resource_filename('idvpackage', 'streamlit-connection-b1a38b694505.json')
        # self.client = vision_v1.ImageAnnotatorClient.from_service_account_json(credentials_path)
        credentials_dict = json.loads(credentials_string)
        credentials = Credentials.from_service_account_info(credentials_dict)
        self.client = vision_v1.ImageAnnotatorClient(credentials = credentials)
        self.translator = Translator()
        self.iso_nationalities = [country.alpha_3 for country in pycountry.countries]
        
    def image_conversion(self,image):  
        """
        This function decodes a base64 string data and returns an image object.
        :return: an Image object that has been created from a base64 encoded string.
        """
        # image=image.split(',')[-1]
        # Decode base64 String Data
        img=Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
        return img

    def rgb2yuv(self, img):
        """
        Convert an RGB image to YUV format.
        """
        try:
            img=np.array(img)
            return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def find_bright_areas(self, image, brightness_threshold):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_image = cv2.threshold(gray_image, brightness_threshold, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        bright_areas = []

        for contour in contours:
            bounding_box = cv2.boundingRect(contour)

            area = bounding_box[2] * bounding_box[3]

            if area > 800:
                bright_areas.append(bounding_box)

        return len(bright_areas)

    def is_blurry(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        laplacian_variance = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        
        return laplacian_variance

    def identify_input_type(self, data):
        if isinstance(data, bytes):
                return "video_bytes"
        else:
            pass

        try:
            decoded_data = base64.b64decode(data)
            
            if decoded_data:
                return "base_64"
        except Exception:
            pass

        return "unknown"

    def sharpen_image(self, image):
        kernel = np.array([[-1, -1, -1],
                        [-1, 9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)


    def adjust_contrast(self, image, factor):
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Contrast(pil_image)
        enhanced_image = enhancer.enhance(factor)
        return np.array(enhanced_image)

    def adjust_brightness(self, image, factor):
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Brightness(pil_image)
        enhanced_image = enhancer.enhance(factor)
        return np.array(enhanced_image)

    def enhance_quality(self, image):
        sharpened_image = self.sharpen_image(image)
        enhanced_image = self.adjust_brightness(sharpened_image, 1.2)
        enhanced_contrast = self.adjust_contrast(enhanced_image, 1.2)
        # grayscale_image = cv2.cvtColor(enhanced_contrast, cv2.COLOR_BGR2GRAY)
        
        return enhanced_contrast

    def check_document_quality(self, data, brightness_threshold=240, blur_threshold=1500, video_duration_threshold=5):
        input_type = self.identify_input_type(data)
        if input_type == 'base_64':
            image_quality = {
                'error': ''
            }
            
            try:
                # Check if the image can be converted from RGB to YUV
                enhanced_data = self.enhance_quality(np.array(self.image_conversion(data)))
                yuv_img = self.rgb2yuv(self.image_conversion(data))

            except:
                print("\n\nyuv error\n\n")
                image_quality['error'] = 'bad_image'

            try:
                # Check brightness
                brightness = np.average(enhanced_data[..., 0])
                if brightness > brightness_threshold:
                    image_quality['error'] = 'bad_image'
            except:
                image_quality['error'] = 'bad_image'

            try:
                # Check blurriness
                # image = np.array(self.image_conversion(data))
                gray = cv2.cvtColor(enhanced_data, cv2.COLOR_BGR2GRAY)
                fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                if fm < blur_threshold:
                    image_quality['error'] = 'bad_image'
            except:
                print("\n\nbrightness error\n\n")
                image_quality['error'] = 'bad_image'
            
            try:
                # check image coloured or gray
                if not self.is_colored(data):
                    image_quality['error'] = 'bad_image'
            except:
                image_quality['error'] = 'bad_image'
            
            return image_quality
        
        elif input_type == 'video_bytes':
            video_quality = {
                'error': ''
            }
            frame_count_vid = 0
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
                    temp_video_file.write(data)
                
                video_capture = cv2.VideoCapture(temp_video_file.name)

                if video_capture.isOpened():
                    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

                    for _ in range(frame_count):
                        ret, frame = video_capture.read()
#                         if ret:
                            # frame_count_vid+=1
                            # if frame_count_vid % 10 == 0:
                        _, buffer = cv2.imencode('.jpg', frame)
                        image_data = buffer.tobytes()

                        image = vision_v1.Image(content=image_data)

                        response = self.client.face_detection(image=image)
                        if len(response.face_annotations) >= 1:
                            break
#                     else:
#                         # No face detected in any frame
#                         print('here 1')
#                         video_quality['error'] = 'no_face_detected_in_video'
                
                selfie_result = self.extract_selfie_from_video(data)
                if isinstance(selfie_result, dict):
                    video_quality['error'] = selfie_result['error']
                else:
                    selfie_blurry_result, selfie_bright_result = self.get_blurred_and_glared_for_doc(selfie_result)
                    if selfie_blurry_result == 'consider' or selfie_bright_result == 'consider':
                        video_quality['error'] = 'face_not_clear_in_video'
                    else:
                        video_quality['selfie'] = selfie_result

            except Exception as e:
                print(e)
                video_quality['error'] = 'bad_video'

            return video_quality

    # def check_image_quality(self, id_card, brightness_threshold=245, blur_threshold=150):
    #     id_card = self.image_conversion(id_card)
    #     id_card = np.array(id_card)
    #     bright_result = self.find_bright_areas(id_card, brightness_threshold)
    #     blurry_result = self.is_blurry(id_card)

    #     if bright_result > 1:
    #         raise Exception(f"Image is too bright. Threshold: {brightness_threshold}")

    #     if blurry_result < blur_threshold:
    #         raise Exception(f"Image is too blurry. Blurriness: {blurry_result}, Threshold: {blur_threshold}")

    def process_image(self,front_id):
        img = self.image_conversion(front_id)
        img = np.array(img)
        I = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = I.shape
        if (w > 640):
            I = cv2.resize(I, (640, int((h / w) * 640)))
        I = I - np.mean(I)
        sinogram = radon(I)
        r = np.array([np.sqrt(np.mean(np.abs(line) ** 2)) for line in sinogram.transpose()])
        rotation = np.argmax(r)
        angle = round(abs(90 - rotation)+0.5)

        if abs(angle) > 5:
            color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(color_img)
            out = im.rotate(angle, expand=True)
        else:
            out = Image.fromarray(img)
    
        # im = self.image_conversion(front_id)
        # out = im.rotate(angle, expand=True)

        return out

    def is_colored(self, base64_image):
        img = self.image_conversion(base64_image)
        img = np.array(img)

        return len(img.shape) == 3 and img.shape[2] >= 3
    
    def get_blurred_and_glared_for_doc(self, image, brightness_threshold=230, blur_threshold=1500):
        blurred = 'clear'
        glare = 'clear'
        
        # image = self.image_conversion(image)
        # image_arr = np.array(image)
        enhanced_data = self.enhance_quality(image)

        blurry1 = self.is_blurry(enhanced_data)

        if blurry1 < blur_threshold:
            blurred = 'consider'
        
        # yuv_image = self.rgb2yuv(image)
        brightness1 = np.average(enhanced_data[..., 0])
        if brightness1 > brightness_threshold:
            glare = 'consider'

        # glare1 = self.find_bright_areas(front_id_arr, 245)
        # glare2 = self.find_bright_areas(back_id_arr, 245)
        # if glare1 > 5 or glare2 > 5:
        #     glare = 'consider'
        
        return blurred, glare

    def check_nationality_in_iso_list(self, nationality):
        if nationality.upper() in self.iso_nationalities:
            return 'clear'
        else:
            return 'consider'

    def get_face_orientation(self, face_landmarks):
        left_eye = np.array(face_landmarks['left_eye']).mean(axis=0)
        right_eye = np.array(face_landmarks['right_eye']).mean(axis=0)

        eye_slope = (right_eye[1] - left_eye[1]) / (right_eye[0] - left_eye[0])
        angle = np.degrees(np.arctan(eye_slope))

        return angle

    def extract_selfie_from_video(self, video_bytes):
        video_dict = {
            'error': ''
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            temp_video_file.write(video_bytes)
        
        cap = cv2.VideoCapture(temp_video_file.name)

        ret, frame = cap.read()

        if not ret:
            pass

        # Convert frame to bytes
        is_success, buffer = cv2.imencode(".jpg", frame)
        io_buf = io.BytesIO(buffer)
        byte_content = io_buf.getvalue()

        image = vision_v1.Image(content=byte_content)

        # Perform face detection
        response = self.client.face_detection(image=image)
        faces = response.face_annotations

        # Initialize variables
        best_face = None
        best_score = -1

        for face in faces:
            vertices = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
            area = (vertices[2][0] - vertices[0][0]) * (vertices[2][1] - vertices[0][1])

            # Use detection confidence as a metric for clarity
            clarity = face.detection_confidence
            
            # Score to find the best face
            score = area * clarity
            
            if score > best_score:
                best_score = score
                best_face = face

            if best_face:
                vertices = [(vertex.x, vertex.y) for vertex in best_face.bounding_poly.vertices]
                left = vertices[0][0]
                upper = vertices[0][1]
                right = vertices[2][0]
                lower = vertices[2][1]

                frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                cropped_face = frame_pil.crop((left, upper, right, lower))
                best_face = cropped_face

        if best_face is not None:
            return np.array(best_face)
        else:
            print('here 2')
            video_dict['error'] = 'no_face_detected_in_video'
            return video_dict

    def load_and_process_image_fr(self, base64_image, arr=False):
        try:
            if not arr:
                img = self.process_image(base64_image)
                img = np.array(img)
                image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            else:
                image = cv2.cvtColor(base64_image, cv2.COLOR_RGB2BGR)

            # base64_image = base64_image.split(',')[-1]
            # image_data = base64.b64decode(base64_image)
            # image_file = io.BytesIO(image_data)

            # image = face_recognition.load_image_file(image_file)

            face_locations = face_recognition.face_locations(image)

            if not face_locations:
                return [], []
        
            face_encodings = face_recognition.face_encodings(image, face_locations)

            return face_locations, face_encodings
        except:
            return [], []
        
    def calculate_similarity(self, face_encoding1, face_encoding2):
        similarity_score = 1 - face_recognition.face_distance([face_encoding1], face_encoding2)[0]
        return round(similarity_score + 0.25, 2)

    def extract_face_and_compute_similarity(self, selfie, front_face_locations, front_face_encodings):
        face_locations1, face_encodings1 = self.load_and_process_image_fr(selfie, arr=True)
        face_locations2, face_encodings2 = front_face_locations, front_face_encodings

        if not face_encodings1 or not face_encodings2.any():
            return 0
        else:
            # face_encoding1 = face_encodings1[0]
            # face_encoding2 = face_encodings2[0]
            largest_face_index1 = face_locations1.index(max(face_locations1, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))
            largest_face_index2 = face_locations2.index(max(face_locations2, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))

            face_encoding1 = face_encodings1[largest_face_index1]
            face_encoding2 = face_encodings2[largest_face_index2]

            similarity_score = self.calculate_similarity(face_encoding1, face_encoding2)

            return min(1, similarity_score)
    
    def calculate_landmarks_movement(self, current_landmarks, previous_landmarks):
        return sum(
            abs(cur_point.position.x - prev_point.position.x) +
            abs(cur_point.position.y - prev_point.position.y)
            for cur_point, prev_point in zip(current_landmarks, previous_landmarks)
        )

    def calculate_face_movement(self, current_face, previous_face):
        return abs(current_face[0].x - previous_face[0].x) + abs(current_face[0].y - previous_face[0].y)

    def calculate_liveness_result(self, eyebrow_movement, nose_movement, lip_movement, face_movement):
        eyebrow_movement_threshold = 15.0
        nose_movement_threshold = 15.0
        lip_movement_threshold = 15.0
        face_movement_threshold = 10.0

        if (
            eyebrow_movement > eyebrow_movement_threshold or
            nose_movement > nose_movement_threshold or
            lip_movement > lip_movement_threshold or
            face_movement > face_movement_threshold
        ):
            return True
        else:
            return False

    # def check_for_liveness(self, similarity, video_bytes, face_match_threshold, liveness_threshold):
    #     # cap = cv2.VideoCapture(video)
    #     with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
    #         temp_video_file.write(video_bytes)
        
    #     cap = cv2.VideoCapture(temp_video_file.name)

    #     frame_count = 0
    #     previous_landmarks = None
    #     previous_face = None
    #     liveness_result_list = []

    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
            
    #         frame_count += 1

    #         if frame_count % 10 == 0:  # analyze every 10 frames
    #             _, buffer = cv2.imencode('.jpg', frame)
    #             image_data = buffer.tobytes()

    #             image = vision_v1.Image(content=image_data)

    #             response = self.client.face_detection(image=image)
    #             faces = response.face_annotations

    #             largest_face = None
    #             largest_face_area = 0

    #             for face in faces:
    #                 current_landmarks = face.landmarks
    #                 current_face = face.bounding_poly.vertices
    #                 face_area = abs((current_face[2].x - current_face[0].x) * (current_face[2].y - current_face[0].y))

    #                 if face_area > largest_face_area:
    #                     largest_face = face
    #                     largest_face_area = face_area

    #             if largest_face:
    #                 # face = faces[0]
    #                 current_landmarks = largest_face.landmarks
    #                 current_face = largest_face.bounding_poly.vertices

    #                 if previous_landmarks and previous_face:
    #                     eyebrow_movement = self.calculate_landmarks_movement(current_landmarks[:10], previous_landmarks[:10])

    #                     nose_movement = self.calculate_landmarks_movement(current_landmarks[10:20], previous_landmarks[10:20])

    #                     lip_movement = self.calculate_landmarks_movement(current_landmarks[20:28], previous_landmarks[20:28])

    #                     face_movement = self.calculate_face_movement(current_face, previous_face)

    #                     liveness_result = self.calculate_liveness_result(eyebrow_movement, nose_movement, lip_movement, face_movement)

    #                     liveness_result_list.append(liveness_result)

    #                 previous_landmarks = current_landmarks
    #                 previous_face = current_face

    #     cap.release()

    #     if any(liveness_result_list) and similarity>=face_match_threshold:
    #         liveness_check_result = 'clear'
    #     else:
    #         liveness_check_result = 'consider'

    #     return liveness_check_result

    def check_for_liveness(self, similarity, video_bytes, face_match_threshold, frames_to_analyze=10):
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            temp_video_file.write(video_bytes)

        cap = cv2.VideoCapture(temp_video_file.name)

        frame_count = 0
        previous_landmarks = None
        previous_face = None
        liveness_result_list = []

        for frame_count in range(frames_to_analyze):
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            image_data = buffer.tobytes()

            image = vision_v1.Image(content=image_data)

            response = self.client.face_detection(image=image)
            faces = response.face_annotations

            largest_face = None
            largest_face_area = 0

            for face in faces:
                current_landmarks = face.landmarks
                current_face = face.bounding_poly.vertices
                face_area = abs((current_face[2].x - current_face[0].x) * (current_face[2].y - current_face[0].y))

                if face_area > largest_face_area:
                    largest_face = face
                    largest_face_area = face_area

            if largest_face:
                current_landmarks = largest_face.landmarks
                current_face = largest_face.bounding_poly.vertices

                if previous_landmarks and previous_face:
                    eyebrow_movement = self.calculate_landmarks_movement(current_landmarks[:10], previous_landmarks[:10])
                    nose_movement = self.calculate_landmarks_movement(current_landmarks[10:20], previous_landmarks[10:20])
                    lip_movement = self.calculate_landmarks_movement(current_landmarks[20:28], previous_landmarks[20:28])
                    face_movement = self.calculate_face_movement(current_face, previous_face)

                    liveness_result = self.calculate_liveness_result(eyebrow_movement, nose_movement, lip_movement, face_movement)
                    liveness_result_list.append(liveness_result)

                previous_landmarks = current_landmarks
                previous_face = current_face

        cap.release()

        if any(liveness_result_list) and similarity >= face_match_threshold:
            liveness_check_result = 'clear'
        else:
            liveness_check_result = 'consider'

        return liveness_check_result
    def convert_dob(self, input_date):
        day = input_date[4:6]
        month = input_date[2:4]
        year = input_date[0:2]

        current_year = datetime.now().year
        current_century = current_year // 100
        current_year_last_two_digits = current_year % 100

        century = current_century
        # If the given year is greater than the last two digits of the current year, assume last century
        if int(year) > current_year_last_two_digits:
            century = current_century - 1

        final_date = f"{day}/{month}/{century}{year}"

        return final_date

    def convert_expiry_date(self, input_date):
        day = input_date[4:6]
        month = input_date[2:4]
        year = input_date[0:2]

        current_year = datetime.now().year
        current_century = current_year // 100
        current_year_last_two_digits = current_year % 100
        century = current_century

        if int(year) <= current_year_last_two_digits:
            century = current_century
        else:
            century = current_century
        final_date = f"{day}/{month}/{century}{year}"

        return final_date

    def clean_string(self, input_string):
        cleaned_string = re.sub(r'[^\w\s]', ' ', input_string)
        return cleaned_string.strip()
    

    def find_and_slice_number(input_number, digits):
            # Generate all possible permutations of the digits
            perms = [''.join(p) for p in permutations(digits)]
            
            # Initialize variables to keep track of the found pattern and its index
            found_pattern = None
            found_index = -1

            # Search for any permutation of the digits in the input_number
            for perm in perms:
                found_index = input_number.find(perm)
                if found_index != -1:
                    found_pattern = perm
                    break

            # If a pattern is found, slice the number accordingly
            if found_pattern:
                if found_index > len(input_number) - found_index - len(found_pattern):
                    # Slice to the left
                    sliced_number = input_number[:found_index + len(found_pattern)]
                else:
                    # Slice to the right
                    sliced_number = input_number[found_index:]
                
                return sliced_number
            else:
                return ''
            
    def get_ocr_results(self, processed_image):
        with io.BytesIO() as output:
            processed_image.save(output, format="PNG")
            image_data = output.getvalue()

        image = vision_v1.types.Image(content=image_data)
        response = self.client.text_detection(image=image)
        id_infos = response.text_annotations

        return id_infos
    
    def extract_document_info(self, image, document_type, country):

        document_data = {}

        if document_type == 'national_id_back':
            document_data = self.extract_back_id_info(image, country)

        elif document_type == 'national_id_front':
            document_data = self.extract_front_id_info(image, country)
    
            # print(f"getting fron data")
            # if side=='front':
            #     document_data = self.extract_front_id_info(image, country)

            # if side=='back':
            #     document_data = self.extract_back_id_info(image, country)

        elif document_type == 'passport':
            document_data = self.exract_passport_info(image, country)
        
        elif document_type == 'driving_license':
            pass
        
        return document_data
        
    def extract_front_id_info(self, front_id, country):
        if country == 'UAE':
            print("working on UAE")
            front_data = {
                'error': ''
            }
            is_colored1 = self.is_colored(front_id)
            if is_colored1:
                try:
                    processed_front_id = self.process_image(front_id)
                    front_id_text = self.get_ocr_results(processed_front_id)
                    front_id_text = front_id_text[0].description
                    
                    pattern1 = r'Resident Identity'
                    pattern2 = r'Identity Card'
                    m = re.search(pattern1, front_id_text)
                    n = re.search(pattern2, front_id_text)
                    if not (m or n):
                        front_data["error"] = "not_front_id"
                        return front_data
                    
                    img = self.image_conversion(front_id)
                    image = np.array(img)
                    pil_image = Image.fromarray(image)

                    doc_on_pp_result = document_on_printed_paper(image)

                    with io.BytesIO() as output:
                        pil_image.save(output, format="PNG")
                        image_data = output.getvalue()

                    logo_result = detect_logo(self.client, image_data)
                    screenshot_result = detect_screenshot(self.client, front_id)
                    photo_on_screen_result = detect_photo_on_screen(self.client, front_id)

                    front_blurred, front_glare = self.get_blurred_and_glared_for_doc(image)

                    front_face_locations, front_face_encodings = self.load_and_process_image_fr(front_id)

                    front_face_locations_str = json.dumps([tuple(face_loc) for face_loc in front_face_locations])
                    front_face_encodings_str = json.dumps([face_enc.tolist() for face_enc in front_face_encodings])

                    front_data = {
                        'front_extracted_data': front_id_text,
                        'front_coloured': True,
                        'front_doc_on_pp': doc_on_pp_result,
                        'front_logo_result': logo_result,
                        'front_screenshot_result': screenshot_result,
                        'front_photo_on_screen_result': photo_on_screen_result,
                        'front_blurred': front_blurred, 
                        'front_glare': front_glare,
                        'front_face_locations': front_face_locations_str, 
                        'front_face_encodings': front_face_encodings_str
                    }

                    non_optional_keys = ["front_face_locations", "front_face_encodings"]
                    empty_string_keys = [key for key, value in front_data.items() if key in non_optional_keys and value == '']

                    if empty_string_keys:
                        front_data['error'] = 'covered_photo'

                except Exception as e:
                    print(e)
                    front_data['error'] = 'bad_image'
                
            else:
                front_data['error'] = 'bad_image'
            
            return front_data

        if country == 'SAU':
            print("working on SAU")
            front_data = {
                'error': ''
            }
            is_colored1 = self.is_colored(front_id)
            if is_colored1:
                try:
                    processed_front_id = self.process_image(front_id)
                    front_id_text = self.get_ocr_results(processed_front_id)
                    front_id_text = front_id_text[0].description
                    front_id_text_list= front_id_text.split('\n')

                    img = self.image_conversion(front_id)
                    image = np.array(img)
                    pil_image = Image.fromarray(image)

                    doc_on_pp_result = document_on_printed_paper(image)

                    with io.BytesIO() as output:
                        pil_image.save(output, format="PNG")
                        image_data = output.getvalue()

                    # saudi id has no logo, set hardcoded value
                    # logo_result = detect_logo_saudi(self.client, image_data)
                    logo_result = 'clear'
                    screenshot_result = detect_screenshot(self.client, front_id)
                    photo_on_screen_result = detect_photo_on_screen(self.client, front_id)

                    front_blurred, front_glare = self.get_blurred_and_glared_for_doc(image)

                    front_face_locations, front_face_encodings = self.load_and_process_image_fr(front_id)

                    front_face_locations_str = json.dumps([tuple(face_loc) for face_loc in front_face_locations])
                    front_face_encodings_str = json.dumps([face_enc.tolist() for face_enc in front_face_encodings])

                    front_data_fields = extract_id_details(front_id_text_list)
                    valid_nationality_result = self.check_nationality_in_iso_list(front_data_fields.get('nationality'))

                    front_data = {
                        'valid_nationality': valid_nationality_result,
                        'front_extracted_data': front_id_text,
                        'front_coloured': True,
                        'front_doc_on_pp': doc_on_pp_result,
                        'front_logo_result': logo_result,
                        'front_screenshot_result': screenshot_result,
                        'front_photo_on_screen_result': photo_on_screen_result,
                        'front_blurred': front_blurred, 
                        'front_glare': front_glare,
                        'front_face_locations': front_face_locations_str, 
                        'front_face_encodings': front_face_encodings_str
                    }
                    
                    front_data.update(front_data_fields)

                    non_optional_keys = ["front_face_locations", "front_face_encodings", "id_number", "name", "dob", "expiry_date", "gender", "nationality"]
                    empty_string_keys = [key for key, value in front_data.items() if key in non_optional_keys and value == '']

                    if empty_string_keys:
                        front_data['error'] = 'covered_photo'

                except Exception as e:
                    print(e)
                    front_data['error'] = 'bad_image'
                
            else:
                front_data['error'] = 'bad_image'
            
            return front_data

    
    def extract_back_id_info(self, back_id, country):
        if country=='UAE':
            back_data = {
                'error': ''
            }
            is_colored2 = self.is_colored(back_id)
            if is_colored2:
                # try:
                    processed_back_id = self.process_image(back_id)
                    id_infos= self.get_ocr_results(processed_back_id)
                    text = id_infos[0].description
                    
                     # This pattern is present on the front. If we find this we return empty strings with error code
                    pattern1 = r'Resident Identity'
                    pattern2 = r'Identity Card'
                    m = re.search(pattern1, text)
                    n = re.search(pattern2, text)
                    if m or n:
                        back_data["error"] = "not_back_id"
                        return back_data
        
                    original_text = text
                    #print(original_text)
                    
                  
                    patterns = {
                        'id_number': (r'(?:ILARE|IDARE)\s*([\d\s]+)', lambda match: match.group(0).replace(" ", "")[15:30] if match else ''),
                        'card_number': (r'(?:ILARE|IDARE)(\d{1,9})', lambda match: match.group(1) if match else ''),
                        'nationality': (r'([A-Z]+)<<', lambda match: match.group(1) if match else ''),
                        'gender': (r'(?<=\d)[A-Z](?=\d)', lambda match: match.group(0) if match else ''),
                        'dob': (r'(\d+)[MF]', lambda match: self.convert_dob(match.group(1)) if match else ''),
                        'expiry_date': (r'[MF](\d+)', lambda match: self.convert_expiry_date(match.group(1)) if match else ''),
                        'name': (r'(.*[A-Za-z]+<[<]+[A-Za-z].*)', lambda match: match.group(0).replace('<', ' ').strip() if match else ''),
                        'first_name': (r'<<([^<]+)', lambda match: match.group(0).replace("<", "") if match else ''),
                        'last_name': (r'([^<]+)(?=<<)', lambda match: match.group(0).replace("<", "") if match else ''),
                        # 'occupation': (r'Occupation:\s*([-\w\s.]+)', lambda match: match.group(1).strip().split('\n', 1)[0] if match else '', re.IGNORECASE),
                        # 'employer': (r'Employer:\s*([\w\s.]+)', lambda match: match.group(1).strip().split('\n', 1)[0] if match else '', re.IGNORECASE),
                        'issuing_place': (r'Issuing Place:\s*([\w\s.]+)', lambda match: match.group(1).strip().split('\n', 1)[0] if match else '', re.IGNORECASE)
                    }

                    mrz_pattern = r'(ILARE.*\n*.*\n*.*\n*.*|IDARE.*\n*.*\n*.*\n*.*)'


                    mrz = re.findall(mrz_pattern, original_text.replace(" ","").strip(), re.MULTILINE)
                    
                    mrz_list=mrz[0].replace(" ", "").split("\n", 3)
                    try: 
                        mrz1=mrz_list[0]

                    except:
                        mrz1=''
                    try:
                        mrz2=mrz_list[1]
                    except:
                        mrz2=''
                    try:
                        mrz3=mrz_list[2]
                    except:
                        mrz3=''
                    
                    mrz1_keys = ['id_number', 'card_number']
                    mrz2_keys = ['nationality', 'gender', 'dob', 'expiry_date']
                    mrz3_keys = ['name', 'first_name', 'last_name']
                    
                    for key, value in patterns.items():
                        pattern = value[0]
                        transform_func = value[1]
                        flags = value[2] if len(value) > 2 else 0

                        text = original_text
                        if key in mrz1_keys:
                            text = mrz1
                        if key in mrz2_keys:
                            text = mrz2
                        if key in mrz3_keys:
                            text = mrz3

                        match = re.search(pattern, text, flags)
                        back_data[key] = transform_func(match) if match else ''
                    
                    ## extracting occupation and employer
                    occ_word='Occupation'
                    occ=''
                    emp_word='Employer'
                    emp=''
                    try:
                        lines=original_text.split('\n')  
                        for line in lines:
                            if occ_word in line:
                                start_index = line.find(occ_word)
                                end_index = start_index + len(occ_word) 
                                occ = line[end_index:]
                                occ = self.clean_string(occ)

                            if emp_word in line:
                                start_index1 = line.find(emp_word)
                                end_index1 = start_index1 + len(emp_word) 
                                emp = line[end_index1:]
                                emp = self.clean_string(emp)
                    except:
                        occ = ''
                        emp = ''

                    ### new rule
                    if len(str(back_data['id_number']))!=15:
                        back_data['id_number']=''
                    
                    ### new rule
                    if len(str(back_data['card_number']))!=9:
                        back_data['card_number']=''
                    

                    current_module = sys.modules[__name__] 

                    for key in ['dob','expiry_date','gender','card_number','name','nationality']:
                        #if not back_data[key] and key not in ['occupation', 'employer', 'first_name', 'last_name', 'issuing_place', 'error']:
                        
                        if not back_data[key]:
                                transform_func_new = getattr(current_module,f'func_{key}')
                                back_data[key] = transform_func_new(original_text)

                    for key in ['dob','expiry_date']:
                         if not back_data[key]:
                             transform_func_new = getattr(current_module,f'find_{key}')
                             back_data[key] = transform_func_new(original_text,back_data['mrz2'])
                    
                    if not back_data['id_number']:
                        back_data['id_number']=func_id_number(original_text,back_data['dob'])

                    if is_valid_and_not_expired(back_data.get('expiry_date')) == 'consider':
                        back_data['error'] = 'expired_document'
                    

                    valid_nationality_result = self.check_nationality_in_iso_list(back_data.get('nationality'))

                    img = self.image_conversion(back_id)
                    image = np.array(img)
                    pil_image = Image.fromarray(image)
                    
                    doc_on_pp_result = document_on_printed_paper(image)
                    screenshot_result = detect_screenshot(self.client, back_id)
                    photo_on_screen_result = detect_photo_on_screen(self.client, back_id)
                    back_blurred, back_glare = self.get_blurred_and_glared_for_doc(image)

                    back_data_update = {
                        'valid_nationality': valid_nationality_result,
                        'back_extracted_data': original_text,
                        'back_coloured': True,
                        'mrz': mrz,
                        'mrz1': mrz1,
                        'mrz2': mrz2,
                        'mrz3': mrz3,
                        'occupation': occ,
                        'employer': emp,
                        'doc_on_pp': doc_on_pp_result,
                        'screenshot_result': screenshot_result,
                        'photo_on_screen_result': photo_on_screen_result,
                        'back_blurred': back_blurred, 
                        'back_glare': back_glare
                    }

                    back_data.update(back_data_update)

                    non_optional_keys = ["id_number", "card_number", "name", "dob", "expiry_date", "gender", "nationality", "mrz", "mrz1", "mrz2", "mrz3"]
                    empty_string_keys = [key for key, value in back_data.items() if key in non_optional_keys and value == '']

            
                    if empty_string_keys:
                        back_data['error'] = 'covered_photo'

                  
                # except:
                #     back_data['error'] = 'bad_image'

            else:
                back_data['error'] = 'bad_image'

            return back_data

    def exract_passport_info(self, passport, nationality):
        if nationality.upper() == 'RUS':
            processed_passport = self.process_image(passport)
            passport_text = self.get_ocr_results(processed_passport)
            passport_text = passport_text[0].description

            passport_details = {}

            patterns = {
                'passport_given_name': (r'Имя Given names\n(.*?)/', lambda match: self.translator.translate(match.group(1), src='ru', dest='en').text if match else ''),
                'passport_surname': (r'RUS(.*?)<<(.*?)<.*', lambda match: match.group(1) if match else ''),
                'passport_number': (r"(\d{7})", lambda match: match.group(1) if match else ''),
                'passport_date_of_birth': (r'(\d+)[MF]', lambda match: self.convert_dob(match.group(1)) if match else ''),
                'passport_date_of_expiry': (r'[MF](\d+)', lambda match: self.convert_expiry_date(match.group(1)) if match else ''),
                'passport_gender': (r'(\d)([A-Za-z])(\d)', lambda match: match.group(2) if match else '')
            }

            mrz1_pattern = r'([A-Z<]+)<<([A-Z<]+)<<([\dA-Z<]+)'
            mrz2_pattern = r'(\d{10}[A-Z]{3}\d{7}[\dA-Z<]+)'

            mrz1_matches = re.findall(mrz1_pattern, passport_text)
            mrz2_matches = re.findall(mrz2_pattern, passport_text)

            if mrz1_matches:
                mrz1 = ' '.join(mrz1_matches[0])
            else:
                mrz1 = ''

            if mrz2_matches:
                mrz2 = mrz2_matches[0]
            else:
                mrz2 = ''

            mrz1_keys = ['passport_surname']
            mrz2_keys = ['passport_date_of_birth', 'passport_date_of_expiry', 'passport_gender']

            for key, value in patterns.items():
                pattern = value[0]
                transform_func = value[1]

                text = passport_text
                if key in mrz1_keys:
                    text = mrz1
                if key in mrz2_keys:
                    text = mrz2

                match = re.search(pattern, text)
                passport_details[key] = transform_func(match) if match else ''

            return passport_details

    # report_names = ["document", "facial_similarity_video"]

    def extract_ocr_info(self, data, video, country, report_names, face_match_threshold=0.60):
        document_report = {}
        facial_report = {}

        colour_picture = 'consider'
        if data.get('front_coloured') and data.get('back_coloured'):
            colour_picture = 'clear'

        blurred = 'clear'
        if data.get('front_blurred')=='consider' or data.get('back_blurred')=='consider':
            blurred = 'consider'
        
        glare = 'clear'
        if data.get('front_glare')=='consider' or data.get('back_glare')=='consider':
            glare = 'consider'

        missing_fields = 'clear'
        if data.get('front_missing_fields') or data.get('back_missing_fields'):
            missing_fields = 'consider'

        if video:
            face_loc = json.loads(data.get('front_face_locations'))
            front_face_locations = tuple(face_loc)
            front_face_encodings = np.array(json.loads(data.get('front_face_encodings')))

            data['front_face_locations'] = front_face_locations
            data['front_face_encodings'] = front_face_encodings

            selfie = data.get('selfie')
            similarity = self.extract_face_and_compute_similarity(selfie, front_face_locations, front_face_encodings)
            
        else:
            selfie = None
            similarity = 0

        # front_face_locations, front_face_encodings = data.get('front_face_locations'), data.get('front_face_encodings')
        # processed_selfie = self.process_image(selfie)
        if country == 'SAU':
            back_id_text = ''
        else:
            back_id_text = data.get('back_extracted_data')

        if 'document' in report_names:
            document_report = form_final_data_document_report(data, data.get('front_extracted_data'), back_id_text, country, colour_picture, selfie, similarity, blurred, glare, missing_fields, face_match_threshold)

        if 'facial_similarity_video' in report_names:
            if video:
                liveness_result = self.check_for_liveness(similarity, video, face_match_threshold)
            else:
                liveness_result = None, None

            facial_report = form_final_facial_similarity_report(data, selfie, similarity, liveness_result, face_match_threshold, country)

        return document_report, facial_report
    
