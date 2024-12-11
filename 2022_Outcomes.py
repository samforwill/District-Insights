import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LassoCV
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
pct_df = pd.read_csv('data/Full_Dataset_PCT.csv')
prf_df = pd.read_csv('data/Full_Dataset_PRF.csv')
localities_df = pd.read_csv('data/district_localities.csv')

# get the variables you need to change your predictions
st.title('Know Your District!')

st.image('http://proximityone.com/cv_dr_graphics/cv_header_la_tract_cvapasian1.jpg')

districts = sorted(list(set(pct_df['Formatted_District'].values)))
district = st.selectbox('Select your district', districts)



state_pictures = {'AL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Alabama_Congressional_Districts%2C_118th_Congress.svg/760px-Alabama_Congressional_Districts%2C_118th_Congress.svg.png',
 'AK': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/AK01_109.png',
 'AZ': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Arizona_Congressional_Districts%2C_118th_Congress.svg/1378px-Arizona_Congressional_Districts%2C_118th_Congress.svg.png',
 'AR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Arkansas_Congressional_Districts%2C_118th_Congress.svg/1600px-Arkansas_Congressional_Districts%2C_118th_Congress.svg.png',
 'CA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/California_Congressional_Districts%2C_118th_Congress.svg/1002px-California_Congressional_Districts%2C_118th_Congress.svg.png',
 'CO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Colorado_Congressional_Districts%2C_118th_Congress.svg/1600px-Colorado_Congressional_Districts%2C_118th_Congress.svg.png',
 'CT': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Connecticut_Congressional_Districts%2C_118th_Congress.svg/1548px-Connecticut_Congressional_Districts%2C_118th_Congress.svg.png',
 'DE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/National-atlas-delaware.png/1552px-National-atlas-delaware.png',
 'FL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Florida_Congressional_Districts%2C_118th_Congress.svg/1474px-Florida_Congressional_Districts%2C_118th_Congress.svg.png',
 'GA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Georgia_congressional_map_2022.jpg/922px-Georgia_congressional_map_2022.jpg',
 'HI': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Hawaii_Congressional_Districts%2C_118th_Congress.svg/1600px-Hawaii_Congressional_Districts%2C_118th_Congress.svg.png',
 'ID': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Idaho_Congressional_Districts%2C_118th_Congress.svg/1200px-Idaho_Congressional_Districts%2C_118th_Congress.svg.png',
 'IL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Illinois_Congressional_Districts%2C_118th_Congress.tif/lossless-page1-808px-Illinois_Congressional_Districts%2C_118th_Congress.tif.png',
 'IN': 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Indiana%27s_congressional_districts_%28since_2023%29.png',
 'IA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Iowa%27s_Congressional_Districts%2C_118th_Congress.svg/1600px-Iowa%27s_Congressional_Districts%2C_118th_Congress.svg.png',
 'KS': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Kansas_Congressional_Districts%2C_118th_Congress.tif/lossless-page1-1600px-Kansas_Congressional_Districts%2C_118th_Congress.tif.png',
 'KY': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Kentucky_Congressional_Districts%2C_118th_Congress.svg/1600px-Kentucky_Congressional_Districts%2C_118th_Congress.svg.png',
 'LA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Louisiana_Congressional_Districts%2C_118th_Congress.svg/1309px-Louisiana_Congressional_Districts%2C_118th_Congress.svg.png',
 'ME': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Maine%27s_congressional_districts_%28since_2023%29.png',
 'MD': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Maryland_Congressional_Districts%2C_118th_Congress_signed_by_the_Governor.svg/1600px-Maryland_Congressional_Districts%2C_118th_Congress_signed_by_the_Governor.svg.png',
 'MA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Massachusetts_Congressional_Districts%2C_118th_Congress.svg/1600px-Massachusetts_Congressional_Districts%2C_118th_Congress.svg.png',
 'MI': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Michigan_Congressional_Districts%2C_118th_Congress.svg/1085px-Michigan_Congressional_Districts%2C_118th_Congress.svg.png',
 'MN': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/MN_2022_congressional_districts.jpg/1060px-MN_2022_congressional_districts.jpg',
 'MS': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Mississippi_Congressional_Districts%2C_118th_Congress.svg/784px-Mississippi_Congressional_Districts%2C_118th_Congress.svg.png',
 'MO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Missouri_Congressional_Districts%2C_118th_Congress.svg/1356px-Missouri_Congressional_Districts%2C_118th_Congress.svg.png',
 'MT': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Montana_Congressional_Districts%2C_118th_Congress.svg/1600px-Montana_Congressional_Districts%2C_118th_Congress.svg.png',
 'NE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Nebraska_Congressional_Districts%2C_118th_Congress.tif/lossless-page1-1600px-Nebraska_Congressional_Districts%2C_118th_Congress.tif.png',
 'NV': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Nevada_Congressional_Districts%2C_118th_Congress.svg/990px-Nevada_Congressional_Districts%2C_118th_Congress.svg.png',
 'NH': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/New_Hampshire_Congressional_Districts%2C_118th_Congress.svg/1200px-New_Hampshire_Congressional_Districts%2C_118th_Congress.svg.png',
 'NJ': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/New_Jersey_Congressional_Districts%2C_118th_Congress.svg/740px-New_Jersey_Congressional_Districts%2C_118th_Congress.svg.png',
 'NM': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/New_Mexico_Congressional_Districts%2C_118th_Congress.svg/1086px-New_Mexico_Congressional_Districts%2C_118th_Congress.svg.png',
 'NY': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/New_York_Congressional_Districts%2C_118th_Congress.svg/1920px-New_York_Congressional_Districts%2C_118th_Congress.svg.png',
 'NC': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/North_Carolina_Congressional_Districts_since_2023_%28Special_Masters_Remedial_Plan%29.svg/1600px-North_Carolina_Congressional_Districts_since_2023_%28Special_Masters_Remedial_Plan%29.svg.png',
 'ND': 'https://upload.wikimedia.org/wikipedia/commons/d/de/NDAtlarge.gif',
 'OH': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Ohio_Congressional_Districts%2C_118th_Congress.tif/lossless-page1-1132px-Ohio_Congressional_Districts%2C_118th_Congress.tif.png',
 'OK': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Oklahoma_Congressional_Districts%2C_118th_Congress.svg/1600px-Oklahoma_Congressional_Districts%2C_118th_Congress.svg.png',
 'OR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Oregon_Congressional_Districts%2C_118th_Congress.svg/1546px-Oregon_Congressional_Districts%2C_118th_Congress.svg.png',
 'PA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Pennsylvania_Congressional_Districts%2C_118th_Congress.svg/1600px-Pennsylvania_Congressional_Districts%2C_118th_Congress.svg.png',
 'RI': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Rhode_Island_Congressional_Districts%2C_113th_Congress.tif/lossless-page1-973px-Rhode_Island_Congressional_Districts%2C_113th_Congress.tif.png',
 'SC': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/South_Carolina_Congressional_Districts%2C_118th_Congress.svg/1600px-South_Carolina_Congressional_Districts%2C_118th_Congress.svg.png',
 'SD': 'https://upload.wikimedia.org/wikipedia/commons/8/89/SD-AtLarge.gif',
 'TN': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Tennessee%27s_Congressonal_Districts_%282023-%29.png/1599px-Tennessee%27s_Congressonal_Districts_%282023-%29.png',
 'TX': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Texas_Congressional_Districts%2C_118th_Congress.svg/1478px-Texas_Congressional_Districts%2C_118th_Congress.svg.png',
 'UT': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Utah_Congressional_Districts%2C_118th_Congress.tif/lossless-page1-1012px-Utah_Congressional_Districts%2C_118th_Congress.tif.png',
 'VT': 'https://upload.wikimedia.org/wikipedia/commons/2/22/VT_1.gif',
 'VA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Virginia_Congressional_Districts%2C_118th_Congress.svg/1600px-Virginia_Congressional_Districts%2C_118th_Congress.svg.png',
 'WA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/WashCDSVG.svg/1600px-WashCDSVG.svg.png',
 'WV': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/West_Virginia%27s_congressional_districts_%28since_2023%29.png',
 'WI': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Wisconsin_Congressional_Districts%2C_118th_Congress.svg/1920px-Wisconsin_Congressional_Districts%2C_118th_Congress.svg.png',
 'WY': ''}

