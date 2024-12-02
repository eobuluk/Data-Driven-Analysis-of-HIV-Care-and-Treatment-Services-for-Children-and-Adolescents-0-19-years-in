import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the data
file_path = '/Users/mac/Desktop/VL_Data.csv'
data = pd.read_csv(file_path)

# Viewing the first few rows
print(data.head())

#  Overview of the dataset##
# Check column types and null values
print(data.info())
# Summary statistics for numeric and categorical data
print(data.describe(include='all'))

# Cleaning the dataset ##
# Step 1: Standardizing column names
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

# Step 2: Replacing 'NE' (Not Evaluated) and blanks with NaN for missing values
data = data.replace('NaN', pd.NA)

# Step 3: Converting relevant columns to numeric or categorical types
# Convert 'age' to numeric
data['age'] = pd.to_numeric(data['age'], errors='coerce')
# Convert MMD months to numeric
data['mmdmonths'] = pd.to_numeric(data['mmdmonths'], errors='coerce')

# Step 4: Check for missing values (count missing values in each column)
print(data.isnull().sum())


# Data Analysis Exploration
# Age Distribution of Patients
plt.figure(figsize=(8, 5))
sns.histplot(data['age'], bins=10, kde=True, color='blue')
plt.title('Age Distribution of Patients')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

# ART Regimen Line Distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=data, x='current_art_regimen_line', palette='Set2')
plt.title('ART Regimen Line Distribution')
plt.xlabel('ART Regimen Line')
plt.ylabel('Count')
plt.show()

# Viral Load Updated Status
vl_updated_counts = data['vl_updated_(y/n/ne)'].value_counts()
print("VL Updated Counts:\n", vl_updated_counts)
vl_updated_counts.plot(kind='bar', color=['green', 'orange', 'red'])
plt.title('Viral Load Updated Status')
plt.xlabel('Viral Load Status')
plt.ylabel('Number of Patients')
plt.show()


# Identify Gaps and Trends ##

# Patients eligible but not enrolled in OVC programs
ovc_gap = data[(data['screened_for_ovc'] == 'Screened and Eligible') &
               (data['eligible_and_enrolled_in_ovc'] == 'NOT ENROLLED')]
print(f"Number of patients eligible but not enrolled in OVC: {len(ovc_gap)}")

# Patients not on optimal ART regimens
non_optimal = data[data['optimization'] != 'Opt']
print(f"Number of patients not on optimal ART regimens: {len(non_optimal)}")

# Count of VL suppression
vl_suppression_counts = data['vl_suppression'].value_counts()
print("VL Suppression Counts:\n", vl_suppression_counts)


# Visualize Findings

# Gap in OVC Enrollment
plt.figure(figsize=(8, 5))
ovc_gap['district'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Gap in OVC Enrollment by District')
plt.xlabel('District')
plt.ylabel('Number of Patients')
plt.show()

# VL Suppression
plt.figure(figsize=(8, 5))
vl_suppression_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['green', 'yellow', 'red'])
plt.title('Viral Load Suppression Status')
plt.ylabel('')
plt.show()


# Summary Table of Key Metrics ##

# Calculate key metrics
total_patients = len(data)
optimal_art_regimens = (data['optimization'] == 'Opt').sum()
vl_updated = (data['vl_updated_(y/n/ne)'] == 'y').sum()

# Create summary table
summary = {
    'Total Patients': total_patients,
    '% on Optimal ART Regimens': (optimal_art_regimens / total_patients) * 100,
    '% with VL Updated': (vl_updated / total_patients) * 100,
}

# Convert to DataFrame for display
summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
print(summary_df)
