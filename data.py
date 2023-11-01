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

joinedDataset = studentCourse.merge(courseData, on=["Term code", "Course section number"], how="left")
st.write(joinedDataset)
joinedDataset = joinedDataset.dropna(subset=["Course title"])

aggregatedDataset = joinedDataset.groupby(["Course title", "Term code"]).aggregate({"Fake ID":"count"}).reset_index()
st.write(aggregatedDataset)
aggregatedDataset = aggregatedDataset.rename(columns={"Fake ID":"Students"})



st.dataframe(aggregatedDataset)