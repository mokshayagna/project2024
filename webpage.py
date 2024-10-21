import streamlit as st
import pandas as pd
import numpy as np

# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
    
# }))
# #create a table with 10 rows and 20 columns
# dataframe = pd.DataFrame(np.random.randn(10, 20))
# st.dataframe(dataframe)

# #creates table and highlights 
# dataframe = pd.DataFrame(np.random.randn(10, 20),columns=('col %d' % i for i in range(20)))
# st.dataframe(dataframe.style.highlight_max(axis=0))


# selecting
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option


# import streamlit as st

# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


#import streamlit as st

# Create a text input box
user_input = st.text_input("Enter your text:")

# Display the entered text
if user_input:
    st.write("You entered:", user_input)
