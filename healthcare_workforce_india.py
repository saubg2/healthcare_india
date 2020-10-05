import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

#setting page
st.beta_set_page_config(page_title='India Healthcare Workforce', page_icon=None, layout='centered', initial_sidebar_state='auto')


#showing title
st.title('Healthcare Workforce in India')

st.text('''
This small project is to overcome the issues 
in gathering data on healthcare workforce in India. 
The data has been gathered from MoH.

The process is on, hands are welcome (saurabhjaipur@gmail.com)
Raw data option is available in sidebar 
''' )
#load data
url='https://docs.google.com/spreadsheets/d/e/2PACX-1vRpLJT-xzmtDSzqxWyol-IanK7kTAdJoDLr8no36copDdkSg7r4j4rUnftVUMZ-Upf6Omynq13Le1EE/pub?gid=0&single=true&output=csv'

# When using @st.cache make sure you have a function that fetches data. 
# Also, you should put the catche just above that function

@st.cache
def fetch_data(link):
	data = pd.read_csv(link)
	data.columns = ['Year','Healthcare_Professional','Healthcare_Center','State', 'Required','Sanctioned','In_Position','Vacant','Shortfall']
	data['Shortfall_Percent'] = np.round((data.In_Position - data.Required)*100/(data.Required),1)
	data['Shortfall'] = data.In_Position - data.Required
	data['Status'] = data['Shortfall_Percent']>0
	data['Status'] = data['Status'].map({True:'Excess',False:'Shortfall'})
	return data

data = fetch_data(url)


#Giving Option to Choose Speciality


# Multi-Select to Choose Healthcare Professional 
professional = st.selectbox('Healthcare Professional', data.Healthcare_Professional.unique(), index = 6, key=None)

#Single Select to Choose CHC/PHC Center 
center = st.selectbox('Healthcare Center', data.Healthcare_Center.unique(), index=1, key=None)

#Slider to Choose Year
year = st.slider('Select Year', min_value=int(min(data.Year.unique())), max_value=int(max(data.Year.unique())), value=int(2019), step=None, format=None, key=None)

#filtering data
data = data[(data.Year == year)&
			(data.Healthcare_Center == center)&
			(data.Healthcare_Professional ==professional)]  


# Pushing Raw Data On Screen
if st.sidebar.checkbox('Show Raw Data'):
	st.subheader('Raw Data')
	st.write(data) # could alternatively use ====> st.dataframe(data)



if len(data) == 0:
	st.text('This Data is Not Available Yet, Please Make Another Selection')
	
else:
	# Plot the Chart
	st.subheader('Shortfall in Percentage')
	st.text('''This is ratio between required and in-position for selected healthcare professional''')
	fig, ax = plt.subplots()
	ax = sns.catplot(
	y = 'State',
	x = 'Shortfall_Percent',
	data = data.sort_values(by = 'Shortfall_Percent', axis = 0),
	kind = 'bar',
	height = 9,
	aspect = 1,
	hue = 'Status')

	plt.tick_params(
    axis = 'x',#x/y/both
    which = 'major',
    size = 3,
    direction = 'inout',#in,out,inout
    
    labelsize = 12,
    labelcolor = 'black',
    
    gridOn = True,
    grid_linewidth = 1,
    grid_color = 'grey',
    grid_alpha = 0.5,
    grid_in_layout = False,
    grid_linestyle = '-',
    grid_zorder = 0,
 
    labelrotation = 0,
    labelright = False,
    labelleft = True,
    labeltop = True,
    labelbottom = False,
    )

	plt.xlabel(
    xlabel = 'Shortfall/Excess in %',
    fontsize = 12,
    labelpad = 15,
    fontweight = 500,
    family = 'Verdana', 
    horizontalalignment = 'center',# this is so counterintuitive
    verticalalignment = 'top',
    color = 'black',
    )
    
	st.pyplot(ax)
