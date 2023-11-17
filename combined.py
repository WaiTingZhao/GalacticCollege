import streamlit as st
import pandas as pd
import plotly.express as px

# Create Interface
st.set_page_config(layout="wide")
genre = st.sidebar.radio(
    "Select The Questions",
    ["Question 1: Popular Courses", "Question 2: Graduation Rates", "Question 3: Grade Distribution"],
    captions = ["View the popular courses.", "View the graduation rates.", "View the grade distribution."])


if genre == 'Question 1: Popular Courses':

    # Load your datasets
    courseData = pd.read_csv("Course section info.csv")
    studentCourse = pd.read_csv("Student - course section info.csv")
    studentCareer = pd.read_csv("Student career info.csv")
    studentInfo = pd.read_csv("Student info.csv")
    studentTerm = pd.read_csv("Student term info.csv")

    # Merging the data from courseData and studentCourse
    joinedDataset = studentCourse.merge(courseData, on=["Term code", "Course section number"], how="left")
    # st.write(joinedDataset)
    joinedDataset = joinedDataset.dropna(subset=["Course title"])
    aggregatedDataset = joinedDataset.groupby(
        ["Course title", "Term code", "Course section number", "Instruction mode"]).aggregate(
        {"Fake ID": "count"}).reset_index()
    # st.write(aggregatedDataset)

    # Remove all the grade results of "F" and "W"
    # Remove all the Course number with "None"
    grade_column = 'Grade'
    joinedDataset[grade_column] = joinedDataset[grade_column].str.strip().str.upper()
    filteredDataset = joinedDataset[~joinedDataset[grade_column].isin(['F', 'W'])]

    # Only keep "In-Person", "Online", "Online Hybrid", "Independent Studies" under the column of Instruction mode.
    # Change "Online Hybrid" into "Blended"
    instruction_mode_column = 'Instruction mode'
    filteredDataset[instruction_mode_column] = filteredDataset[instruction_mode_column].str.replace("Online Hybrid",
                                                                                                    "Blended (Online & In-Person)")
    st.title("Top 10 Popular Courses")
    st.sidebar.title("Filters")

    # Rename Fake ID to 'Students',converted term_x to year.
    filteredDataset["Year"] = filteredDataset["Term_x"].str.split().str[1]
    filteredDataset["Year"] = pd.to_numeric(filteredDataset["Year"])

    # Select the Visualization
    mode = st.sidebar.radio("Choose an Instruction Mode",
                            options=["In-Person",
                                     "Blended (Online & In-Person)",
                                     "Online",
                                     "Independent Studies",
                                     "Total"])

    Year = st.sidebar.slider("Choose your range:",
                             min_value=filteredDataset["Year"].min(),
                             max_value=filteredDataset["Year"].max(),
                             value=[filteredDataset["Year"].min(), filteredDataset["Year"].max()]
                             )

    # Filter data according to Year
    mask = (filteredDataset["Year"] >= Year[0]) & (filteredDataset["Year"] <= Year[1])
    filteredDataset = filteredDataset[mask]

    # Add total under instructional Mode
    if mode != "Total":
        mask = filteredDataset["Instruction mode"] == mode
        filteredDataset = filteredDataset[mask]

    filteredDataset = filteredDataset.groupby(["Course title"]).aggregate({"Fake ID": "count"}).reset_index()
    filteredDataset = filteredDataset.rename(columns={"Fake ID": "Students"})

    # st.dataframe(filteredDataset)

    df = pd.DataFrame(filteredDataset.nlargest(10, "Students"))
    # st.dataframe(df)
    fig = px.bar(df, x='Course title', y='Students')
    st.plotly_chart(fig)