dem_categories = ['COMMUTING TO WORK - Worked from home',
                  'Total households - Female householder, no spouse/partner present',
                  'HISPANIC OR LATINO AND RACE - Mexican',
                  'EDUCATIONAL ATTAINMENT - Population 25 years and over - Graduate or professional degree',
                  'RACE - One race - Black or African American',
                  'OCCUPATION - Natural resources, construction, and maintenance occupations',
                  'ANCESTRY - Swiss',
                  'HOUSING TENURE - Moved in 1989 and earlier',
                  'COMMUTING TO WORK - Car, truck, or van -- carpooled',
                  'HOUSE HEATING FUEL - Wood',
                  'ANCESTRY - Norwegian']
                    
rep_categories = ['RACE - One race - White',
                  'INDUSTRY - Agriculture, forestry, fishing and hunting, and mining',
                  'EDUCATIONAL ATTAINMENT - Population 25 years and over - Some college, no degree',
                  'PLACE OF BIRTH - Native - State of residence',
                  'Total households - Married-couple household',
                  'ANCESTRY - American',
                  'EDUCATIONAL ATTAINMENT - Population 25 years and over - 9th to 12th grade, no diploma',
                  'Population born outside the United States - Native - Entered 2010 or later',
                  'HEALTH INSURANCE COVERAGE - Civilian noninstitutionalized population under 19 years - No health insurance coverage',
                  'Females 15 years and over - Widowed']
