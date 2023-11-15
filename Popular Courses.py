import streamlit as st
import pandas as pd
import plotly.express as px

genre = st.radio(
    "Select The Questions",
    ["Question 1: Popular Courses", "Question 2: Graduation Rates", "Question 3: Grade Distribution"],
    captions = ["View the popular courses.", "View the graduation rates.", "View the grade distribution."])

if genre == 'Question 1: Popular Courses':
   st.write("Popular Courses")
if genre == 'Question 2: Graduation Rates':
    st.write("Graduation Rates")
else:
    st.write("Grade Distribution")

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

#Create Interface
st.set_page_config(layout="wide")
st.title("Popular Courses")
st.sidebar.title("Filters")

#Rename Fake ID to 'Students',converted term_x to year.
filteredDataset["Year"]= filteredDataset["Term_x"].str.split().str[1]
filteredDataset["Year"]= pd.to_numeric(filteredDataset["Year"])

#Select the Visualization
mode = st.sidebar.radio("Choose an Instruction Mode",
                       options=["In-Person",
                                "Blended (Online & In-Person)",
                                "Online",
                                "Independent Studies",
                                "Total"])

Year = st.sidebar.slider("Choose your range:",
                          min_value=filteredDataset["Year"].min(),
                          max_value=filteredDataset["Year"].max(),
                          value=[filteredDataset["Year"].min(),filteredDataset["Year"].max()]
                          )

#Filter data according to Year
mask=(filteredDataset["Year"]>=Year[0]) & (filteredDataset["Year"]<=Year[1])
filteredDataset=filteredDataset[mask]

#Add total under instructional Mode
if mode!="Total":
    mask=filteredDataset["Instruction mode"]==mode
    filteredDataset=filteredDataset[mask]


filteredDataset = filteredDataset.groupby(["Course title"]).aggregate({"Fake ID": "count"}).reset_index()
filteredDataset = filteredDataset.rename(columns={"Fake ID": "Students"})


#st.dataframe(filteredDataset)

df = pd.DataFrame(filteredDataset.nlargest(10,"Students"))
#st.dataframe(df)
fig = px.bar(df, x='Course title', y='Students')
st.plotly_chart(fig)

