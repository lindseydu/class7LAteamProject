import streamlit as st
import pandas as pd


def show():
    StudentCourseSectionInfo = pd.read_csv("data/Student - course section info.csv")
    CourseSectionInfo = pd.read_csv("data/Course section info.csv")
    StudentInfo = pd.read_csv("data/Student info.csv")
    StudentTermInfo = pd.read_csv("data/Student term info.csv")

    StudentInfo["International student"] = (StudentInfo["International student"]
                                            .replace({"Y": "International", "N": "Local"}))

    st.title("Galactic College Learning Insights Dashboard")

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
