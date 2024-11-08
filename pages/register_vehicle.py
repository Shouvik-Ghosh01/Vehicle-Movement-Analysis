import streamlit as st
import numpy as np
import cv2
from detect import run
import re
import string
import pandas as pd
from utils import display_heading
from menu import menu

# Dictionary mapping state codes to their corresponding states in India
state_codes = {
    'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CG': 'Chhattisgarh',
    'GA': 'Goa', 'GJ': 'Gujarat', 'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JK': 'Jammu and Kashmir',
    'JH': 'Jharkhand', 'KA': 'Karnataka', 'KL': 'Kerala', 'MP': 'Madhya Pradesh', 'MH': 'Maharashtra',
    'MN': 'Manipur', 'ML': 'Meghalaya', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OD': 'Odisha', 'PB': 'Punjab',
    'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TN': 'Tamil Nadu', 'TS': 'Telangana', 'TR': 'Tripura', 'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand', 'WB': 'West Bengal', 'AN': 'Andaman and Nicobar Islands', 'CH': 'Chandigarh',
    'DN': 'Dadra and Nagar Haveli and Daman and Diu',
    'DL': 'Delhi', 'LD': 'Lakshadweep', 'PY': 'Puducherry'
}


def clean_number_plate(text):
    # Remove special characters from the beginning and end
    cleaned_text = text.strip(string.punctuation + '~' + '|' + '!' + '-' + '_' + '(' + ')' + '{' + '}')
    # Remove special characters except for alphanumeric and spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Remove any extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    if not cleaned_text:
        return cleaned_text  # Return immediately if cleaned_text is empty

    if cleaned_text[0] == 'I':
        cleaned_text = cleaned_text[1::]
    return cleaned_text


def correct_state_code(text):
    if len(text) < 3:
        return "", text
    # Check various possible combinations for a valid state code
    possible_codes = [text[:2], text[1:3], text[0] + text[2]]
    for code in possible_codes:
        if code in state_codes:
            corrected_text = text[:2] + text[2:]  # Only replace the state code part
            return code, corrected_text
    return None, text


def analyze_number_plate(text):
    # Clean the number plate text
    cleaned_text = clean_number_plate(text)
    # Correct the state code
    state_code, corrected_text = correct_state_code(cleaned_text)
    if state_code:
        state = state_codes[state_code]
        # Remove spaces from the corrected text
        corrected_text_without_spaces = corrected_text.replace(" ", "")
        return f"The number plate belongs to {state} with the state code {state_code}.", corrected_text_without_spaces
    else:
        return "The state code could not be identified.", text


def main():
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    menu()
    display_heading()

    st.title('Register Your Vehicle')
    st.markdown('Upload an image to detect and register a vehicle.')

    img_files = st.file_uploader(label="Choose image files",
                                 type=['png', 'jpg', 'jpeg'],
                                 accept_multiple_files=True)

    def create_opencv_image_from_stringio(img_stream, cv2_img_flag=1):
        img_stream.seek(0)
        img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        return cv2.imdecode(img_array, cv2_img_flag)

    # Load authorized vehicles from CSV
    try:
        authorized_vehicles = pd.read_csv('datasets/authorized_vehicles.csv')
    except FileNotFoundError:
        authorized_vehicles = pd.DataFrame(columns=['Plate_Number'])  # Adjust column name here

    for n, img_file_buffer in enumerate(img_files):
        if img_file_buffer is not None:
            # Convert file buffer to cv2 image
            open_cv_image = create_opencv_image_from_stringio(img_file_buffer)

            # Pass image to the model to get the detection result
            detected_image, detected_texts = run(open_cv_image)

            # Show result image using st.image()
            if detected_image is not None:
                st.image(detected_image, channels="RGB",
                         caption=f'Detection Results ({n + 1}/{len(img_files)})')

            # Display detected texts and analyze them
            if detected_texts:
                # st.markdown(f"Detected Texts ({n+1}/{len(img_files)}):")
                for text in detected_texts:
                    # st.write(text.strip())  # For debugging purposes
                    # Analyze the detected text
                    analysis_result, corrected_text = analyze_number_plate(text)
                    st.write(f"Detected Vehicle Number: {corrected_text}")  # Display corrected text
                    st.write(analysis_result)  # Display analysis result

                    # Ask user if the detected plate is correct
                    confirmation = st.selectbox('Is this number plate correct?', ('Select an option', 'Yes', 'No'))
                    if confirmation == 'Yes':
                        # Check if the number plate already exists in authorized vehicles
                        if corrected_text in authorized_vehicles['Plate_Number'].values:
                            st.warning('This number plate is already authorized.')
                        else:
                            # Create a new DataFrame for appending
                            new_record = pd.DataFrame({'Plate_Number': [corrected_text]})
                            authorized_vehicles = pd.concat([authorized_vehicles, new_record], ignore_index=True)
                            st.success('Number plate added to authorized vehicles.')
                    elif confirmation == 'No':
                        # Ask user to enter manually and add to authorized vehicles
                        manual_input = st.text_input('Enter the correct number plate manually:')
                        if st.button('Add manually entered number plate'):
                            if manual_input in authorized_vehicles['Plate_Number'].values:
                                st.warning('This number plate is already authorized.')
                            else:
                                new_record = pd.DataFrame({'Plate_Number': [manual_input]})
                                authorized_vehicles = pd.concat([authorized_vehicles, new_record], ignore_index=True)
                                st.success('Manually entered number plate added to authorized vehicles.')
                        else:
                            st.warning('Please enter your vehicle number in the field above.')

    # Save authorized vehicles back to CSV
    authorized_vehicles.to_csv('datasets/authorized_vehicles.csv', index=False)

    st.markdown("<br><br>", unsafe_allow_html=True)





if __name__ == '__main__':
    main()