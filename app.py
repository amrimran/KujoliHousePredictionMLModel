import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load the trained model
model = joblib.load('kujoli_random_forest_model.pkl')

current_year = datetime.now().year

min_year = 1900
max_year = current_year + 100
default_year = (min_year + max_year) // 2

# Title and description
st.title('Kujoli House Price Prediction App')
st.write('Enter the details of the house below to get the predicted price.')
df = pd.read_csv('data.csv')

neighborhood_dict = {
    'College Creek': 'CollgCr',
    'Veenker': 'Veenker',
    'Crawford': 'Crawfor',
    'Northridge': 'NridgHt',
    'Mitchell': 'Mitchel',
    'Somerset': 'Somerst',
    'Northwest Ames': 'NWAmes',
    'Old Town': 'OldTown',
    'Brookside': 'BrkSide',
    'Sawyer': 'Sawyer',
    'Northridge Heights': 'NoRidge',
    'North Ames': 'Names',
    'Sawyer West': 'SawyerW',
    'Iowa DOT and Rail Road': 'IDOTRR',
    'Meadow Village': 'MeadowV',
    'Edwards': 'Edwards',
    'Timberland': 'Timber',
    'Gilbert': 'Gilbert',
    'Stone Brook': 'StoneBr',
    'Clear Creek': 'ClearCr',
    'Northpark Villa': 'NPkVill',
    'Bloomington': 'Blmngtn',
    'Briardale': 'BrDale',
    'South & West of Iowa State University': 'SWISU',
    'Bluestem': 'Blueste'
}

houseStyle_dict = {
    'One story':'1Story',
    'One and one-half story: 2nd level finished':'1.5Fin',
    'One and one-half story: 2nd level unfinished':'1.5Unf',
    'Two story':'2Story',
    'Two and one-half story: 2nd level finished':'2.5Fin',
    'Two and one-half story: 2nd level unfinished':'2.5Unf',
    'Split Foyer':'SFoyer',
    'Split Level':'SLvl'
}

# Create a list of display names for the dropdown
neighborhood_names = list(neighborhood_dict.keys())
houseStyle_names = list(houseStyle_dict.keys())


unique_neighborhoods = df['Neighborhood'].unique().tolist()
unique_neighborhoods2 = ['College Creek','Veenker','Crawford','Northridge','Mitchel','Somerset','Northwest Ames','Old Town','Brookside','Sawyer','Northridge Heights','North Ames','Sawyer West','Iowa DOT and Rail Road','Meadow Village','Edwards','Timberland','Gilbert','Stone Brook','Clear Creek','Northpark Villa','Bloomington','Briardale','South & West of Iowa State University','Bluestem']
years = list(range(1900, current_year + 1))
years.reverse()



neighborhood = st.selectbox('Neighborhood', options=neighborhood_names)
houseStyle = st.selectbox('House Style', options=houseStyle_names)
year_built = st.selectbox('Year Built', options=years, index=years.index(current_year))
bedroomAbvGr = st.number_input('Num of Bedroom', min_value=0, max_value=10, value=3)
bathrooms = st.number_input('Num of Bathrooms', min_value=0, max_value=10, value=5)
num_of_fireplaces= st.number_input('Num of Fireplace(s)', min_value=0, max_value=5, value=1)
garagecars= st.number_input('Num of Car(s) fit in Garage', min_value=0, max_value=5, value=1)
grLivArea= st.slider('Above ground living area square feet', min_value=0, max_value=1000, value=500)
totalBsmtSF = st.slider('Total square feet of basement area', min_value=0, max_value=1000, value=1)

# Retrieve the exact value based on the selected display name
selected_neighborhood = neighborhood_dict[neighborhood]
selected_houseStyle = houseStyle_dict[houseStyle]


# Dictionary to store input data
input_data = {
    'YearBuilt': [year_built],
    'Fireplaces': [num_of_fireplaces],
    'GarageCars': [garagecars],
    'GrLivArea': [grLivArea],
    'TotalBsmtSF': [totalBsmtSF],
    'BedroomAbvGr': [bedroomAbvGr],
    'Bathrooms':[bathrooms],
    'Neighborhood': [selected_neighborhood],
    # 'Neighborhood': [],    
    'HouseStyle': [selected_houseStyle],  
}

# Convert to DataFrame
input_df = pd.DataFrame(input_data)
encoded_data = pd.get_dummies(input_df, columns=['Neighborhood', 'HouseStyle'])

all_columns = ['YearBuilt', 'Fireplaces', 'GarageCars', 'GrLivArea', 'TotalBsmtSF',
               'BedroomAbvGr', 'Bathrooms', 'Neighborhood_Blmngtn','Neighborhood_Blueste',
               'Neighborhood_BrDale','Neighborhood_BrkSide','Neighborhood_ClearCr','Neighborhood_CollgCr',
               'Neighborhood_Crawfor','Neighborhood_Edwards','Neighborhood_Gilbert','Neighborhood_IDOTRR',
               'Neighborhood_MeadowV','Neighborhood_Mitchel','Neighborhood_NAmes',
                'Neighborhood_NPkVill', 'Neighborhood_NWAmes', 'Neighborhood_NoRidge',
                'Neighborhood_NridgHt', 'Neighborhood_OldTown', 'Neighborhood_SWISU',
                'Neighborhood_Sawyer', 'Neighborhood_SawyerW', 'Neighborhood_Somerst',
                'Neighborhood_StoneBr', 'Neighborhood_Timber', 'Neighborhood_Veenker',
                'HouseStyle_1.5Fin', 'HouseStyle_1.5Unf', 'HouseStyle_1Story',
                'HouseStyle_2.5Fin', 'HouseStyle_2.5Unf', 'HouseStyle_2Story',
                'HouseStyle_SFoyer', 'HouseStyle_SLvl']

for column in all_columns:
    if column not in encoded_data.columns:
        encoded_data[column] = False

encoded_data = encoded_data.reindex(columns=all_columns)

encoded_data2 = pd.DataFrame(encoded_data)

# Predict button
if st.button('Predict'):
    print(
        "heheh"
    )
    print(encoded_data)
    # Assuming you have your encoded_data DataFrame
# Iterate over each row and print its values
    for index, row in encoded_data.iterrows():
        print(row)

    prediction = model.predict(encoded_data2)
    st.write(f'The predicted house price is: $ {prediction[0]:,.2f}')
