import streamlit as st
import pandas as pd
import plotly.express as px

StudentCourseSectionInfo = pd.read_csv("data/Student - course section info.csv")
CourseSectionInfo = pd.read_csv("data/Course section info.csv")
StudentCareerInfo = pd.read_csv("data/Student career info.csv")
StudentInfo = pd.read_csv("data/Student info.csv")
StudentTermInfo = pd.read_csv("data/Student term info.csv")

StudentInfo["International student"]= StudentInfo["International student"].replace({"Y": "Yes", "N": "No","":"Unknown"})


st.title("Galactic College Learning Insights Dashboard")

joinedDataset = StudentInfo.merge(StudentCareerInfo,on=["Fake ID"], how="left")
joinedDataset = joinedDataset.dropna(subset=["Received Pell grant?","International student","Legal sex","Marital status","Race"])
joinedDataset = pd.DataFrame(joinedDataset)

joinedDataset = joinedDataset.drop(columns=["Birth date", "Job Full Time or Part Time", "Average tuition and fees", "Average disbursed", "Converted high school GPA", "Converted previous undergraduate GPA", "Years since last formal education", "Academic plan code", "Degree", "Career number", "Admit term code", "Admit term", "Total transferred units", "Start effective term", "Completion term code", "End effective term code", "Semesters", "Degree awarded", "Start effective term code"])

# Assuming 'Received Pell grant?' contains 'Yes' or 'No' as string values
joinedDataset['Received Pell grant?'] = joinedDataset['Received Pell grant?'].map({'Yes': True, 'No': False})

# Now, you can safely check for True values and group by 'Academic plan'
pell_grant_counts = joinedDataset[joinedDataset['Received Pell grant?']].groupby('Academic plan').size().reset_index(name='Count of Pell Grants')

#Rename Fake ID
joinedDataset = joinedDataset.rename(columns={"Fake ID":"Students"})


# Plot
fig_original = px.bar(pell_grant_counts, x='Academic plan', y='Count of Pell Grants')
st.plotly_chart(fig_original)

prg = st.selectbox("Select Program",
                       options= joinedDataset["Academic plan"].unique().tolist())

pell_grant_count = pell_grant_counts[pell_grant_counts["Academic plan"]==prg]["Count of Pell Grants"].values[0]

# Use the function to display text with a larger font
def large_text(text, size=20):
    return f'<p style="font-size: {size}px;">{text}</p>'
count_of_pell_grant_prg= f"Count of Pell Grants for {prg} is {pell_grant_count}"
st.markdown(large_text(count_of_pell_grant_prg), unsafe_allow_html=True)


demographic = st.radio("Demographic Drill Down", ["Nationality","Sex","Race"], index=None)


# Demographic Filters
if demographic == 'Nationality':
    fig3 = px.pie(joinedDataset[joinedDataset["Academic plan"]==prg], values="Students", names="International student",
                  title=f"The population of international students who received the grant of {prg}")
    st.plotly_chart(fig3)
elif demographic == 'Sex':
    fig5 = px.pie(joinedDataset[joinedDataset["Academic plan"]==prg], values="Students", names="Legal sex",
                  title=f"The percentage of legal sex of students who recerive the grant of {prg}")
    st.plotly_chart(fig5)
elif demographic == 'Race':
    fig2 = px.pie(joinedDataset[joinedDataset["Academic plan"]==prg], values="Students", names="Race",
                  title=f"The race of students who received the grant of {prg}")
    st.plotly_chart(fig2)

# code for popular course
joinedDatasetPop = StudentCourseSectionInfo.merge(CourseSectionInfo, on=["Term code", "Course section number"], how="left")
joinedDatasetPop = joinedDatasetPop.dropna(subset=["Course title"])
st.dataframe(joinedDatasetPop)

aggregatedDataset = joinedDatasetPop.groupby(["Course title","Term_x"]).aggregate({"Fake ID":"count"}).reset_index()

aggregatedDataset = aggregatedDataset.rename(columns={"Fake ID":"Students"})

st.dataframe(aggregatedDataset)

# Find the row with the maximum 'Students' value
max_value = aggregatedDataset.loc[aggregatedDataset['Students'].idxmax()]

# Display the most popular course and the number of students in a metric card
course_name = max_value['Course title']
num_students = max_value['Students']
st.write("Most Popular Courses")
st.metric(label=course_name, value=num_students)

# code for popular program
#joinedDatasetPro = StudentCourseSectionInfo.merge(CourseSectionInfo, on=["Term code", ""])