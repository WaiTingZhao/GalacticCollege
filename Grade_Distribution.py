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
aggregatedDataset = joinedDataset.groupby(["Course title", "Term code","Course section number"]).aggregate({"Fake ID":"count"}).reset_index()

#Remove all the grade results of "F" and "W"
#Remove all the Course number with "None"
grade_column = 'Grade'
joinedDataset[grade_column] = joinedDataset[grade_column].str.strip().str.upper()
filteredDataset = joinedDataset[~joinedDataset[grade_column].isin(['F', 'W'])]
st.write(filteredDataset)

