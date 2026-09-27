import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Visualize your data")
st.subheader("Let's get the view of data in form of graphs and charts")


df = st.session_state["df"]

st.dataframe(df)


selected_columns = st.sidebar.multiselect(
    "Select column(s)",
    df.columns,
    max_selections=2
)

st.write("<- To select columns for visualization see the slidebar on the left")


# =========================================================
# ONE COLUMN SELECTED
# =========================================================

if len(selected_columns) == 1:

    column = selected_columns[0]

    # -----------------------------------------------------
    # Numerical column → Histogram
    # -----------------------------------------------------

    if pd.api.types.is_numeric_dtype(df[column]):

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Observation

        average = df[column].mean()
        maximum = df[column].max()
        minimum = df[column].min()

        st.subheader("Observation")

        st.write(
            f"The average {column} is {average:.2f}. "
            f"The highest value is {maximum:.2f}, "
            f"while the lowest value is {minimum:.2f}."
        )


    # -----------------------------------------------------
    # Categorical column → Pie chart
    # -----------------------------------------------------

    else:

        counts = df[column].value_counts()

        fig = px.pie(
            counts,
            names=counts.index,
            values=counts.values,
            title=f"Distribution of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Observation

        most_common = counts.idxmax()
        highest_count = counts.max()

        least_common = counts.idxmin()
        lowest_count = counts.min()

        st.subheader("Observation")

        st.write(
            f"{most_common} is the most common category with "
            f"{highest_count} records, while {least_common} "
            f"is the least common with {lowest_count} records."
        )


# =========================================================
# TWO COLUMNS SELECTED
# =========================================================

elif len(selected_columns) == 2:

    x_column = selected_columns[0]
    y_column = selected_columns[1]

    x_is_numeric = pd.api.types.is_numeric_dtype(df[x_column])
    y_is_numeric = pd.api.types.is_numeric_dtype(df[y_column])


    # =====================================================
    # BOTH NUMERICAL → LINE CHART
    # =====================================================

    if x_is_numeric and y_is_numeric:

        fig = px.line(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Observation

        highest_value = df[y_column].max()
        lowest_value = df[y_column].min()
        average_value = df[y_column].mean()

        st.subheader("Observation")

        st.write(
            f"The average {y_column} is {average_value:.2f}. "
            f"The highest value is {highest_value:.2f}, "
            f"while the lowest value is {lowest_value:.2f}."
        )


    # =====================================================
    # ONE NUMERICAL + ONE CATEGORICAL → BAR CHART
    # =====================================================

    elif x_is_numeric != y_is_numeric:

        # If X is numerical and Y is categorical,
        # swap them.

        if x_is_numeric and not y_is_numeric:
            x_column, y_column = y_column, x_column

        # Now:
        # x_column → categorical
        # y_column → numerical

        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} by {x_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Observation

        grouped_data = df.groupby(x_column)[y_column].sum()

        highest_category = grouped_data.idxmax()
        highest_value = grouped_data.max()

        lowest_category = grouped_data.idxmin()
        lowest_value = grouped_data.min()

        st.subheader("Observation")

        st.write(
            f"{highest_category} has the highest total {y_column} "
            f"with {highest_value:.2f}, while {lowest_category} "
            f"has the lowest total with {lowest_value:.2f}."
        )


    # =====================================================
    # BOTH CATEGORICAL → GROUPED BAR CHART
    # =====================================================

    else:

        grouped_data = df.groupby(
            [x_column, y_column]
        ).size().reset_index(name="count")

        fig = px.bar(
            grouped_data,
            x=x_column,
            y="count",
            color=y_column,
            barmode="group",
            title=f"{x_column} vs {y_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Observation

        highest_row = grouped_data.loc[
            grouped_data["count"].idxmax()
        ]

        lowest_row = grouped_data.loc[
            grouped_data["count"].idxmin()
        ]

        highest_x = highest_row[x_column]
        highest_y = highest_row[y_column]
        highest_count = highest_row["count"]

        lowest_x = lowest_row[x_column]
        lowest_y = lowest_row[y_column]
        lowest_count = lowest_row["count"]

        st.subheader("Observation")

        st.write(
            f"The combination of {highest_x} and {highest_y} "
            f"has the highest number of records with "
            f"{highest_count} observations. "
            f"The combination of {lowest_x} and {lowest_y} "
            f"has the lowest with {lowest_count} observations."
        )


if st.button("Get Overall insights and recommendations ->"):
    st.switch_page("pages/03_Insights_observations.py")
