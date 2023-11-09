import streamlit as st
import pandas as pd
import plotly.express as px

# open the data
courseData = pd.read_csv("Course section info.csv")
studentCourse = pd.read_csv("Student - course section info.csv")
studentCareer = pd.read_csv("Student career info.csv")
studentInfo = pd.read_csv("Student info.csv")
studentTerm = pd.read_csv("Student term info.csv")

#Merging the data from studentTerm and studentInfo
joinedDataset = studentTerm.merge(studentInfo, on=["Fake ID"], how="left")
st.write(joinedDataset)
