import streamlit as st
import pandas as pd
import plotly.express as px

# open the data
courseData = pd.read_csv("Course section info.csv")
studentCourse = pd.read_csv("Student - course section info.csv")
studentCareer = pd.read_csv("Student career info.csv")
studentInfo = pd.read_csv("Student info.csv")
studentTerm = pd.read_csv("Student term info.csv")

# show the data
# st.write(courseData)
# st.write(studentCourse)
# st.write(studentCareer)
# st.write(studentInfo)
# st.write(studentTerm)

#Merging the data from courseData and studentCourse
joinedDataset = studentCourse.merge(courseData, on=["Term code", "Course section number"], how="left")
#st.write(joinedDataset)
joinedDataset = joinedDataset.dropna(subset=["Course title"])
aggregatedDataset = joinedDataset.groupby(["Course title", "Term code","Course section number", "Instruction mode"]).aggregate({"Fake ID":"count"}).reset_index()
#st.write(aggregatedDataset)


#Remove all the grade results of "F" and "W"
#Remove all the Course number with "None"
grade_column = 'Grade'
joinedDataset[grade_column] = joinedDataset[grade_column].str.strip().str.upper()
filteredDataset = joinedDataset[~joinedDataset[grade_column].isin(['F', 'W'])]



#Only keep "In-Person", "Online", "Online Hybrid", "Independent Studies" under the column of Instruction mode.
#Change "Online Hybrid" into "Blended"
instruction_mode_column = 'Instruction mode'
filteredDataset[instruction_mode_column] = filteredDataset[instruction_mode_column].str.replace("Online Hybrid", "Blended (Online & In-Person)")


#filteredDataset["Year"]= filteredDataset["Term_x"].str.split()[1]
st.dataframe(filteredDataset)
filteredDataset = filteredDataset.groupby(["Course title"]).aggregate({"Fake ID": "count"}).reset_index()
filteredDataset = filteredDataset.rename(columns={"Fake ID": "Students"})


#Create Interface
st.set_page_config(layout="wide")
st.title("Popular Courses")
st.sidebar.title("Filters")

#Select the Visualization
vis = st.sidebar.radio("Select a visualization",
                       options=["Instruction mode",
                                "Term_X"])

df = pd.DataFrame(filteredDataset)
sorted_data = df.sort_values(by='Students', ascending=True).head(10)
fig = px.bar(sorted_data, x='Students', y='Course title')
st.plotly_chart(fig)
st.dataframe(filteredDataset)

