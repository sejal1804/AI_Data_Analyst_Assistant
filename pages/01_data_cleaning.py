import streamlit as st
import pandas as pd

st.title("Data Cleaning")
st.subheader("Let's clean your data")

df = st.session_state["df"]

st.dataframe(df)

# Create a flag
if "check_nulls" not in st.session_state:
    st.session_state["check_nulls"] = False

# Check for null values
if st.button("Check for null values"):
    st.session_state["check_nulls"] = True

# Show missing values after button is clicked
if st.session_state["check_nulls"]:

    missing_values = df.isnull().sum()

    missing_data = pd.DataFrame({
        "Columns": missing_values.index,
        "Null_values": missing_values.values
    })

    st.write("Missing Values")
    st.dataframe(missing_data)

    # Now show the cleaning options
    column = st.selectbox(
        "Select the column",
        df.columns
    )

    method = st.selectbox(
        "Select how to handle missing values",
        ["Keep", "Mean", "Median", "Mode"]
    )

    if st.button("Apply"):

        if method == "Mean":
            df[column] = df[column].fillna(df[column].mean())

        elif method == "Median":
            df[column] = df[column].fillna(df[column].median())

        elif method == "Mode":
            df[column] = df[column].fillna(df[column].mode()[0])

        st.session_state["df"] = df

        st.success("Missing values handled successfully!")

# Create a flag for duplicates
if "check_for_data_type" not in st.session_state:
    st.session_state["check_for_data_type"] = False

if "change_data_type" not in st.session_state:
    st.session_state["change_data_type"] = False


if st.button("Check data types of columns"):
    st.session_state["check_for_data_type"] = True


if st.session_state["check_for_data_type"]:

    data_types = df.dtypes
    st.dataframe(data_types)

    if st.button("Change data types"):
        st.session_state["change_data_type"] = True


    if st.session_state["change_data_type"]:

        column = st.selectbox(
            "Select Column",
            df.columns
        )

        datatype = st.selectbox(
            "Select data type",
            ["int", "str", "float", "datetime"]
        )

        if st.button("Apply data type"):

            try:

                if datatype == "int":
                    df[column] = df[column].astype(int)

                elif datatype == "str":
                    df[column] = df[column].astype(str)

                elif datatype == "float":
                    df[column] = df[column].astype(float)

                elif datatype == "datetime":
                    df[column] = pd.to_datetime(df[column])

                st.session_state["df"] = df

                st.success("Data type changed successfully!")

            except ValueError:
                st.error(
                    "This column cannot be converted to the selected data type."
                )


# Create a flag for removing column

if "remove_column" not in st.session_state:
    st.session_state["remove_column"] = False

if st.button("Remove any column"):
    st.session_state["remove_column"] = True

if st.session_state["remove_column"]:

    choice = st.selectbox(
        "Do you want to remove any column?",
        ["No", "Yes"]
    )

    if choice == "Yes":

        column = st.selectbox(
            "Select the column you want to remove",
            df.columns
        )

        if st.button("Remove column"):
            df = df.drop(columns=[column])
            st.session_state["df"] = df

            st.success("Column removed successfully!")

    elif choice == "No":
        st.info("No columns will be removed.")

if st.button("Lets visualize your data ->"):
    st.switch_page("pages/02_visualization.py")