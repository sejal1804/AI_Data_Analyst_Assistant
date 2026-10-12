
import streamlit as st
import pandas as pd

st.title("Data Cleaning")
st.subheader("Let's clean your data")

df = st.session_state["df"]

st.dataframe(df)

# Create a flag for checking null values
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

    # Show cleaning options
    column = st.selectbox(
        "Select the column",
        df.columns,
        key="null_column"
    )

    method = st.selectbox(
        "Select how to handle missing values",
        ["Keep", "Mean", "Median", "Mode"],
        key="null_method"
    )

    if st.button("Apply", key="apply_missing_values"):

        if method == "Mean":
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].mean())
            else:
                st.error("Mean can only be applied to numeric columns.")

        elif method == "Median":
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].median())
            else:
                st.error("Median can only be applied to numeric columns.")

        elif method == "Mode":
            modes = df[column].mode()

            if not modes.empty:
                df[column] = df[column].fillna(modes[0])

        st.session_state["df"] = df

        if method == "Keep":
            st.info("Missing values have been kept.")
        else:
            st.success("Missing values handled successfully!")


# Check data types of columns
if "check_for_data_type" not in st.session_state:
    st.session_state["check_for_data_type"] = False

if "change_data_type" not in st.session_state:
    st.session_state["change_data_type"] = False

if st.button("Check data types of columns"):
    st.session_state["check_for_data_type"] = True

if st.session_state["check_for_data_type"]:

    data_types = df.dtypes

    st.write("Current data types")
    st.dataframe(data_types)

    if st.button("Change data types"):
        st.session_state["change_data_type"] = True

    if st.session_state["change_data_type"]:

        column = st.selectbox(
            "Select Column",
            df.columns,
            key="datatype_column"
        )

        datatype = st.selectbox(
            "Select data type",
            ["int", "str", "float", "datetime"],
            key="datatype_choice"
        )

        if st.button("Apply data type", key="apply_data_type"):

            try:
                if datatype == "int":
                    df[column] = pd.to_numeric(
                        df[column], errors="raise"
                    ).astype(int)

                elif datatype == "str":
                    df[column] = df[column].astype(str)

                elif datatype == "float":
                    df[column] = pd.to_numeric(
                        df[column], errors="raise"
                    ).astype(float)

                elif datatype == "datetime":
                    df[column] = pd.to_datetime(
                        df[column], errors="raise"
                    )

                st.session_state["df"] = df

                st.success("Data type changed successfully!")

            except (ValueError, TypeError):
                st.error(
                    "This column cannot be converted to the selected data type."
                )


# Remove columns
if "remove_column" not in st.session_state:
    st.session_state["remove_column"] = False

if st.button("Remove any column"):
    st.session_state["remove_column"] = True

if st.session_state["remove_column"]:

    choice = st.selectbox(
        "Do you want to remove any column?",
        ["No", "Yes"],
        key="remove_column_choice"
    )

    if choice == "Yes" and len(df.columns) > 0:

        column = st.selectbox(
            "Select the column you want to remove",
            df.columns,
            key="column_to_remove"
        )

        if st.button("Remove column", key="confirm_remove_column"):

            df = df.drop(columns=[column])
            st.session_state["df"] = df

            st.success("Column removed successfully!")

    elif choice == "No":
        st.info("No columns will be removed.")


# Remove duplicate records
if "check_duplicates" not in st.session_state:
    st.session_state["check_duplicates"] = False

if st.button("Check for duplicate records"):
    st.session_state["check_duplicates"] = True

if st.session_state["check_duplicates"]:

    duplicate_count = df.duplicated().sum()

    st.write(f"Duplicate records found: {duplicate_count}")

    if duplicate_count > 0:

        if st.button("Remove Duplicates"):

            df = df.drop_duplicates()

            st.session_state["df"] = df

            st.success("Duplicate records removed successfully!")

            st.write(f"Remaining records: {len(df)}")

            st.dataframe(df)

    else:
        st.info("No duplicate records found.")


# Navigate to visualization page
if st.button("Let's visualize your data ->"):
    st.switch_page("pages/02_visualization.py")
