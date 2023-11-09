import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv("loan.csv")

# Streamlit App
st.title("Loan Data Dashboard")

# Sidebar Filters
st.sidebar.subheader("Filters")
filter_option = st.sidebar.radio("Filter by Loan Status:", ['Y', 'N', 'All'], index=2)

# Data Filtering
if filter_option == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Loan_Status'] == filter_option]

property_area = st.sidebar.selectbox("Select Property Area:", df['Property_Area'].unique())
filtered_by_area_df = df[df['Property_Area'] == property_area]

# Main Content
st.subheader("Filtered Data")
st.dataframe(filtered_df)

st.subheader("Filtered Data by Property Area")
st.dataframe(filtered_by_area_df)

st.subheader("Descriptive Statistics")
st.write(filtered_df.describe())

# Create columns for side-by-side visualization
col1, col2 = st.columns(2)

# Dropdown for selecting columns
#selected_column_bar = col1.selectbox("Select a column for Bar Chart:", df.columns[:-1])
#selected_column_pie = col2.selectbox("Select a column for Pie Chart:", df.columns[:-1])
chart_columns = ["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]
selected_column_bar = col1.selectbox("Select a column for Bar Chart:", chart_columns)
selected_column_pie = col2.selectbox("Select a column for Pie Chart:", chart_columns)

# Bar Chart
bar_fig, bar_ax = plt.subplots()
sns.countplot(x=selected_column_bar, data=filtered_df, ax=bar_ax)
bar_ax.set_title(f"Bar Chart for {selected_column_bar}")
col1.pyplot(bar_fig)

# Pie Chart
pie_fig, pie_ax = plt.subplots()
filtered_df[selected_column_pie].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=pie_ax)
pie_ax.set_title(f"Pie Chart for {selected_column_pie}")
col2.pyplot(pie_fig)

scatter_columns= ["ApplicantIncome","CoapplicantIncome","LoanAmount"]
# Dropdown for selecting columns for distribution plot
selected_column_dist_applicant = st.selectbox("Select a column for Distribution Plot (Applicant Income):", scatter_columns)

# Distribution Plot for Applicant Income
st.subheader(f"Distribution Plot for {selected_column_dist_applicant}")
fig, ax = plt.subplots()
sns.histplot(filtered_df[selected_column_dist_applicant], bins=20, kde=True, color='blue', ax=ax)
ax.set_xlabel(selected_column_dist_applicant)
ax.set_ylabel('Frequency')
st.pyplot(fig)

# Bivariate Analysis
st.subheader("Bivariate Analysis")
# Create columns for side-by-side dropdowns
col1, col2 = st.columns(2)

# Dropdown for selecting the first column
selected_column1 = col1.selectbox("Select the first column for analysis:", ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"])

# Dropdown for selecting the second column
selected_column2 = col2.selectbox("Select the second column for analysis:", ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Property_Area"])

# Pair plot for numerical columns
if selected_column1 in ['ApplicantIncome', 'CoapplicantIncome'] and selected_column2 in ['ApplicantIncome', 'CoapplicantIncome']:
    pair_fig = sns.pairplot(df, hue='Loan_Status', palette='viridis')
    st.pyplot(pair_fig)
else:
    # Count plot for categorical columns
    count_fig, count_ax = plt.subplots()
    sns.countplot(x=selected_column1, hue=selected_column2, data=df, ax=count_ax)
    count_ax.set_title(f"Count Plot for {selected_column1} vs {selected_column2}")
    st.pyplot(count_fig)


# Correlation Matrix Heatmap
st.subheader("Correlation Matrix")
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
st.pyplot()

# Add some spacing for aesthetics
st.markdown("---")

# Footer
st.sidebar.markdown(
    "#### About\n"
    "This dashboard is designed to explore and analyze loan data using Streamlit, "
    "Seaborn, and Matplotlib."
)
