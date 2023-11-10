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
