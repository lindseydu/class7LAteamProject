import streamlit as st
import pandas as pd
import plotly.express as px

StudentCourseSectionInfo = pd.read_csv("data/Student - course section info.csv")
CourseSectionInfo = pd.read_csv("data/Course section info.csv")
StudentCareerInfo = pd.read_csv("data/Student career info.csv")
StudentInfo = pd.read_csv("data/Student info.csv")
StudentTermInfo = pd.read_csv("data/Student term info.csv")

StudentInfo["International student"] = (StudentInfo["International student"]
                                        .replace({"Y": "International", "N": "Local"}))


st.title("Galactic College Learning Insights Dashboard")

# Q1 How many students have received the Pell grant?
st.header(":green[Pell Grant]")
st.sidebar.title("Filters")

joinedDataset = StudentInfo.merge(StudentCareerInfo, on=["Fake ID"], how="left")
joinedDataset = joinedDataset.dropna(subset=["Received Pell grant?", "International student",
                                             "Legal sex", "Marital status", "Race"])

joinedDataset = joinedDataset.drop(columns=["Birth date", "Job Full Time or Part Time", "Average tuition and fees",
                                            "Average disbursed", "Converted high school GPA",
                                            "Converted previous undergraduate GPA", "Years since last formal education",
                                            "Academic plan code", "Degree", "Career number", "Admit term code",
                                            "Admit term", "Total transferred units", "Start effective term",
                                            "Completion term code", "End effective term code", "Semesters",
                                            "Degree awarded", "Start effective term code"])

# Assuming 'Received Pell grant?' contains 'Yes' or 'No' as string values
joinedDataset['Received Pell grant?'] = joinedDataset['Received Pell grant?'].map({'Yes': True, 'No': False})

# Now, you can safely check for True values and group by 'Academic plan'
pell_grant_counts = (joinedDataset[joinedDataset['Received Pell grant?']]
                     .groupby('Academic plan').size().reset_index(name='Count of Pell Grants'))

# Rename Fake ID
joinedDataset = joinedDataset.rename(columns={"Fake ID": "Students"})


# Bar chart for pell grant across all the programs in the college
fig_original = px.bar(pell_grant_counts, x='Academic plan', y='Count of Pell Grants')
fig_original.update_layout(
    title={
        'text': "Count of Pell Grants at Galactic Over the Years",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'bottom'
    },
    title_font_size=24
)
st.plotly_chart(fig_original)

prg = st.sidebar.selectbox("Select the program for which you want to view more details",
                           options=joinedDataset["Academic plan"].unique().tolist())

pell_grant_count = pell_grant_counts[pell_grant_counts["Academic plan"] == prg]["Count of Pell Grants"].values[0]

# Use the function to display text with a larger font (heading 1)


def heading1_text(text, size=20):
    return f'<p style="font-size: {size}px;">{text}</p>'


count_of_pell_grant_prg = f"{pell_grant_count} students received the Pell Grants in the program {prg}"
st.markdown(heading1_text(count_of_pell_grant_prg), unsafe_allow_html=True)

demographic = st.sidebar.radio("Demographic Drill Down", ["Nationality", "Sex", "Race"])

# Demographic Filters
if demographic == 'Nationality':
    fig3 = px.pie(joinedDataset[joinedDataset["Academic plan"] == prg],
                  values="Students", names="International student",
                  title=f"The percentage of international students who received the Pell Grant in {prg}")
    st.plotly_chart(fig3)
elif demographic == 'Sex':
    fig5 = px.pie(joinedDataset[joinedDataset["Academic plan"] == prg], values="Students", names="Legal sex",
                  title=f"The percentage of students who received Pell Grant "
                        f"in {prg} by legal sex")
    st.plotly_chart(fig5)
elif demographic == 'Race':
    fig2 = px.pie(joinedDataset[joinedDataset["Academic plan"] == prg], values="Students", names="Race",
                  title=f"The percentage of students who received Pell Grant in {prg} by race")
    st.plotly_chart(fig2)


# Q2 What are the most popular things?
st.header(":green[What's Popular]")
st.sidebar.title("Filters")
# code for popular course
joinedDatasetPop = StudentCourseSectionInfo.merge(CourseSectionInfo,
                                                  on=["Term code", "Course section number"], how="left")
joinedDatasetPop = joinedDatasetPop.dropna(subset=["Course title"])

aggregatedDataset = joinedDatasetPop.groupby(["Course title", "Term_x",
                                              "Instruction mode"]).aggregate({"Fake ID": "count"}).reset_index()

aggregatedDataset = aggregatedDataset.rename(columns={"Fake ID": "Students"})


# Term filter set up
term = st.sidebar.selectbox("Select Term",
                            options=aggregatedDataset["Term_x"].unique().tolist())

courses_by_term = aggregatedDataset[aggregatedDataset["Term_x"] == term]

# Find the row with the highest number of 'Students'
max_course = courses_by_term.loc[courses_by_term['Students'].idxmax()]

