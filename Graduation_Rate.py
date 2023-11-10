import streamlit as st
import pandas as pd
import plotly.express as px

# Open the data
courseData = pd.read_csv("Course section info.csv")
studentCourse = pd.read_csv("Student - course section info.csv")
studentCareer = pd.read_csv("Student career info.csv")
studentInfo = pd.read_csv("Student info.csv")
studentTerm = pd.read_csv("Student term info.csv")

# Merging the data from studentTerm and studentInfo
# joinedDataset = studentTerm.merge(studentInfo, on=["Fake ID"], how="left")

# Create a new 'enrolled' column considering all students with an academic plan as enrolled
studentCareer['Enrolled'] = studentCareer['Academic plan'].apply(lambda x: 1 if pd.notna(x) else 0)

# Create a new 'graduated' column based on whether 'degree_earned' is not blank
studentCareer['Graduated'] = studentCareer['Degree awarded'].apply(lambda x: 1 if pd.notna(x) and str(x).strip() else 0)

# Extract years from 'Start effective term'
studentCareer['Start effective year'] = studentCareer['Start effective term'].str.extract('(\d{4})')

# Convert 'Start effective year' to integers
studentCareer['Start effective year'] = pd.to_numeric(studentCareer['Start effective year'], errors='coerce')

# Streamlit web app
st.title("Graduation Rate Calculator")

# Sidebar for user input
selection = st.sidebar.radio("Select Graduation Rate Based On:", ('Degree', 'Academic Plan'))

# Use 'Start effective year' values for slider range
min_year, max_year = studentCareer['Start effective year'].min(), studentCareer['Start effective year'].max()

# Convert to integer to ensure consistent types
min_year, max_year = int(min_year), int(max_year)

# Create a slider with numerical values
selected_year_range = st.sidebar.slider('Select Year Range',
                                        min_value=min_year,
                                        max_value=max_year,
                                        value=(min_year, max_year))

# Convert to integer to ensure consistent types
selected_year_range = tuple(map(int, selected_year_range))

# Filter the data based on the selected year range
filtered_data = studentCareer[(studentCareer['Start effective year'] >= selected_year_range[0]) &
                              (studentCareer['Start effective year'] <= selected_year_range[1])]

# Group by selected category
if selection == 'Degree':
    grouped_data = filtered_data.groupby('Degree')
    title = 'Graduation Rate Based on Degree'
elif selection == 'Academic Plan':
    grouped_data = filtered_data.groupby('Academic plan')
    title = 'Graduation Rate Based on Academic Plan'

# Calculate graduation rate
graduated_count = grouped_data['Graduated'].sum()
enrolled_count = grouped_data['Enrolled'].sum()
graduation_rate = graduated_count / enrolled_count * 100

# Debugging information
# st.write("Graduated Count:", graduated_count)
# st.write("Enrolled Count:", enrolled_count)

# Create a DataFrame for Plotly
graduation_rate_df = pd.DataFrame({
    'Group': graduation_rate.index,
    'Graduation Rate': graduation_rate.values
})

# Display the results using Plotly with inverted axes
fig = px.bar(graduation_rate_df, x='Graduation Rate', y='Group', text='Graduation Rate',
             labels={'Graduation Rate': 'Graduation Rate (%)'})
fig.update_layout(title=title, xaxis_title='Graduation Rate (%)', yaxis_title=selection)
st.plotly_chart(fig)
