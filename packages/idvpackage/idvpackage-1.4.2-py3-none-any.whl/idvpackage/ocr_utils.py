from datetime import datetime
import re
import cv2
import numpy as np
from google.cloud import vision_v1
from idvpackage.constants import *
import pkg_resources
from PIL import Image
import base64
import io
from rapidfuzz import fuzz

def create_final_result(dictionary):
    result = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            sub_result = create_final_result(value)
            if sub_result == 'consider':
                return 'consider'
            elif sub_result == 'clear':
                result = 'clear'
        elif value in ['clear', 'consider', ""]:
            if value == 'consider':
                return 'consider'
            elif result != 'clear':
                result = value
    return result

def create_sub_result(document_report):
    sub_result = 'clear'

    digital_document = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("digital_document")
    corner_removed = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("corner_removed")
    watermarks_digital_text_overlay = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("watermarks_digital_text_overlay")
    obscured_security_features = document_report["breakdown"]["image_integrity"]["breakdown"]["conclusive_document_quality"]["properties"].get("obscured_security_features")
    screenshot = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("screenshot")
    document_on_printed_paper = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("document_on_printed_paper")
    photo_of_screen = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("photo_of_screen")
    scan = document_report["breakdown"]["visual_authenticity"]["breakdown"]["original_document_present"]["properties"].get("scan")

    consider_caution_count = sum(value == 'consider' for value in [digital_document, corner_removed, watermarks_digital_text_overlay, obscured_security_features, screenshot, document_on_printed_paper, photo_of_screen, scan])
    
    data_consistency = document_report["breakdown"]["data_consistency"]["result"]
    data_comparison = document_report["breakdown"]["data_comparison"]["result"]

    if data_consistency == 'consider' or data_comparison == 'consider':
        sub_result = 'caution'

    if consider_caution_count >= 2:
        sub_result = 'suspected'

    return sub_result

def age_validation(dob, age_threshold=18):
    age_val = {
        "breakdown": {
            "minimum_accepted_age": {
            "properties": {},
            "result": ""
            }
        },
        "result": ""
        }
    
    try:
        dob_date = datetime.strptime(dob, "%d/%m/%Y")
    except:
        dob_date = ''

    if dob_date:
        current_date = datetime.now()

        age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))

        if age>=age_threshold:
            age_val["breakdown"]["minimum_accepted_age"]["result"] = "clear"
            age_val["result"] = "clear"
        else:
            age_val["breakdown"]["minimum_accepted_age"]["result"] = "consider"
            age_val["result"] = "consider"
    else:
        age_val["breakdown"]["minimum_accepted_age"]["result"] = "consider"
        age_val["result"] = "consider"

    return age_val
    
def created_at():
    current_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    return current_datetime

def is_valid_and_not_expired(expiry_date):
    try:
        parsed_date = datetime.strptime(expiry_date, "%d/%m/%Y")
        current_date = datetime.now()
        
        if parsed_date < current_date:
            return 'consider'
        return 'clear'
    
    except:
        return 'consider'

def identify_document_type(text):
    text = text.upper()
    emirates_id_pattern = r'\b(ILARE\w*|IDARE\w*|RESIDENT IDENTITY)\b'
    iqama_id_pattern = r'KINGDOM OF SAUDI ARABIA|RESIDENT IDENTITY|MINISTRY OF INTERIOR'
    passport_pattern = r'\b(PASSPORT|PPT)\b'
    driver_license_pattern = r'\b(DRIVER|LICENSE|DL)\b'
    
    if re.search(emirates_id_pattern, text):
        return "EID"

    if re.search(passport_pattern, text):
        return "PASSPORT"

    if re.search(driver_license_pattern, text):
        return "DL"

    return "Unknown"

