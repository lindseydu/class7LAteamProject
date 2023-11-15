import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    StudentCareerInfo = pd.read_csv("data/Student career info.csv")
    StudentInfo = pd.read_csv("data/Student info.csv")

    StudentInfo["International student"] = (StudentInfo["International student"]
                                            .replace({"Y": "International", "N": "Local"}))

    st.title("Galactic College Learning Insights Dashboard")

    # Q1 How many students have received the Pell grant?
    st.header(":green[Pell Grant]")
    st.sidebar.title("Filters")

    joinedDataset = StudentInfo.merge(StudentCareerInfo, on=["Fake ID"], how="left")
    joinedDataset = joinedDataset.dropna(subset=["Received Pell grant?", "International student",
                                                 "Legal sex", "Marital status", "Race"])

    joinedDataset = joinedDataset.drop(
        columns=["Birth date", "Job Full Time or Part Time", "Average tuition and fees",
                 "Average disbursed", "Converted high school GPA",
                 "Converted previous undergraduate GPA",
                 "Years since last formal education",
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

    prg = st.sidebar.selectbox("Select Program",
                               options=joinedDataset["Academic plan"].unique().tolist())

    pell_grant_count = pell_grant_counts[pell_grant_counts["Academic plan"] == prg]["Count of Pell Grants"].values[
        0]

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
