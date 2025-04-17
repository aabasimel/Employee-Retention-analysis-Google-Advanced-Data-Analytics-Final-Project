# Employee-Retention-analysis-Google-Advanced-Data-Analytics-Final-Project

# Salifort Motors Employee Retention Analysis 🚗⚡

# About the Company
Salifort Motors is a **fictional French-based alternative energy vehicle manufacturer**. With a global workforce of **over 100,000 employees**, the company specializes in researching, designing, constructing, validating, and distributing electric, solar, algae, and hydrogen-based vehicles. Salifort’s end-to-end vertical integration model has made it a leader at the intersection of alternative energy and automobiles.

# Project Overview
As a data specialist at Salifort Motors, I was given the results of a **recent employee survey**. The senior leadership team has tasked me with **analyzing the data to identify factors influencing employee retention** and designing a model to **predict whether an employee will leave the company**.

**Key Business Questions:**

✅ What factors contribute to employee turnover?  

✅ Can we build a model to predict employee attrition?

✅ How can the company improve employee retention strategies?


Dataset & Features
The dataset includes various employee attributes, such as:

* Department (e.g., Sales, R&D, HR)

* Number of projects assigned

* Average monthly working hours

* Time spent at the company

* Last evaluation score

* Satisfaction level

* Salary level

* Work accidents

* Promotions in the last 5 years

* Left (Target variable: 1 = left, 0 = stayed)

# Methodology & Approach
To solve this problem, I explored two machine learning approaches:

**Logistic Regression** – A simple and interpretable baseline model.

**Tree-based Machine Learning Model** – A more powerful model to capture complex patterns in employee attrition.

**Performance Metrics:**
To evaluate the model, I used:

✔ Accuracy

✔ Precision & Recall

✔ F1-Score

✔ ROC-AUC Score


**Results & Insights**

🔹 Employees with low satisfaction levels are more likely to leave.

🔹 Overworked employees (high average monthly hours) have a higher attrition rate.

🔹 Employees in certain departments (e.g., Sales & Support) show higher turnover.

🔹 Salary level plays a crucial role—lower-paid employees tend to leave more.

**How to Run the Project**
Prerequisites
Ensure you have the following installed:

Python (3.x)

Jupyter Notebook or any Python IDE

Required libraries: pandas, numpy, seaborn, matplotlib, scikit-learn, xgboost

## Deployed Application

If you'd like to see the deployed version of this application, visit the following link:

[View Deployed Application](https://employeeattritionssalfort.streamlit.app/)

