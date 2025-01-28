import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files
import requests

# Download the CSV file (if not already downloaded)
url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/user_behavior_dataset-UxLrK4gd7ptajTBnAzeAngHpdJ56cn.csv"
response = requests.get(url)
with open("user_behavior_dataset.csv", "wb") as f:
    f.write(response.content)

# Load the dataset
df = pd.read_csv("user_behavior_dataset.csv")

# 1. Summary Statistics
print("Summary Statistics:")
print(df.describe())

# 2. Data Visualization

# Set up the plotting style
plt.style.use('seaborn')
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

# Histogram of App Usage Time
sns.histplot(data=df, x='App Usage Time (min/day)', kde=True, ax=axes[0])
axes[0].set_title('Distribution of App Usage Time')
axes[0].set_xlabel('App Usage Time (min/day)')

# Scatter plot of App Usage Time vs. Battery Drain
sns.scatterplot(data=df, x='App Usage Time (min/day)', y='Battery Drain (mAh/day)', hue='Operating System', ax=axes[1])
axes[1].set_title('App Usage Time vs. Battery Drain')
axes[1].set_xlabel('App Usage Time (min/day)')
axes[1].set_ylabel('Battery Drain (mAh/day)')

# Box plot of Data Usage by User Behavior Class
sns.boxplot(data=df, x='User Behavior Class', y='Data Usage (MB/day)', ax=axes[2])
axes[2].set_title('Data Usage by User Behavior Class')
axes[2].set_xlabel('User Behavior Class')
axes[2].set_ylabel('Data Usage (MB/day)')

plt.tight_layout()
plt.show()

# 3. Insights
print("\nInsights:")
print("1. App Usage Time Distribution:")
print(f"   - Mean: {df['App Usage Time (min/day)'].mean():.2f} minutes per day")
print(f"   - Median: {df['App Usage Time (min/day)'].median():.2f} minutes per day")
print(f"   - The distribution appears to be {'right-skewed' if df['App Usage Time (min/day)'].mean() > df['App Usage Time (min/day)'].median() else 'left-skewed'}")

print("\n2. App Usage Time vs. Battery Drain:")
correlation = df['App Usage Time (min/day)'].corr(df['Battery Drain (mAh/day)'])
print(f"   - Correlation: {correlation:.2f}")
print(f"   - There is a {'strong' if abs(correlation) > 0.7 else 'moderate' if abs(correlation) > 0.5 else 'weak'} {'positive' if correlation > 0 else 'negative'} correlation between App Usage Time and Battery Drain")

print("\n3. Data Usage by User Behavior Class:")
class_means = df.groupby('User Behavior Class')['Data Usage (MB/day)'].mean()
highest_class = class_means.idxmax()
lowest_class = class_means.idxmin()
print(f"   - User Behavior Class {highest_class} has the highest average data usage: {class_means[highest_class]:.2f} MB/day")
print(f"   - User Behavior Class {lowest_class} has the lowest average data usage: {class_means[lowest_class]:.2f} MB/day")

print("\nAdditional Observations:")
print(f"- The dataset contains {df['Operating System'].nunique()} different operating systems")
print(f"- The average number of apps installed is {df['Number of Apps Installed'].mean():.2f}")
print(f"- The average age of users in the dataset is {df['Age'].mean():.2f} years")