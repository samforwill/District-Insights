import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LassoCV

# Load the data
pct_df = pd.read_csv('data/Full_Dataset_PCT.csv')

# get the variables you need to change your predictions
st.title('Political margin predictions!')

districts = sorted(list(set(pct_df['Formatted_District'].values)))
district = st.selectbox('Select your district', districts)

# Provide a slider to change the metric for the chosen district
turnout_to_change = st.slider('Percent of 2020 turnout', min_value=0.0, max_value=150.0, value=50.0, step=0.1)

# Filter the data
filtered_pct_df = pct_df[pct_df["Swing from 2020 presidential"].abs() <= 22] #ran unopposed

    
# Preprocess the data
pct_df["Percent of 2020 turnout"] = pct_df["Percent of 2020 turnout"].str.rstrip('%').astype('float')

# Filter the data for training
filtered_pct_df = pct_df[pct_df["Swing from 2020 presidential"].abs() <= 22] #ran unopposed

# Define target variable
y = filtered_pct_df['2022 Margin']


primary_columns = ['COMMUTING TO WORK - Worked from home', 'RACE - One race - Black or African American', 'HISPANIC OR LATINO AND RACE - Mexican', 'EDUCATIONAL ATTAINMENT - Population 25 years and over - Graduate or professional degree', 'ANCESTRY - Swiss', 'Total households - Cohabiting couple household', 'SELECTED MONTHLY OWNER COSTS (SMOC) - Housing units without a mortgage - $600 to $799', 'YEAR STRUCTURE BUILT - Built 1940 to 1949', 'Females 15 years and over - Never married', 'HOUSE HEATING FUEL - Wood', 'ANCESTRY - Swedish', 'ANCESTRY - French Canadian', 'HEALTH INSURANCE COVERAGE - Not in labor force: - With public coverage', 'EMPLOYMENT STATUS - Females 16 years and over - In labor force', 'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME (SMOCAPI) - Housing unit without a mortgage (excluding units where SMOCAPI cannot be computed) - 10.0 to 14.9 percent', 'RACE - Two or more races - White and American Indian and Alaska Native', 'HOUSE HEATING FUEL - Coal or coke', 'GROSS RENT - No rent paid', 'VALUE - $200,000 to $299,999', 'Total population - Under 5 years', 'INDUSTRY - Wholesale trade', 'PLACE OF BIRTH - Native - State of residence', 'Total households - Married-couple household - With children of the householder under 18 years', 'EDUCATIONAL ATTAINMENT - Population 25 years and over - High school graduate (includes equivalency)', 'HISPANIC OR LATINO AND RACE - Cuban', 'YEAR STRUCTURE BUILT - Built 1980 to 1989', 'INDUSTRY - Agriculture, forestry, fishing and hunting, and mining', 'Total households - Married-couple household', 'EDUCATIONAL ATTAINMENT - Population 25 years and over - Some college, no degree', 'RACE - One race - White']

# Define feature variables for training
X_train = filtered_pct_df[primary_columns].copy()  # Make a copy to avoid SettingWithCopyWarning
X_train["Percent of 2020 turnout"] = filtered_pct_df["Percent of 2020 turnout"]
X_train['PVI_2023'] = filtered_pct_df['PVI_2023']   # just in case we wanna use it

# Initialize the scaler
scaler = MinMaxScaler()

# Fit the scaler on the training data
scaler.fit(X_train)

# Transform the training data
X_train_scaled = scaler.transform(X_train)

# Initialize LassoCV
lasso = LassoCV(cv=3)

# Fit the model
lasso.fit(X_train_scaled, y)

if st.button('Predict the margin'):
    # Change the selected metric for the chosen district
    pct_df.loc[pct_df['Formatted_District'] == district, 'Percent of 2020 turnout'] = turnout_to_change

    # Prepare the data for the chosen district
    district_data = pct_df[pct_df['Formatted_District'] == district][primary_columns].copy()
    district_data["Percent of 2020 turnout"] = pct_df[pct_df['Formatted_District'] == district]["Percent of 2020 turnout"]
    district_data['PVI_2023'] = pct_df[pct_df['Formatted_District'] == district]['PVI_2023']

    # Scale the data for the chosen district
    district_data_scaled = scaler.transform(district_data)

    # Generate prediction
    prediction = lasso.predict(district_data_scaled)

    # Check if the selected district is in the filtered DataFrame
    if district not in filtered_pct_df['Formatted_District'].values:
        st.write('This district ran unopposed!! But given a generic opponent, my predicted margin would be:', prediction[0])
    else:
        # Actual margin
        actual_margin = pct_df[pct_df['Formatted_District'] == district]['2022 Margin'].values[0]
        st.write(f'The actual margin is {actual_margin}')
        st.write(f'The predicted margin is {prediction[0]}')
    


    
    