import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset (assuming it's already downloaded)
df = pd.read_csv("user_behavior_dataset.csv")

# 1. Hypothesis Testing
print("1. Hypothesis Testing")
print("Hypothesis: Users with Android devices have higher average app usage time than iOS users.")

# Separate Android and iOS users
android_usage = df[df['Operating System'] == 'Android']['App Usage Time (min/day)']
ios_usage = df[df['Operating System'] == 'iOS']['App Usage Time (min/day)']

# Perform independent t-test
t_statistic, p_value = stats.ttest_ind(android_usage, ios_usage)

print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value}")

alpha = 0.05
if p_value < alpha:
    print("We reject the null hypothesis.")
    print("There is a significant difference in app usage time between Android and iOS users.")
else:
    print("We fail to reject the null hypothesis.")
    print("There is no significant difference in app usage time between Android and iOS users.")

# 2. Correlation Analysis
print("\n2. Correlation Analysis")

# Select numeric columns for correlation analysis
numeric_columns = ['App Usage Time (min/day)', 'Screen On Time (hours/day)', 'Battery Drain (mAh/day)',
                   'Number of Apps Installed', 'Data Usage (MB/day)', 'Age', 'User Behavior Class']
correlation_matrix = df[numeric_columns].corr()

# Plot correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Heatmap of User Behavior Variables')
plt.tight_layout()
plt.show()

# Interpret strongest correlations
print("Strongest correlations:")
for i in range(len(numeric_columns)):
    for j in range(i+1, len(numeric_columns)):
        corr = correlation_matrix.iloc[i, j]
        if abs(corr) > 0.5:
            print(f"{numeric_columns[i]} and {numeric_columns[j]}: {corr:.2f}")

# 3. Regression Analysis
print("\n3. Regression Analysis")
print("Predicting 'Battery Drain (mAh/day)' based on 'App Usage Time (min/day)'")

X = df[['App Usage Time (min/day)']]
y = df['Battery Drain (mAh/day)']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

# Plot the regression line
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', alpha=0.5)
plt.plot(X_test, y_pred, color='red', linewidth=2)
plt.xlabel('App Usage Time (min/day)')
plt.ylabel('Battery Drain (mAh/day)')
plt.title('Linear Regression: App Usage Time vs Battery Drain')
plt.tight_layout()
plt.show()

print(f"\nRegression equation: Battery Drain = {model.intercept_:.2f} + {model.coef_[0]:.2f} * App Usage Time")
print(f"For every additional minute of app usage, battery drain increases by approximately {model.coef_[0]:.2f} mAh")
