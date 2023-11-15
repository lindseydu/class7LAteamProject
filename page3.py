import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    StudentCareerInfo = pd.read_csv("data/Student career info.csv")
    StudentInfo = pd.read_csv("data/Student info.csv")
    StudentTermInfo = pd.read_csv("data/Student term info.csv")

    StudentInfo["International student"] = (StudentInfo["International student"]
                                            .replace({"Y": "International", "N": "Local"}))

    st.title("Galactic College Learning Insights Dashboard")

    # Q3 What does "this" program look like??

    box_style = "border: 2px solid #ffffff; border-radius: 5px; padding: 10px; text-align: left; margin-bottom: 20px;"

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
