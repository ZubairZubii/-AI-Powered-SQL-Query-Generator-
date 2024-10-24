import re
import streamlit as st
import google.generativeai as genai

Gemeni_Ai_key = "AIzaSyC6C89uUPZ8z4PQJMFLuXubUNqtGOLcRsQ"
genai.configure(api_key=Gemeni_Ai_key)
model = genai.GenerativeModel("gemini-pro")

def extract_sql_query(text):
    match = re.search(r"```sql\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot:", layout="centered")
    
    # Custom CSS for modern styling
    st.markdown("""
        <style>
            /* General page styling */
            body {
                background-color: #f0f2f6;
                color: #343a40;
                font-family: 'Segoe UI', sans-serif;
            }
            .css-1lcbmhc, .css-1d391kg {
                background-color: #ffffff;
                border: 1px solid #e3e3e3;
                padding: 20px;
                border-radius: 10px;
            }
            /* Heading styling */
            .main-heading {
                color: #4e73df;
                font-weight: 600;
                text-align: center;
                margin-bottom: 10px;
            }
            .sub-heading {
                color: #2e59d9;
                text-align: center;
                font-size: 1.1rem;
                margin-bottom: 20px;
            }
            /* Input field styling */
            textarea {
                border: 2px solid #ced4da;
                border-radius: 6px;
            }
            /* Button styling */
            .stButton>button {
                background-color: #4e73df;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .stButton>button:hover {
                background-color: #2e59d9;
            }
            /* Code block styling */
            .css-15fqyul {
                background-color: #f9f9f9;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 15px;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Main heading
    st.markdown("<h1 class='main-heading'>SQL Query Generator 🤖</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='sub-heading'>Generate SQL queries with AI assistance</h3>", unsafe_allow_html=True)
    
    text_input = st.text_area("Enter your Query in Plain English", height=150, placeholder="e.g., Show all employees with salary above 5000")
    
    submit = st.button("Generate SQL Query")
    
    if submit:
        with st.spinner("Generating SQL Query..."):
            template = f"""
            Create a SQL query snippet with the below text:
            
            ```
            {text_input}
            ```
            
            I just want sql query
            """
            response = model.generate_content(template)
            raw_output = response.text
            sql_query = extract_sql_query(raw_output)

            expected_output = f"""
            What would be the expected response of the sql query snippet:
            
            ```
            {sql_query}
            ```
            
            Provide a sample tabular Response with no explanation
            """
            eout = model.generate_content(expected_output).text

            explanation = f"""
            Explain this sql query:
            
            Please provide the simplest explanation
            
            ```
            {sql_query}
            ```
            """
            explainout = model.generate_content(explanation).text



            # Display results with enhanced styling
            st.success("SQL Query generated successfully!")
            st.code(sql_query, language="sql")

            st.success("Expected Output of the SQL query:")
            st.markdown(eout)

            st.success("Explanation of the SQL Query:")
            st.markdown(explainout)

# Run the app
main()
