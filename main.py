import streamlit as st
import pandas as pd
import plotly.express as px

StudentCourseSectionInfo = pd.read_csv("data/Student - course section info.csv")
CourseSectionInfo = pd.read_csv("data/Course section info.csv")
StudentCareerInfo = pd.read_csv("data/Student career info.csv")
StudentInfo = pd.read_csv("data/Student info.csv")
StudentTermInfo = pd.read_csv("data/Student term info.csv")

st.write("Student Course Section Info")
st.dataframe(StudentCourseSectionInfo)
st.write("Course Section Info")
st.dataframe(CourseSectionInfo)
st.write("Student Career Info")
st.dataframe(StudentCareerInfo)
st.write("Student Info")
st.dataframe(StudentInfo)
st.write("Student Term Info")
st.dataframe(StudentTermInfo)