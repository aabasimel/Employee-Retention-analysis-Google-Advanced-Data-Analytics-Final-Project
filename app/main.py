import streamlit as st
import pickle
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="🧑‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

def read_pickle(path, saved_model_name):
    with open(path + saved_model_name, 'rb') as to_read:
        model = pickle.load(to_read)
    return model

model_path = './models/'
saved_model_name = 'grid_search_rf1.pickle'
loaded_model = read_pickle(model_path, saved_model_name)

with st.sidebar:
    st.title("About")
    st.info("""
    This app predicts employee attrition using a Random Forest model trained on HR data.
    Adjust the parameters on the right and click 'Predict' to see the results.
    """)
    st.markdown("### Model Information")
    st.write(f"**Best CV Score:** {loaded_model.best_score_:.2f}")
    st.write("**Best Parameters:**")
    st.json(loaded_model.best_params_)

st.title('🧑‍💼 Employee Attrition Prediction')
st.markdown("Predict whether an employee is likely to leave the company based on key factors.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Employee Details")
    
    satisfaction_level = st.slider('Satisfaction Level', 0, 100, 50, help="Employee satisfaction level (0-100 scale)")
    satisfaction_color = "red" if satisfaction_level < 30 else "orange" if satisfaction_level < 70 else "green"
    st.markdown(f"""
    <div style="height: 10px; background: lightgray; border-radius: 5px; margin-top: -15px;">
        <div style="width: {satisfaction_level}%; height: 100%; background: {satisfaction_color}; border-radius: 5px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    last_evaluation = st.slider('Last Performance Evaluation', 0.0, 1.0, 0.5, help="Score from the employee's last performance review (0.0-1.0 scale)")
    eval_color = "red" if last_evaluation < 0.4 else "orange" if last_evaluation < 0.7 else "green"
    st.markdown(f"""
    <div style="height: 10px; background: lightgray; border-radius: 5px; margin-top: -15px;">
        <div style="width: {last_evaluation*100}%; height: 100%; background: {eval_color}; border-radius: 5px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    number_project = st.number_input('Number of Projects', min_value=1, max_value=10, value=5, help="How many projects the employee is currently working on")
    if number_project > 7:
        st.warning("High project load may increase attrition risk")
    
    average_montly_hours = st.number_input('Average Monthly Hours', min_value=50, max_value=400, value=200, help="Typical monthly working hours for this employee")
    if average_montly_hours > 250:
        st.warning("High monthly hours may indicate burnout risk")

with col2:
    st.header("Employment History")
    
    tenure = st.number_input('Tenure (Years)', min_value=0, max_value=10, value=5, help="How many years the employee has been with the company")
    work_accident = st.radio('Had a Work Accident?', ['No', 'Yes'], help="Whether the employee has had a workplace accident")
    promotion_last_5years = st.radio('Promoted in Last 5 Years?', ['No', 'Yes'], help="Whether the employee received a promotion in the last 5 years")
    salary = st.selectbox('Salary Level', ['low', 'medium', 'high'], help="The employee's current salary level")
    
    department_options = [
        'IT', 'RandD', 'Accounting', 'HR', 'Management', 
        'Marketing', 'Product Management', 'Sales', 'Support', 'Technical'
    ]
    department = st.selectbox('Department', department_options, help="The employee's current department")

work_accident = 1 if work_accident == 'Yes' else 0
promotion_last_5years = 1 if promotion_last_5years == 'Yes' else 0
salary_mapping = {'low': 1, 'medium': 2, 'high': 3}
salary = salary_mapping[salary]
department_columns = {dept: 1 if dept == department else 0 for dept in department_options}

input_data = np.array([[satisfaction_level / 100, last_evaluation, number_project,
                       average_montly_hours, tenure, work_accident,
                       promotion_last_5years, salary] + list(department_columns.values())])

predict_col, spacer = st.columns([1, 3])
with predict_col:
    predict_btn = st.button('🔮 Predict Attrition Risk', help="Click to predict whether this employee is likely to leave", use_container_width=True)

if predict_btn:
    with st.spinner('Analyzing employee data...'):
        prediction = loaded_model.predict(input_data)
        prediction_prob = loaded_model.predict_proba(input_data)
        
        leave_prob = prediction_prob[0][1]
        stay_prob = prediction_prob[0][0]
        
        st.markdown("---")
        st.header("Prediction Results")
        
        if prediction[0] == 0:
            st.success("✅ Prediction: This employee is likely to **stay** with the company")
        else:
            st.error("⚠️ Prediction: This employee is at risk of **leaving** the company")
        
        st.subheader("Attrition Risk Probability")
        risk_color = "#4CAF50" if leave_prob < 0.3 else "#FFC107" if leave_prob < 0.7 else "#F44336"
        st.markdown(f"""
        <div style="height: 30px; background: #f0f0f0; border-radius: 15px; position: relative; margin-bottom: 20px;">
            <div style="width: {leave_prob*100}%; height: 100%; background: {risk_color}; border-radius: 15px; 
                 display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; color: white; font-weight: bold;">
                {leave_prob*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_prob1, col_prob2 = st.columns(2)
        with col_prob1:
            st.metric("Probability to Stay", f"{stay_prob*100:.1f}%")
        with col_prob2:
            st.metric("Probability to Leave", f"{leave_prob*100:.1f}%")
        
        st.subheader("Key Risk Factors")
        risk_factors = []
        if satisfaction_level < 40:
            risk_factors.append(f"Low satisfaction level ({satisfaction_level}/100)")
        if last_evaluation < 0.4:
            risk_factors.append(f"Low performance evaluation ({last_evaluation:.1f}/1.0)")
        if number_project > 6:
            risk_factors.append(f"High project load ({number_project} projects)")
        if average_montly_hours > 250:
            risk_factors.append(f"High monthly hours ({average_montly_hours} hrs/month)")
        if tenure < 2:
            risk_factors.append(f"Short tenure ({tenure} years)")
        if promotion_last_5years == 0 and tenure > 3:
            risk_factors.append("No recent promotion despite tenure")
        if salary == 1:
            risk_factors.append("Low salary level")
        
        if risk_factors:
            for factor in risk_factors:
                st.warning(f"• {factor}")
        else:
            st.info("No significant risk factors identified")

st.markdown("---")
st.markdown(
    f"""
    <style>
    .footer {{
        font-size: 0.8rem;
        color: gray;
        text-align: center;
        margin-top: 2rem;
    }}
    </style>
    <div class="footer">
        HR Analytics Dashboard • Powered by Random Forest • Model accuracy: {loaded_model.best_score_ * 100:.1f}%
    </div>
    """, 
    unsafe_allow_html=True
)
