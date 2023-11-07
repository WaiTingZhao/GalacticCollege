import streamlit as st
import pandas as pd

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
aggregatedDataset = aggregatedDataset.rename(columns={"Fake ID":"Students"})

st.dataframe(aggregatedDataset)

#Remove all the grade results of "F" and "W"
#Remove all the Course number with "None"
grade_column = 'Grade'
joinedDataset[grade_column] = joinedDataset[grade_column].str.strip().str.upper()
filteredDataset = joinedDataset[~joinedDataset[grade_column].isin(['F', 'W'])]
st.dataframe(filteredDataset)

#Only keep "In-Person", "Online", "Online Hybrid", "Independent Studies" under the column of Instruction mode.
instruction_mode_column = 'Instruction mode'
#Change "Online Hybrid" into "Blended"

#Change the "course section number" into the correct "course title" name.
