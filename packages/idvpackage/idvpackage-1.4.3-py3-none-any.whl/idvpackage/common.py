import re
from datetime import datetime
from itertools import permutations

def func_gender( extract):
    extract_no_space = extract.replace(' ','')
    try:
        pattern = r'\sM|F'
        m = re.search(pattern, extract)
        sex = m.group(0)[-1]
    except:
        pattern = r'\d{3}(?:M|F)\d'
        m = re.findall(pattern, extract_no_space)
        if len(m) != 0:
            sex = m[0][3:4]
        else:
            sex = ''

    return sex

def func_common_dates(  extract_no_space):
    dob = ''
    expiry_date = ''
    try:
        matches = re.findall(r'\d{2}/\d{2}/\d{4}', extract_no_space)
        y1 = matches[0][-4:]
        y2 = matches[1][-4:]
        if int(y1) < int(y2):
            dob = matches[0]
            expiry_date = matches[1]
        else:
            dob = matches[1]
            expiry_date = matches[0]
    except:
        dob = ''
        expiry_date = ''

    return dob, expiry_date

def func_dob(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if dob == '':  
        match_dob = re.findall(r'\d{7}(?:M|F)\d', extract_no_space)
        for i in match_dob:
            print(i)
            raw_dob = i[0:6]
            print(raw_dob)
            year = str(datetime.today().year)[2:4]
            temp = '19'
            if int(raw_dob[0:2]) > int(year):
                temp = '19'
            else:
                temp = '20'      
            dob = raw_dob[4:6]+'/'+raw_dob[2:4]+'/'+temp+raw_dob[0:2]
            try:
                dt_obj = datetime.strptime(dob, '%d/%m/%Y')
                break
            except:
                print(f'invalid date {dob}')
                dob = ''
    return dob

def func_expiry_date(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if expiry_date == '':
        match_doe = re.findall(r'\d{7}[A-Z]{2,3}', extract_no_space) 
        for i in match_doe:
         
            raw_doe = i[0:6]
            print(raw_doe)
            expiry_date = raw_doe[4:6]+'/'+raw_doe[2:4]+'/20'+raw_doe[0:2]
            try:
                dt_obj = datetime.strptime(expiry_date, '%d/%m/%Y')
                break
            except:
   
                expiry_date = ''

    return expiry_date


def extract_first_9_digits(string_input):
    match = re.search(r'\b\d{9}\b', string_input)
    if match:
        sequence = match.group(0)
        return sequence
    else:
        return ""

def func_card_number(  extract):
    extract_no_space = extract.replace(' ','')
    try:
        card_number = re.search(r'\d{9}', extract_no_space).group()
    except:
        card_number=  extract_first_9_digits(extract_no_space)

    return card_number

def func_name(  extract):
    bio_data = extract[-40:]
    breakup = bio_data.split('\n')
    if len(breakup) == 2:
        name_extract = breakup.pop(0)
    else:
        country_extract = breakup.pop(0).replace(" ","")
        name_extract = breakup.pop(0)

# Check the alphanumeric nature of name_extract
    if not name_extract.isupper():
        name_extract = breakup.pop(0)
    
    try:
        name = name_extract.replace("<", " ").replace(">", " ").replace(".", " ").replace(":", " ").replace('«','').strip()
        name = ' '.join(name.split())
        name = name.replace("0", "O") # special case fix
    except:
        name = ""

    return name

def func_nationality(  extract):
    extract_no_space = extract.replace(' ','')
    try:
        pattern = r'\d{5}[A-Z]{3}|\d{5}[A-Z]{2}'

        m = re.findall(pattern, extract_no_space)
        country = m[len(m)-1].replace("<", "")[5:]
    except:
        country = ""

    if country == '':
        try:
            pattern = r'\d{2}[a-z][A-Z]{2}'

            m = re.findall(pattern, extract_no_space)
            country = m[len(m)-1].replace("<", "")[2:].upper()
        except:
            country = ""

    return country

def clean_string(input_string):
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
    
def func_id_number(extract,dob):
        
    try:
        p = "784" + "\d{12}"
        id_re = re.search(p, clean_string(extract).replace(' ',''))
        id_number = id_re.group()
    except:
        
        try:
            pattern = r'\d{15,}'
            digits = '784'
            matches = re.findall(pattern, clean_string(extract).replace(' ',''))
            input_number = matches[0]
            dob=dob[-4:]
            id_number='784'+dob+find_and_slice_number(input_number, digits)[:8]
            
        except:
            id_number = ''

    return id_number


# #year = dob[-4:]
# p = "784" + "\d{12}"
# id_re = re.search(p, clean_string(data).replace(' ',''))
# id_number = id_re.group()



def convert_to_date(date_str):
    year = '19' + date_str[:2] if int(date_str[:2]) >= 50 else '20' + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:6]
    return f"{day}/{month}/{year}"

def check_valid_date(date_str, format="%d/%m/%Y"):
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False
    

def find_expiry_date(original_text,mrz2):
    
    dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', original_text)
    expiry_date = ''

    if len(dates) == 2:
        
        date1 = datetime.strptime(dates[0], '%d/%m/%Y')
        date2 = datetime.strptime(dates[1], '%d/%m/%Y')
        
        if date2 < date1:
            expiry_date = dates[0]
        elif date2 > date1:
            expiry_date = dates[1]
            
    elif mrz2:
        match_expiry_date = re.search(r'[A-Za-z](\d+)', mrz2)
        if match_expiry_date:
            expiry_date = match_expiry_date.group(1)[:6]
            expiry_date = convert_to_date(expiry_date)
    
            
    if not check_valid_date(expiry_date):
            expiry_date=''
    return expiry_date

def find_dob(original_text,mrz2):
    
     dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', original_text)
     dob = ''
  
     if len(dates) == 2:
            date1 = datetime.strptime(dates[0], '%d/%m/%Y')
            date2 = datetime.strptime(dates[1], '%d/%m/%Y')

            if date2 < date1:
                dob = dates[1]
            elif date2 > date1:
                dob = dates[0] 
                
     elif mrz2:
        match_dob = re.search(r'(\d+)[A-Za-z]', mrz2)
        if match_dob:
            dob = match_dob.group(1)[:6] 
            dob=convert_to_date(dob)
    
     if not check_valid_date(dob):
            dob=''
     return dob

