# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!

#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit
# To run from terminal: streamlit run myapp.py

#---------------------------------#
# Imports
import streamlit as st
from PIL import Image
import pandas as pd
import json
import numpy as np

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title
image = Image.open('logo.jpg')
st.image(image, width = 500)
st.title('AB & Tau Risk Scores for MCI Individuals')
st.markdown("""
**Description:** Maximum score of 100 points.
""")

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
""")

#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Variables')



#---------------------------------#
# Sidebar - Predictors Input
model_ab = 0
model_desc = 'Model has not yet been chosen.'

age = col1.slider('Age (years)', 65, 85, 65)

height = col1.slider('Height (inches)', 36, 96, 36)
weight = col1.slider('Weight (lbs)', 51, 350, 51)
bmi = 703*float(weight)/float(height)**2

check_WMH = col1.checkbox('WMH is known')
if check_WMH:
    wmh = col1.slider('WMH', 0, 5, 0)
check_apoe4 = col1.checkbox('APOE4 status is known')
if check_apoe4:
    apoe4 = col1.radio('APOE4 (# of e4 alleles)', ['0','1','2','Unknown'])
check_adas = col1.checkbox('ADAS-13 score is known')
if check_adas:
    adas = col1.slider('ADAS-13', 0, 13, 0)
check_trab = col1.checkbox('TRAB score is known')
if check_trab:
    adas = col1.slider('ADAS-13', 0, 13, 0)


#---------------------------------#
# Page contents
col2.subheader('Risk Score')

#---------------------------------#
# Indicator vectors for age, bmi, family history, free recall, and ADL
age_points = [0,0,0]
bmi_points = [0,0,0]
trab_points = [0,0]
adas_points = [0,0]
apo_points = [0,0,0]
wmh_points = [0,0]

A = [0,0,0]
B = [0,0,0]
T = [0,0]
AD = [0,0]
APO = [0,0,0]
W = [0,0]

if model_ab==1:
    a = float(age)
    if a < 60:
        A = [1,0,0]
    elif a < 75:
        A = [0,1,0]
    else:
        A = [0,0,1]

    if bmi < 25:
        B = [1,0,0]
    elif bmi < 30:
        B = [0,1,0]
    else:
        B = [0,0,1]

    age_points = [0,38,75]
    bmi_points = [25,12,0]

    model_desc = 'Model 1 chosen with variables: Age and BMI.'

elif model_ab==2:
    a = float(age)
    if a < 60:
        A = [1,0,0]
    elif a < 75:
        A = [0,1,0]
    else:
        A = [0,0,1]

    if trab<115:
        T = [1,0]
    else:
        T = [0,1]

    if adas<20:
        AD = [1,0]
    else:
        AD = [0,1]

    age_points = [0,33,55]
    trab_points = [7,0]
    adas_points = [0,40]

    model_desc = 'Model 2 chosen with variables: Age, Trail-B, and ADAS-13.'

elif model_ab==3:
    a = float(age)
    if a < 60:
        A = [1,0,0]
    elif a < 75:
        A = [0,1,0]
    else:
        A = [0,0,1]

    if trab<115:
        T = [1,0]
    else:
        T = [0,1]

    if adas<20:
        AD = [1,0]
    else:
        AD = [0,1]

    ap = float(apoe4)
    if ap==0:
        APO = [1,0,0]
    elif ap==1:
        APO = [0,1,0]
    elif ap==2:
        APO = [0,0,1]

    age_points = [0,24,40]
    trab_points = [1,0]
    adas_points = [0,15]
    apo_points = [0,26,45]

    model_desc = 'Model 3 chosen with variables: Age, Trail-B, ADAS-13, and APOE4 status.'

elif model_ab==4:
    a = float(age)
    if a < 60:
        A = [1,0,0]
    elif a < 75:
        A = [0,1,0]
    else:
        A = [0,0,1]

    if adas<20:
        AD = [1,0]
    else:
        AD = [0,1]

    ap = float(apoe4)
    if ap==0:
        APO = [1,0,0]
    elif ap==1:
        APO = [0,1,0]
    elif ap==2:
        APO = [0,0,1]

    if wmh<1.2:
        W = [1,0]
    else:
        W = [0,1]

    age_points = [0,23,37]
    adas_points = [0,14]
    apo_points = [0,25,44]
    wmh_points = [0,5]

    model_desc = 'Model 4 chosen with variables: Age, ADAS-13, APOE4 status, and WMH.'


#---------------------------------#
# Calculate score as sum of dot products between vectors
score = np.dot(A, age_points)
score = score + np.dot(B, bmi_points)
score = score + np.dot(T, trab_points)
score = score + np.dot(AD, adas_points)
score = score + np.dot(APO, apo_points)
score = score + np.dot(W, wmh_points)
#score = score + np.dot(AD, adl_points)

#---------------------------------#
#Output to screen
if model_ab == 0:
    col2.write(model_desc)
else:
    col2.write(model_desc)
    col2.write('Risk Score points total: ' + str(score))
    col2.write('For educational purposes only')
    col2.write('For details see: PAPER')