# CSS style for the metric boxes
box_style = "border: 2px solid #ffffff; border-radius: 5px; padding: 10px; text-align: left; margin-bottom: 20px;"

# Display the most popular course and the number of students in a metric card
course_name = max_course['Course title']
num_students = max_course['Students']
st.markdown(f"""
        <div style="{box_style}">
            <h6 style="margin:0; padding:0; font-weight: normal;"> Most Popular Course </h6>
            <h3 style="margin:0; padding:0;">{course_name}</h3>
            <p style="margin:0; padding:0;"><strong>{num_students}</strong> Students</p>
        </div>
        """, unsafe_allow_html=True)

# Display the most popular mode and the number of students in a metric card
mode_name = max_course['Instruction mode']
num_students = max_course['Students']
st.markdown(f"""
        <div style="{box_style}">
            <h6 style="margin:0; padding:0; font-weight: normal;"> Most Popular Mode of Instruction </h6>
            <h3 style="margin:0; padding:0;">{mode_name}</h3>
            <p style="margin:0; padding:0;"><strong>{num_students}</strong> Students</p>
        </div>
        """, unsafe_allow_html=True)

# Code for popular program
joinedDatasetPro = StudentTermInfo.groupby(["Academic plan", "Term"]).aggregate({"Fake ID": "count"}).reset_index()

joinedDatasetPro = joinedDatasetPro.rename(columns={"Fake ID": "Students"})

# Term filter setup for program
programs_by_term = joinedDatasetPro[joinedDatasetPro["Term"] == term]

# Find the row with the highest number of 'Students'
max_program = programs_by_term.loc[programs_by_term['Students'].idxmax()]

# Display the most popular program and the number of students in a metric card
program_name = max_program['Academic plan']
num_students = max_program['Students']
st.markdown(f"""
        <div style="{box_style}">
            <h6 style="margin:0; padding:0; font-weight: normal;"> Most Popular Program </h6>
            <h3 style="margin:0; padding:0;">{program_name}</h3>
            <p style="margin:0; padding:0;"><strong>{num_students}</strong> Students</p>
        </div>
        """, unsafe_allow_html=True)

# Q3 What does “this” program look like??

st.header(":green[Program Insights]")

joinedDatasetINS = StudentTermInfo.merge(StudentCareerInfo, on=["Fake ID",
                                                                "Academic plan", "Academic plan code"], how="left")
joinedDatasetINS = joinedDatasetINS.rename(columns={"Fake ID": "Students"})
joinedDatasetINS['Degree awarded'] = joinedDatasetINS['Degree awarded'].fillna('None')

st.sidebar.title("Filters")

# Graduation rate
term = st.sidebar.selectbox("Select Term",
                            options=joinedDatasetINS["Term"].unique().tolist())
prg = st.sidebar.selectbox("Select Program",
                           options=joinedDatasetINS["Academic plan"].unique().tolist())

filteredDataset = joinedDatasetINS[joinedDatasetINS["Term"] == term]
filteredDataset = filteredDataset[filteredDataset["Academic plan"] == prg]

# Counting for Enrollment
course_counts = StudentTermInfo.groupby(['Academic plan', 'Term']).size().reset_index(name='No of Enrollments')
course_counts.columns = ["Program", "Term", "No of Enrollments"]

course_count_dataset = course_counts[(course_counts["Term"] == term) & (course_counts['Program'] == prg)]

# Get the count for the selected academic plan
selected_count = course_count_dataset["No of Enrollments"].iloc[0]

# Create a graduation dataframe
graduationRate = filteredDataset[["Academic plan", "Degree awarded"]]

graduationRate['Degree awarded'] = (graduationRate['Degree awarded']
                                    .map({'BS': True, 'BA': True, 'AAS': True, 'AA': True, "na": False}))

# Counting degrees awarded
degree_counts = graduationRate.groupby('Academic plan')['Degree awarded'].sum().reset_index(name='Degree awarded')

degree_awarded_count = degree_counts[degree_counts["Academic plan"] == prg]["Degree awarded"].values[0]

# Display the total enrollment for the selected academic plan using st.metric
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
            <div style="{box_style}">                
                <h6 style="margin:0; padding:0;">Total students enrolled</h6>
                <h1 style="margin:0; padding:0;">{selected_count}</h1>
            </div>
            """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
                <div style="{box_style}">                
                    <h6 style="margin:0; padding:0;">No of degrees awarded</h6>
                    <h1 style="margin:0; padding:0;">{degree_awarded_count}</h1>
                </div>
                """, unsafe_allow_html=True)

filteredDataset['Degree awarded'] = (filteredDataset['Degree awarded']
                                     .apply(lambda x: "Graduated" if x != 'None' else "Did not graduate"))

fig = px.pie(filteredDataset, values="Students", names="Degree awarded",
             title="The percentage of students who successfully graduated")

st.plotly_chart(fig)
