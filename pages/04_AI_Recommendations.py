import streamlit as st
import pandas as pd
from groq import Groq


# -----------------------------------
# GROQ CLIENT
# -----------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("AI Recommendations")
st.subheader("Get AI-powered recommendations from your data")


# -----------------------------------
# CHECK DATASET
# -----------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()


# Get dataset
df = st.session_state["df"]

st.write("Your dataset is ready for AI analysis.")


# -----------------------------------
# IDENTIFY COLUMN TYPES
# -----------------------------------

numerical_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    exclude="number"
).columns.tolist()


# -----------------------------------
# BUSINESS KEYWORDS
# -----------------------------------

business_keywords = [
    "sales",
    "sale",
    "revenue",
    "profit",
    "amount",
    "price",
    "quantity",
    "qty",
    "cost",
    "income",
    "expense",
    "rating",
    "review",
    "order",
    "orders"
]


# -----------------------------------
# FIND BUSINESS METRIC COLUMNS
# -----------------------------------

metric_columns = []

for column in numerical_columns:

    column_name = column.lower()

    if any(word in column_name for word in business_keywords):
        metric_columns.append(column)


# If no obvious business metric is found,
# use numerical columns except ID-like columns.

if len(metric_columns) == 0:

    for column in numerical_columns:

        column_name = column.lower()

        if not any(word in column_name for word in [
            "id",
            "code",
            "zip",
            "postal",
            "latitude",
            "longitude"
        ]):

            metric_columns.append(column)


# -----------------------------------
# CREATE BUSINESS FINDINGS
# -----------------------------------

findings = []

for metric in metric_columns:

    for category in categorical_columns:

        category_name = category.lower()

        # Ignore columns unlikely to provide
        # useful business grouping.

        if any(word in category_name for word in [
            "id",
            "address",
            "phone",
            "email",
            "name"
        ]):

            continue


        # Avoid very high-cardinality columns

        if df[category].nunique() > 50:
            continue


        try:

            grouped_data = df.groupby(category)[metric].sum()

            if len(grouped_data) > 1:

                highest_category = grouped_data.idxmax()
                highest_value = grouped_data.max()

                lowest_category = grouped_data.idxmin()
                lowest_value = grouped_data.min()

                finding = (
                    f"{highest_category} has the highest total "
                    f"{metric} with {highest_value:.2f}. "
                    f"{lowest_category} has the lowest total "
                    f"{metric} with {lowest_value:.2f}."
                )

                findings.append(finding)

        except Exception:
            continue


# -----------------------------------
# REMOVE DUPLICATE FINDINGS
# -----------------------------------

findings = list(dict.fromkeys(findings))


# -----------------------------------
# DISPLAY BUSINESS FINDINGS
# -----------------------------------

st.subheader("Business Findings")

if findings:

    for finding in findings[:5]:

        st.write("•", finding)

else:

    st.info(
        "No meaningful business findings could be "
        "identified from this dataset."
    )


# -----------------------------------
# GENERATE AI RECOMMENDATIONS
# -----------------------------------

if findings:

    if st.button("Generate AI Recommendations"):

        findings_text = "\n".join(
            f"- {finding}"
            for finding in findings[:5]
        )


        # -----------------------------------
        # AI PROMPT
        # -----------------------------------

        prompt = f"""
You are a business data analyst.

The Python analysis of a user's dataset produced
the following factual findings:

{findings_text}

Based ONLY on these findings:

1. Give 2 practical business recommendations.
2. Give 2 areas the business should investigate further.

Rules:
- Do not invent information.
- Do not assume facts that are not present.
- Keep recommendations practical.
- Clearly distinguish recommendations from findings.
- Keep the response concise.
"""


        # -----------------------------------
        # SEND FINDINGS TO GROQ AI
        # -----------------------------------

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )


            # -----------------------------------
            # DISPLAY AI RESPONSE
            # -----------------------------------

            st.subheader("AI Recommendations")

            st.write(
                response.choices[0].message.content
            )


        except Exception as e:

            st.error(
                "Unable to connect to Groq AI."
            )

            st.code(str(e))