elif genre == 'Question 2: Graduation Rates':

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
    studentCareer['Graduated'] = studentCareer['Degree awarded'].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() else 0)

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

    # Conditionally display multiselector only when "Academic Plan" is selected
    if selection == 'Academic Plan':
        # Multiselect widget for academic plans with default as all plans selected
        default_academic_plans = studentCareer['Academic plan'].unique()
        selected_academic_plans = st.sidebar.multiselect('Select Academic Plans', default_academic_plans,
                                                         default_academic_plans)
    else:
        selected_academic_plans = None

    # Filter the data based on the selected year range and academic plans
    filtered_data = studentCareer[(studentCareer['Start effective year'] >= selected_year_range[0]) &
                                  (studentCareer['Start effective year'] <= selected_year_range[1])]

    # Apply additional filter for academic plans if selected
    if selected_academic_plans is not None:
        filtered_data = filtered_data[filtered_data['Academic plan'].isin(selected_academic_plans)]

    # Group by selected category
    if selection == 'Degree':
        # Extract the selected year range from the tuple
        start_year, end_year = selected_year_range

        grouped_data = filtered_data.groupby('Degree')
        title = 'Graduation Rate Based on Degree By Percentage %'
        caption = f"Below displays the Graduation Rate based on Degree by percentage % within the specified year range from {start_year} to {end_year}."
    elif selection == 'Academic Plan':
        grouped_data = filtered_data.groupby('Academic plan')
        title = 'Graduation Rate Based on Academic Plan'
        caption = ""  # You can customize the caption for Academic Plan if needed

    # Calculate graduation rate
    graduated_count = grouped_data['Graduated'].sum()
    enrolled_count = grouped_data['Enrolled'].sum()
    graduation_rate = graduated_count / enrolled_count * 100
    graduation_rate = graduation_rate.round(2)  # Round to 2 decimal points

    # Create a DataFrame for Plotly with rounded values
    graduation_rate_df = pd.DataFrame({
        'Group': graduation_rate.index,
        'Graduation Rate': graduation_rate.values.round(2)  # Round to 2 decimal points
    })

    # Display the results using Plotly with inverted axes
    fig = px.bar(graduation_rate_df, x='Graduation Rate', y='Group',
                 text=graduation_rate_df['Graduation Rate'].apply(lambda x: f'{x:.2f}%'),
                 labels={'Graduation Rate': 'Graduation Rate (%)'})
    fig.update_layout(title=title, xaxis_title='Graduation Rate (%)', yaxis_title=selection)

    # Display the Plotly chart
    st.plotly_chart(fig)

else:
    st.title("Grade Distribution Pie Chart")
    # open the data
    courseData = pd.read_csv("Course section info.csv")
    studentCourse = pd.read_csv("Student - course section info.csv")
    studentCareer = pd.read_csv("Student career info.csv")
    studentInfo = pd.read_csv("Student info.csv")
    studentTerm = pd.read_csv("Student term info.csv")

    # Merging the data from courseData and studentCourse
    joinedDataset = studentCourse.merge(courseData, on=["Term code", "Course section number"], how="left")
    joinedDataset = joinedDataset.dropna(subset=["Course title"])
    aggregatedDataset = joinedDataset.groupby(["Course title", "Term_x", "Grade"]).aggregate(
        {"Fake ID": "count"}).reset_index()

    # Convert terms to years
    aggregatedDataset["Year"] = aggregatedDataset["Term_x"].str.split().str[1]
    aggregatedDataset["Year"] = pd.to_numeric(aggregatedDataset["Year"])

    # Create a sidebar for course selection
    selected_course = st.sidebar.selectbox("Select a Course", aggregatedDataset['Course title'].unique())

    # Create a sidebar for year selection
    selected_year_range = st.sidebar.slider(
        "Select a Year Range",
        min_value=int(aggregatedDataset["Year"].min()),
        max_value=int(aggregatedDataset["Year"].max()),
        value=(int(aggregatedDataset["Year"].min()), int(aggregatedDataset["Year"].max()))
    )

    # Filter the data for the selected course and year range
    selected_data = aggregatedDataset[(aggregatedDataset['Course title'] == selected_course) &
                                      (aggregatedDataset['Year'] >= selected_year_range[0]) &
                                      (aggregatedDataset['Year'] <= selected_year_range[1])]

    # Group by grade and calculate the count for the selected course and year range
    grade_distribution_selected_data = selected_data.groupby('Grade').size().reset_index(name='Count')

    grade_distribution_selected_data["Grade"] = grade_distribution_selected_data['Grade'].astype('category')
    grade_distribution_selected_data["Grade"] = grade_distribution_selected_data['Grade'].cat.reorder_categories(
        ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F', 'W'])
    order = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F', 'W']

    # Calculate percentages
    total_count = grade_distribution_selected_data['Count'].sum()
    grade_distribution_selected_data['Percentage'] = (grade_distribution_selected_data['Count'] / total_count) * 100

    # Create a caption
    st.write(
        f"## Grade Distribution for {selected_course} within the Year ({selected_year_range[0]} - {selected_year_range[1]})")

    # Create a pie chart for the selected course's grade distribution
    fig_selected_course_pie = px.pie(grade_distribution_selected_data, values='Percentage', names='Grade',
                                     category_orders={"Grade": order},
                                     # title=f'Grade Distribution for {selected_course} ({selected_year_range[0]} - {selected_year_range[1]})',
                                     hole=0.3)

    # Set category order for the legend (letter grades)
    fig_selected_course_pie.update_layout(
        legend=dict(traceorder='normal'),
        legend_title="Grades",
    )

    # Display the pie chart
    st.plotly_chart(fig_selected_course_pie)