categories = rep_categories

def get_picture_url(district):
    # Split the district string on the hyphen to get the state abbreviation
    state_abbreviation = district.split('-')[0]
    # Return the corresponding picture URL from the dictionary, or None if the state is not in the dictionary
    return state_pictures.get(state_abbreviation)

def double_plot(district_info_dem, district_info_rep):
    sns.set_context("poster")
    
    # Create a long-form DataFrame suitable for seaborn
    long_df_dem = district_info_dem.reset_index().melt(id_vars='index', var_name='Type', value_name='Value')
    long_df_rep = district_info_rep.reset_index().melt(id_vars='index', var_name='Type', value_name='Value')
    
    # Remove the "%" sign and convert the 'Value' column to a numeric data type
    long_df_dem['Value'] = pd.to_numeric(long_df_dem['Value'].str.rstrip('%'))
    long_df_rep['Value'] = pd.to_numeric(long_df_rep['Value'].str.rstrip('%'))
    
    # Create a figure with 2 subplots: one for democratic features and one for republican features
    fig, axs = plt.subplots(nrows=2, figsize=(15, 30))
    
    # Plot the data
    sns.barplot(x='Value', y='index', hue='Type', data=long_df_dem, orient='h', ax=axs[0])
    sns.barplot(x='Value', y='index', hue='Type', data=long_df_rep, orient='h', ax=axs[1])
    
    # Set the titles
    axs[0].set_title('Democratic Features')
    axs[1].set_title('Republican Features')
    
    # Display the plots
    st.pyplot(fig)




def plot_district_info(district_info):
    sns.set_context("poster")
    # Create a long-form DataFrame suitable for seaborn
    long_df = district_info.reset_index().melt(id_vars='index', var_name='Type', value_name='Value')
    
    # Remove the "%" sign and convert the 'Value' column to a numeric data type
    long_df['Value'] = pd.to_numeric(long_df['Value'].str.rstrip('%'))
    
    # Create a figure
    plt.figure(figsize=(15, 15))
    
    # Plot the data
    sns.barplot(x='Value', y='index', hue='Type', data=long_df, orient='h')
    
    # Display the plot
    st.pyplot()


def display_district_info(district, categories, title):
    # Get the raw numbers for the selected district
    district_raw_numbers = prf_df.loc[prf_df['Formatted_District'] == district, categories]
    
    # Calculate the national averages for the percentages
    national_percentage_averages = pct_df[categories].mean()
    
    # Get the percentages for the selected district
    district_percentages = pct_df.loc[pct_df['Formatted_District'] == district, categories]
    
    # Create a DataFrame to nicely display the information
    display_df = pd.DataFrame({
        'National Percentage Averages (%)': national_percentage_averages.values,
        'District Percentages (%)': district_percentages.values[0],
        'District Raw Numbers': district_raw_numbers.values[0]
    }, index=categories)

    # Format the data
    display_df['National Percentage Averages (%)'] = display_df['National Percentage Averages (%)'].map("{:.1f}%".format)
    display_df['District Percentages (%)'] = display_df['District Percentages (%)'].map("{:.1f}%".format)
    display_df['District Raw Numbers'] = display_df['District Raw Numbers'].astype(int)
    
    # Display the DataFrame with a title
    st.subheader(title)
    st.table(display_df)

    # Return the DataFrame
    return display_df









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


if st.button('Show District Info!'):
    # Display the representative's name, localities description, and PVI score
    rep_name = pct_df.loc[pct_df['Formatted_District'] == district, 'Rep'].values[0]
    localities_description = localities_df.loc[localities_df['Formatted_District'] == district, 'Localities'].values[0]
    pvi_score = localities_df.loc[localities_df['Formatted_District'] == district, 'C'].values[0]
    
    
    st.markdown(f"<h2 style='text-align: center; color: black;'>Representative: {rep_name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: black;'>Localities Description: {localities_description}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: black;'>2023 PVI Score: {pvi_score}</h2>", unsafe_allow_html=True)
    
    
    # Display the district picture
    picture_url = get_picture_url(district)
    if picture_url is not None:
        st.image(picture_url)


    # Call the function once and store its result in district_info
    district_info_dem = display_district_info(district, dem_categories, "Democratic Features")
    district_info_rep = display_district_info(district, rep_categories, "Republican Features")
    
    # Use district_info in the call to plot_district_info
    double_plot(district_info_dem, district_info_rep)


    
    
    



    
# Provide a slider to change the metric for the chosen district
st.markdown(f"<h2 style='text-align: center; color: black;'>Predict 2022 Election Results</h2>", unsafe_allow_html=True)
turnout_to_change = st.slider('See how turnout affects predicted margin (based on 2020 election participation rates)', min_value=0.0, max_value=150.0, value=80.0, step=0.1)

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
    


    
    