def identify_front_id(text):
    front_id_keywords = ['Resident Identity', 'United arab emirates', 'federal authority for identity', 'ID Number', 'Kingdom of saudi arabia', 'ministry of interior']
    pattern = '|'.join(map(re.escape, front_id_keywords))
    
    if re.search(pattern, text, re.IGNORECASE):
        return True
    else:
        return False

def identify_back_id(text):
    back_id_keywords = ['ILARE', 'IDARE', 'Signature']
    pattern = '|'.join(map(re.escape, back_id_keywords))
    
    if re.search(pattern, text, re.IGNORECASE):
        return True
    else:
        return False

# def document_on_printed_paper(image, edge_threshold=100, contour_area_threshold=5000, paper_texture_threshold=0.008):
#     image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     image_blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
#     image_edges = cv2.Canny(image_blurred, edge_threshold, edge_threshold * 2)

#     image_contours, _ = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     image_paper_edges = [contour for contour in image_contours if cv2.contourArea(contour) > contour_area_threshold]

#     paper_edge_ratio = len(image_paper_edges) / max(len(image_contours), 1)
#     print(f"paper edge ratio: {paper_edge_ratio}")

#     # Determine if the image contains a printed paper texture
#     if paper_edge_ratio >= paper_texture_threshold:
#         return 'consider'
#     else:
#         return 'clear'
#     # print(front_paper_edges, back_paper_edges)
    
#     # if len(image_paper_edges) > 0:
#     #     return 'consider'
#     # else:
#     #     return 'clear'

