import streamlit as st
import pandas as pd

st.title("Overall Business Insights")
st.subheader("Key Business Findings")

df = st.session_state["df"]

numerical_columns = df.select_dtypes(include="number").columns
categorical_columns = df.select_dtypes(exclude="number").columns

business_insights = []

business_keywords = [
    "sales",
    "revenue",
    "profit",
    "amount",
    "price",
    "quantity",
    "orders",
    "order",
    "rating",
    "reviews",
    "cost"
]

ignore_columns = [
    "id",
    "customer_id",
    "order_id",
    "product_id",
    "postal_code",
    "latitude",
    "longitude"
]

metric_columns = []

for column in numerical_columns:

    column_name = column.lower()

    if any(word in column_name for word in business_keywords):
        metric_columns.append(column)

    elif any(word in column_name for word in ignore_columns):
        continue


for metric in metric_columns:

    for category in categorical_columns:

        category_name = category.lower()

        if any(word in category_name for word in [
            "name",
            "id",
            "address",
            "phone",
            "email"
        ]):
            continue

        grouped_data = df.groupby(category)[metric].sum()

        if len(grouped_data) > 1:

            highest_category = grouped_data.idxmax()
            highest_value = grouped_data.max()

            business_insights.append(
                f"{highest_category} generates the highest "
                f"total {metric} with {highest_value:.2f}."
            )


if business_insights:

    for insight in business_insights[:5]:
        st.write(f"• {insight}")

else:

    st.info(
        "No meaningful business insights could be identified "
        "from the available business metrics."
    )

if st.button("Get Recommendations"):
    st.switch_page("pages/04_AI_Recommendations.py")