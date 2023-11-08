import streamlit as st
import pandas as pd
import plotly.express as px

StudentCourseSectionInfo = pd.read_csv("data/Student - course section info.csv")
CourseSectionInfo = pd.read_csv("data/Course section info.csv")
StudentCareerInfo = pd.read_csv("data/Student career info.csv")
StudentInfo = pd.read_csv("data/Student info.csv")
StudentTermInfo = pd.read_csv("data/Student term info.csv")

st.title("Galactic College Learning Insights Dashboard")

joinedDataset = StudentInfo.merge(StudentCareerInfo,on=["Fake ID"], how="left")
joinedDataset = joinedDataset.dropna(subset=["Received Pell grant?"])
joinedDataset = pd.DataFrame(joinedDataset)

joinedDataset = joinedDataset.drop(columns=["Birth date", "Job Full Time or Part Time", "Average tuition and fees", "Average disbursed", "Converted high school GPA", "Converted previous undergraduate GPA", "Years since last formal education", "Academic plan code", "Degree", "Career number", "Admit term code", "Admit term", "Total transferred units", "Start effective term", "Completion term code", "End effective term code", "Semesters", "Degree awarded", "Start effective term code"])

# Assuming 'Received Pell grant?' contains 'Yes' or 'No' as string values
joinedDataset['Received Pell grant?'] = joinedDataset['Received Pell grant?'].map({'Yes': True, 'No': False})

# Now, you can safely check for True values and group by 'Academic plan'
pell_grant_counts = joinedDataset[joinedDataset['Received Pell grant?']].groupby('Academic plan').size().reset_index(name='Count of Pell Grants')

#Rename Fake ID
joinedDataset = joinedDataset.rename(columns={"Fake ID":"Students"})

# Plot
fig = px.bar(pell_grant_counts, x='Academic plan', y='Count of Pell Grants')
st.plotly_chart(fig)


# Demographic Filters
demographic = st.radio("Demographic Drill Down", ["Nationality","Sex","Race"], index=None)

if demographic == 'Nationality':
    fig3 = px.pie(joinedDataset, values="Students", names="International student",
                  title="The population of international students who received the grant")
    st.plotly_chart(fig3)
elif demographic == 'Sex':
    fig5 = px.pie(joinedDataset, values="Students", names="Legal sex",
                  title="The percentage of legal sex of students who recerive the grant")
    st.plotly_chart(fig5)
elif demographic == 'Race':
    fig2 = px.pie(joinedDataset, values="Students", names="Race",
                  title="The race of students who received the grant")
    st.plotly_chart(fig2)