import streamlit as st
import pandas as pd
import plotly.express as px

# open the data
courseData = pd.read_csv("Course section info.csv")
studentCourse = pd.read_csv("Student - course section info.csv")
studentCareer = pd.read_csv("Student career info.csv")
studentInfo = pd.read_csv("Student info.csv")
studentTerm = pd.read_csv("Student term info.csv")

#Merging the data from courseData and studentCourse
joinedDataset = studentCourse.merge(courseData, on=["Term code", "Course section number"], how="left")
joinedDataset = joinedDataset.dropna(subset=["Course title"])
aggregatedDataset = joinedDataset.groupby(["Course title", "Term_x", "Grade"]).aggregate({"Fake ID":"count"}).reset_index()

#Convert terms to years
aggregatedDataset["Year"]= aggregatedDataset["Term_x"].str.split().str[1]
aggregatedDataset["Year"]= pd.to_numeric(aggregatedDataset["Year"])

st.write(aggregatedDataset)

# Assuming you've loaded and processed your dataset as 'aggregatedDataset' here

# Create a sidebar for course selection
selected_course = st.sidebar.selectbox("Select a Course", aggregatedDataset['Course title'].unique())

# Filter the data for the selected course
selected_course_data = aggregatedDataset[aggregatedDataset['Course title'] == selected_course]

# Group by grade and calculate the count for the selected course
grade_distribution_selected_course = selected_course_data.groupby('Grade').size().reset_index(name='Count')

# Calculate percentages
total_count = grade_distribution_selected_course['Count'].sum()
grade_distribution_selected_course['Percentage'] = (grade_distribution_selected_course['Count'] / total_count) * 100

# Create a pie chart for the selected course's grade distribution
fig_selected_course_pie = px.pie(grade_distribution_selected_course, values='Percentage', names='Grade',
                                 title=f'Grade Distribution for {selected_course}', hole=0.3)

# Set category order for the legend (letter grades)
fig_selected_course_pie.update_layout(
    legend=dict(traceorder='normal'),
    legend_title="Grades",
    legend_traceorder='reversed'
)
st.plotly_chart(fig_selected_course_pie)