def document_on_printed_paper(image, block_size=11, c_value=2, texture_threshold=0.1, contour_area_threshold=5000):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value)
    image_contours, _ = cv2.findContours(image_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter out small noise contours
    image_paper_edges = [contour for contour in image_contours if cv2.contourArea(contour) > contour_area_threshold]

    # Calculate the percentage of paper texture in the image
    texture_ratio = len(image_paper_edges) / max(len(image_contours), 1)

    # Determine if the image contains a printed paper texture
    if texture_ratio >= texture_threshold:
        return 'consider'
    else:
        return 'clear'
    
def detect_logo(client, input_image_content):
    reference_logo_path = pkg_resources.resource_filename('idvpackage', 'emirates_id_logo.jpeg')
    
    with open(reference_logo_path, 'rb') as logo_file:
        reference_image_content = logo_file.read()

    reference_image = vision_v1.types.Image(content=reference_image_content)
    input_image = vision_v1.types.Image(content=input_image_content)

    reference_response = client.logo_detection(image=reference_image)
    input_response = client.logo_detection(image=input_image)

    reference_logos = reference_response.logo_annotations
    input_logos = input_response.logo_annotations

    for reference_logo in reference_logos:
        for input_logo in input_logos:
            if reference_logo.description.lower() == input_logo.description.lower():
                return 'clear'

    return 'consider'

def detect_logo_saudi(client, input_image):
    reference_logo_path = pkg_resources.resource_filename('idvpackage', 'sau_id_logo.png')
    
    with open(reference_logo_path, 'rb') as logo_file:
        reference_image_content = logo_file.read()

    reference_image = vision_v1.types.Image(content=reference_image_content)
    input_image = vision_v1.types.Image(content=input_image)

    reference_response = client.logo_detection(image=reference_image)
    input_response = client.logo_detection(image=input_image)

    reference_logos = reference_response.logo_annotations
    input_logos = input_response.logo_annotations

    for reference_logo in reference_logos:
        for input_logo in input_logos:
            if reference_logo.description.lower() == input_logo.description.lower():
                return 'clear'

    return 'consider'


def perform_feature_matching(image, template_image_path):
    template_image = cv2.imread(template_image_path, cv2.IMREAD_COLOR)

    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(template_image, None)
    kp2, des2 = sift.detectAndCompute(image, None)

    if len(kp1) == 0 or len(kp2) == 0:
        return 0.0 
    
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    similarity_score = len(good_matches) / len(kp1)

    return similarity_score

# part of detecting screenshot - checks for time values seen on phone
def extract_time_values(text_annotations):
    time_values = []
    for annotation in text_annotations:
        text = annotation.description
        time_matches = re.findall(r'\d{1,2}:\d{2}', text)
        time_values.extend(time_matches)
    return time_values

def detect_screenshot(client, image):
    icons = 0
    battery_value_and_time = 0

    similarity_threshold = 0.45

    for filename in pkg_resources.resource_listdir('idvpackage', 'icons'):
        if filename.endswith('.png'):
            icon_path = pkg_resources.resource_filename('idvpackage', f'icons/{filename}')
            image_data = np.frombuffer(base64.b64decode(image), dtype=np.uint8)

            front_similarity_score = perform_feature_matching(image_data, icon_path)
            if front_similarity_score >= similarity_threshold:
                icons+=1

    image_data = vision_v1.Image(content=base64.b64decode(image))

    image_response = client.text_detection(image=image_data)

    image_text_annotations = image_response.text_annotations

    image_time_values = extract_time_values(image_text_annotations)

    if image_time_values:
        battery_value_and_time+=1

    if icons or battery_value_and_time:
        return 'consider'
    else:
        return 'clear'

def detect_photo_on_screen(client, image):
    flag = 'clear'

    image_data = vision_v1.Image(content=base64.b64decode(image))
    
    image_response = client.label_detection(image=image_data)
    image_labels = image_response.label_annotations

    confidence_threshold = 0.70  

    keywords = ['mobile phone', "mobile device", "portable communications device", 'communication device', 'smartphone', 'cell phone', "hand", 'touchscreen', 'laptop', 'notebook', 'computer', 'screen', 'finger', 'thumb', 'gadget']

    for label in image_labels:
        description = label.description.lower()
        confidence = label.score
        if confidence >= confidence_threshold:
            match = any(fuzz.ratio(description, keyword.lower()) >= 90 for keyword in keywords)
            if match:
                return 'consider'

    return flag

def fuzzy_match_fields(field1, field2, threshold=70):
    similarity = fuzz.partial_ratio(field1, field2)
    return similarity >= threshold

## for data comparison, accept data from dev and match with data extracted from id
def data_comparison_check(data):
    data_comparison = DATA_COMPARISON

    user_data = data.get('manual_input', '')
    if user_data:
        if not data.get('dob') == user_data.get('dob'):
            data_comparison['breakdown']['date_of_birth']['result'] = 'consider'
        
        if not fuzzy_match_fields(data.get('first_name').lower(),user_data.get('first_name').lower()):
            data_comparison['breakdown']['first_name']['result'] = 'consider'
        
        if not fuzzy_match_fields(data.get('gender').lower(),user_data.get('gender').lower()):
            data_comparison['breakdown']['gender']['result'] = 'consider'

        if not fuzzy_match_fields(data.get('last_name').lower(),user_data.get('last_name').lower()):
            data_comparison['breakdown']['last_name']['result'] = 'consider'

    result = create_final_result(data_comparison)    
    data_comparison['result'] = result

    return data_comparison

def data_consistency_check(data, front_id_text, back_id_text, country):
    data_consistency = DATA_CONSISTENCY

    passport_data = data.get('passport')
    if passport_data:
        print(f"fuzzy match data: ")
        if not data.get('dob') == passport_data.get('passport_date_of_birth'):
            data_consistency['breakdown']['date_of_birth']['result'] = 'consider'
        
        if not fuzzy_match_fields(data.get('first_name').lower(),passport_data.get('passport_given_name').lower()):
            data_consistency['breakdown']['first_name']['result'] = 'consider'
        
        if not fuzzy_match_fields(data.get('gender').lower(),passport_data.get('passport_gender').lower()):
            data_consistency['breakdown']['gender']['result'] = 'consider'

        if not fuzzy_match_fields(data.get('last_name').lower(),passport_data.get('passport_surname').lower()):
            data_consistency['breakdown']['last_name']['result'] = 'consider'

    #### For data consistency compare data from different sources, like id and passport. 
    #### so the dob from id should match with dob extracted from passport

    if country == 'UAE':
        doc_type1 = identify_document_type(front_id_text)
        doc_type2 = identify_document_type(back_id_text)
        if doc_type1 == 'EID' or doc_type2=='EID':
            data_consistency['breakdown']['document_type']['result'] = 'clear'
        else:
            data_consistency['breakdown']['document_type']['result'] = 'consider'

    if country == 'SAU':
        doc_type1 = identify_front_id(front_id_text)
        if doc_type1:
            data_consistency['breakdown']['document_type']['result'] = 'clear'
        else:
            data_consistency['breakdown']['document_type']['result'] = 'consider'
    
    result = create_final_result(data_consistency)    
    data_consistency['result'] = result

    return data_consistency

def data_validation_check(data, country):
    data_validation = DATA_VALIDATION

    try:
        dob = data.get('dob')
        parsed_date = datetime.strptime(dob, "%d/%m/%Y")
        data_validation["breakdown"]['date_of_birth']["result"] = 'clear'
    except:
        data_validation["breakdown"]['date_of_birth']["result"] = 'consider'

    try:
        doe = data.get('expiry_date')
        parsed_date = datetime.strptime(doe, "%d/%m/%Y")
        data_validation["breakdown"]['expiry_date']["result"] = 'clear'
    except:
        data_validation["breakdown"]['expiry_date']["result"] = 'consider'

    gender = data.get('gender')
    if gender.isalpha() and len(gender) == 1:
        data_validation["breakdown"]['gender']["result"] = 'clear'
    else:
        data_validation["breakdown"]['gender']["result"] = 'consider'
    
    data_validation['breakdown']['valid_nationality']["result"] = data.get('valid_nationality')

    if country == 'UAE':
        doc_no = data.get('card_number', '')
        if len(doc_no)==9:
            data_validation["breakdown"]['document_numbers']["result"] = 'clear'
        else:
            data_validation["breakdown"]['document_numbers']["result"] = 'consider'

        doe = data.get('expiry_date')
        expiry_result = is_valid_and_not_expired(doe)
        data_validation['breakdown']['document_expiration']["result"] = expiry_result

        mrz = data.get('mrz', '')
        mrz1 = data.get('mrz1', '')
        mrz2 = data.get('mrz2', '')
        mrz3 = data.get('mrz3', '')
        if len(mrz) == 1 and mrz1 and mrz2 and mrz3:
            data_validation["breakdown"]['mrz']["result"] = 'clear'
        else:
            data_validation["breakdown"]['mrz']["result"] = 'consider'
    
    result = create_final_result(data_validation)
    data_validation['result'] = result

    # if data_validation["breakdown"]['date_of_birth']["result"]=='clear' and data_validation["breakdown"]['expiry_date']["result"]=='clear' and data_validation["breakdown"]['gender']["result"]=='clear' and data_validation["breakdown"]['mrz']["result"]=='clear':
    #     data_validation['result'] = 'clear'

    return data_validation

## pending
def image_integrity_check(data, front_id_text, back_id_text, coloured, blurred, glare, missing_fields, country):
    image_integrity = IMAGE_INTEGRITY

    image_integrity['breakdown']['colour_picture']['result'] = coloured
    image_integrity['breakdown']['conclusive_document_quality']['properties']['corner_removed'] = is_valid_and_not_expired(data.get('expiry_date'))
    image_integrity['breakdown']['conclusive_document_quality']['properties']['abnormal_document_features'] = blurred
    image_integrity['breakdown']['image_quality']['properties']['blurred_photo'] = blurred
    image_integrity['breakdown']['image_quality']['properties']['covered_photo'] = missing_fields
    image_integrity['breakdown']['image_quality']['properties']['cut_off_document'] = missing_fields
    image_integrity['breakdown']['image_quality']['properties']['glare_on_photo'] = glare
    image_integrity['breakdown']['image_quality']['properties']['other_photo_issue'] =  missing_fields

    f_result = identify_front_id(front_id_text)
    front_doc_on_pp = data.get('front_doc_on_pp')

    if country == 'UAE':
        b_result = identify_back_id(back_id_text)

        if back_id_text and b_result:
            image_integrity['breakdown']['conclusive_document_quality']['properties']['missing_back'] = 'clear'
        else:
            image_integrity['breakdown']['conclusive_document_quality']['properties']['missing_back'] = 'consider'

        if f_result and b_result:
            image_integrity['breakdown']['supported_document']['result'] = 'clear'
        else:
            image_integrity['breakdown']['supported_document']['result'] = 'consider'
    
        back_doc_on_pp = data.get('doc_on_pp')
        if front_doc_on_pp == 'consider' or back_doc_on_pp == 'consider':
            image_integrity['breakdown']['conclusive_document_quality']['properties']['digital_document'] = 'consider'

    if country == 'SAU':
        if f_result:
            image_integrity['breakdown']['supported_document']['result'] = 'clear'
        else:
            image_integrity['breakdown']['supported_document']['result'] = 'consider'
        
        image_integrity['breakdown']['conclusive_document_quality']['properties']['digital_document'] = front_doc_on_pp

    image_integrity['breakdown']['conclusive_document_quality']['properties']['watermarks_digital_text_overlay'] = data.get('front_logo_result')
    # image_integrity['breakdown']['image_quality']['properties']['blurred_photo'] = blurred
    # image_integrity['breakdown']['image_quality']['properties']['glare_on_photo'] = glare

    image_quality_result = create_final_result(image_integrity['breakdown']['image_quality'])
    conclusive_document_quality_result = create_final_result(image_integrity['breakdown']['conclusive_document_quality'])
    colour_picture_result = image_integrity['breakdown']['colour_picture']['result']
    supported_documents_result = image_integrity['breakdown']['supported_document']['result']

    if image_quality_result == 'consider' or conclusive_document_quality_result == 'consider' or colour_picture_result == 'consider' or supported_documents_result == 'consider':
        image_integrity['result'] = 'consider'

    return image_integrity

def visual_authenticity_check(data, front_id_text, back_id_text, selfie, facial_similarity, face_match_threshold, country):
    print(f"\nSimilarity: {facial_similarity}\n")
    visual_authenticity = VISUAL_AUTHENTICITY

    if np.any(selfie):
        if facial_similarity>=face_match_threshold:
            visual_authenticity['breakdown']['face_detection'] = 'clear'
            visual_authenticity['breakdown']['security_features'] = 'clear'
        else:
            visual_authenticity['breakdown']['face_detection'] = 'consider'
            visual_authenticity['breakdown']['security_features'] = 'consider'
    else:
        visual_authenticity['breakdown']['face_detection'] = ''
        visual_authenticity['breakdown']['security_features'] = ''
    
    doc_type1 = identify_document_type(front_id_text)
    front_doc_on_pp = data.get('front_doc_on_pp')
    front_screenshot = data.get('front_screenshot_result')
    front_photo_on_screen_result = data.get('front_photo_on_screen_result')

    if country == 'UAE':
        doc_type2 = identify_document_type(back_id_text)
        if doc_type1 == 'EID' and doc_type2 == 'EID':
            visual_authenticity['breakdown']['original_document_present']['properties']['scan'] = 'clear'
        else:
            visual_authenticity['breakdown']['original_document_present']['properties']['scan'] = 'consider'
    
        back_doc_on_pp = data.get('doc_on_pp')
        if front_doc_on_pp == 'consider' or back_doc_on_pp == 'consider':
            visual_authenticity['breakdown']['original_document_present']['properties']['document_on_printed_paper'] = 'consider'

        back_screenshot = data.get('screenshot_result')
        if front_screenshot == 'consider' or back_screenshot == 'consider':
            visual_authenticity['breakdown']['original_document_present']['properties']['screenshot'] = 'consider'

        photo_on_screen_result = data.get('photo_on_screen_result')
        if front_photo_on_screen_result == 'consider' or photo_on_screen_result == 'consider':
            visual_authenticity['breakdown']['original_document_present']['properties']['photo_of_screen'] = 'consider'

    if country == 'SAU':
        if identify_front_id(front_id_text):
            visual_authenticity['breakdown']['original_document_present']['properties']['scan'] = 'clear'
        else:
            visual_authenticity['breakdown']['original_document_present']['properties']['scan'] = 'consider'
    
        visual_authenticity['breakdown']['original_document_present']['properties']['document_on_printed_paper'] = front_doc_on_pp
        visual_authenticity['breakdown']['original_document_present']['properties']['screenshot'] = front_screenshot
        visual_authenticity['breakdown']['original_document_present']['properties']['photo_of_screen'] = front_photo_on_screen_result


    final_result = create_final_result(visual_authenticity)
    visual_authenticity['result'] = final_result

    return visual_authenticity

def main_details(data):
    main_properties = MAIN_DATA

    try:
        main_properties['date_of_birth'] = data.get('dob')
        main_properties['date_of_expiry'] = data.get('expiry_date', '')

        if data.get('card_number'):
            card_data_t = {
            "type": "type",
            "value": "document_number"
            }

            card_data_v = {
                "type": "value",
                "value": data['card_number']
            }

            main_properties['document_numbers'].append(card_data_t)
            main_properties['document_numbers'].append(card_data_v)

        if data.get('id_number'):
            id_data_t = {
                        "type": "type",
                        "value": "personal_number"
                    }
            id_data_v = {
                        "type": "value",
                        "value": data['id_number']
                    }
                
            main_properties['document_numbers'].append(id_data_t) 
            main_properties['document_numbers'].append(id_data_v) 
        
        main_properties['document_type'] = 'national_identity_card'
        main_properties['name'] = data.get('name')
        main_properties['first_name'] = data.get('first_name', '')
        main_properties['gender'] = data.get('gender', '')
        main_properties['issuing_country'] = data.get('issuing_place', '')
        main_properties['last_name'] = data.get('last_name', '')
        main_properties['mrz_line1'] = data.get('mrz1', '')
        main_properties['mrz_line2'] = data.get('mrz2', '')
        main_properties['mrz_line3'] = data.get('mrz3', '')
        main_properties['nationality'] = data.get('nationality')

    except:
        main_properties

    return main_properties    

def form_final_data_document_report(data, front_id_text, back_id_text, country, coloured, selfie, facial_similarity, blurred, glare, missing_fields, face_match_threshold):
    try:
        document_report = {
            ## pending - to be filled by dev
            "_id": "",
            "breakdown": {
                "age_validation": age_validation(data.get('dob')),
                "compromised_document": {
                    "result": "clear"
                    },
                "data_comparison": data_comparison_check(data),
                "data_consistency": data_consistency_check(data, front_id_text, back_id_text, country),
                "data_validation": data_validation_check(data, country),
                "image_integrity": image_integrity_check(data, front_id_text, back_id_text, coloured, blurred, glare, missing_fields, country),
                "issuing_authority": {
                "breakdown": {
                    "nfc_active_authentication": {
                    "properties": {}
                    },
                    "nfc_passive_authentication": {
                    "properties": {}
                    }
                }
                },
                "police_record": {},
                "visual_authenticity": visual_authenticity_check(data, front_id_text, back_id_text, selfie, facial_similarity, face_match_threshold, country)
            },
            ## pending - to be filled by dev
            "check_id": "", 
            "created_at": created_at(),
            "documents": [
                {
                ## pending - id value in table stored in db for front id - to be filled by dev
                "id": ""
                },
                {
                ## pending - id value in table stored in db for front id - to be filled by dev
                "id": ""
                }
            ],
            # to be filled by dev
            "href": "",
            "name": "document",
            "properties": main_details(data),
            "result": "",
            "status": "complete",
            "sub_result": ""
        }
        
        final_result = create_final_result(document_report)
        document_report['result'] = final_result
        
        sub_result = create_sub_result(document_report)
        document_report['sub_result'] = sub_result

        return document_report
    
    except Exception as e:
        print(e)
        return {}

def form_final_facial_similarity_report(data, selfie, facial_similarity, liveness_result, face_match_threshold, country):
    facial_report = FACIAL_REPORT
    
    facial_report['created_at'] = created_at()
    
    facial_report['breakdown']['face_comparison']['breakdown']['face_match']['properties']['score'] = facial_similarity

    if not np.any(selfie):
        facial_report['breakdown']['face_comparison']['breakdown']['face_match']['result'] = ''
        facial_report['breakdown']['face_comparison']['result'] = ''
        facial_report['breakdown']['image_integrity']['breakdown']['face_detected']['result'] = ''
        facial_report['breakdown']['image_integrity']['breakdown']['source_integrity']['result'] = ''

    if np.any(selfie) and facial_similarity >= face_match_threshold:
        facial_report['breakdown']['face_comparison']['breakdown']['face_match']['result'] = 'clear'
        facial_report['breakdown']['face_comparison']['result'] = 'clear'
        facial_report['breakdown']['image_integrity']['breakdown']['face_detected']['result'] = 'clear'
    else:
        facial_report['breakdown']['face_comparison']['breakdown']['face_match']['result']  = 'consider'
        facial_report['breakdown']['face_comparison']['result'] = 'consider'
        facial_report['breakdown']['image_integrity']['breakdown']['face_detected']['result'] = 'consider'

    front_photo_on_screen_result = data.get('front_photo_on_screen_result')

    if country == 'UAE':
        photo_on_screen_result = data.get('photo_on_screen_result')
        if front_photo_on_screen_result == 'consider' or photo_on_screen_result == 'consider':
            facial_report['breakdown']['image_integrity']['breakdown']['source_integrity']['result'] = 'consider'

    if country == 'SAU':
        facial_report['breakdown']['image_integrity']['breakdown']['source_integrity']['result'] = front_photo_on_screen_result

    facial_report['breakdown']['visual_authenticity']['breakdown']['spoofing_detection']['properties']['score'] = facial_similarity

    if liveness_result == 'consider':
        facial_report['breakdown']['visual_authenticity']['breakdown']['liveness_detected']['result'] = 'consider'
        facial_report['breakdown']['visual_authenticity']['breakdown']['spoofing_detection']['result'] = 'consider'
        facial_report['breakdown']['visual_authenticity']['result'] = 'consider'
    elif liveness_result == None:
        facial_report['breakdown']['visual_authenticity']['breakdown']['liveness_detected']['result'] = ''
        facial_report['breakdown']['visual_authenticity']['breakdown']['spoofing_detection']['properties']['score'] = ''
        facial_report['breakdown']['visual_authenticity']['breakdown']['spoofing_detection']['result'] = ''

    # if np.any(selfie) and liveness_result:
    visual_authenticity_final_result = create_final_result(facial_report['breakdown']['visual_authenticity'])
    facial_report['breakdown']['visual_authenticity']['result'] = visual_authenticity_final_result

    image_integrity_final_result = create_final_result(facial_report['breakdown']['image_integrity'])
    facial_report['breakdown']['image_integrity']['result'] = image_integrity_final_result

    complete_final_result = create_final_result(facial_report['breakdown'])
    facial_report['result'] = complete_final_result
    facial_report['sub_result'] = complete_final_result

    return facial_report
