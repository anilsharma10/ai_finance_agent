import streamlit as st
import boto3
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def setup_page_config():
    st.set_page_config(
        page_title="Financial Planner",
        page_icon="💰",
        layout="wide"
    )

def load_custom_styles():
    try:
        with open('styles.css', 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found.")

def get_aws_credentials():
    return {
        'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'region': os.getenv('AWS_REGION', 'us-east-1')
    }

def create_bedrock_client(credentials):
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=credentials['region'],
        aws_access_key_id=credentials['access_key'],
        aws_secret_access_key=credentials['secret_key']
    )

def build_financial_prompt(goals, situation):
    return f"""🎯 Your Task:
Using the information provided, generate a structured, easy-to-follow financial plan that includes the following sections:

CLIENT INFORMATION:
- Financial Goals: {goals}
- Current Situation: {situation}

# FINANCIAL ANALYSIS REPORT

## Current Financial Analysis
Clear assessment of their income, expenses, savings, and liabilities. Identify strengths and areas for improvement.

## Goal Prioritization
Rank their financial goals by importance and feasibility. Provide realistic timelines for achieving each goal.

## Monthly Budget Breakdown
Recommend a practical monthly budget. Include categories like housing, transportation, food, debt payments, savings, and discretionary spending. Use dollar estimates based on their situation.

## Savings Strategy
Recommend how much they should save each month, and suggest suitable saving vehicles (e.g., high-yield savings accounts, CDs).

## Investment Recommendations
Provide beginner-friendly investment options based on their timeline and risk tolerance (e.g., index funds, Roth IRA, ETFs).

## Debt Management Plan
Offer a clear strategy to pay down any existing debt (e.g., snowball vs. avalanche method) with timelines and payment targets.

## Emergency Fund Strategy
Recommend how much they should keep in an emergency fund and a plan to build it over time.

## Actionable Next Steps
Provide a checklist of concrete steps they should take in the next 3, 6, and 12 months to stay on track. Include dollar targets where possible.

🧠 Guidelines:
- Be specific, realistic, and encouraging.
- Tailor all advice to the client's situation.
- Use bullet points, headings, and clear formatting.
- Avoid vague or generic advice.
- Include estimated dollar amounts where helpful.
- Do not include any HTML tags, div tags, or formatting in your response. Provide clean, plain text only."""

def generate_financial_plan(bedrock_client, prompt):
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

def render_header():
    st.title("AI Personal Finance Planner 💰")
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h3 style="color: #1e3a8a; font-weight: 700; margin: 0; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px;">
            💎 Your Financial Success Starts Here
        </h3>
    </div>
    """, unsafe_allow_html=True)

def render_input_form():
    st.markdown("---")
    st.markdown("### 📊 Enter Your Financial Information")
    
    goals = st.text_input(
        "What are your financial goals?", 
        placeholder="e.g., Save for house down payment, Pay off student loans, Build retirement fund"
    )
    
    situation = st.text_area(
        "Describe your current financial situation", 
        placeholder="e.g., I make $80k/year, have $10k in savings, $15k in student loans, monthly expenses of $3k"
    )
    
    return goals, situation

def clean_financial_report(plan):
    # Remove HTML tags
    plan = re.sub(r'<[^>]+>', '', plan)
    plan = re.sub(r'</[^>]+>', '', plan)
    
    # Remove trailing div tags
    plan = re.sub(r'```</div>$', '```', plan)
    plan = re.sub(r'</div>$', '', plan)
    
    # Clean up spacing in code blocks
    lines = plan.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if line.strip().startswith('```') or line.strip().endswith('```'):
            cleaned_lines.append(line)
        elif line.startswith(' ') and any(char.isalnum() for char in line):
            cleaned_lines.append(line.lstrip())
        else:
            cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines).strip()
    result = result.replace('</div>', '')
    result = result.replace('<div>', '')
    
    return result

def display_financial_report(plan):
    clean_plan = clean_financial_report(plan)
    
    st.markdown("---")
    st.markdown("## 💡 Your Personalized Financial Plan")
    st.markdown(f'<div class="financial-report">{clean_plan}</div>', unsafe_allow_html=True)

def main():
    setup_page_config()
    load_custom_styles()
    render_header()
    
    financial_goals, current_situation = render_input_form()
    
    if st.button("🚀 YOYO", type="primary"):
        if not financial_goals or not current_situation:
            st.warning("Please fill in both your financial goals and current situation.")
            return
        
        credentials = get_aws_credentials()
        if not credentials['access_key'] or not credentials['secret_key']:
            st.error("❌ AWS credentials not found. Please check your .env file.")
            return
        
        try:
            bedrock_client = create_bedrock_client(credentials)
            
            with st.status("Processing your financial information...", expanded=True) as status:
                prompt = build_financial_prompt(financial_goals, current_situation)
                plan = generate_financial_plan(bedrock_client, prompt)
                status.update(label="✅ Plan generated successfully!", state="complete")
            
            display_financial_report(plan)
            
        except Exception as e:
            st.error(f"❌ Error generating financial plan: {str(e)}")
    else:
        st.info("💡 Enter your financial information above and click 'YOYO' to get personalized advice!")

if __name__ == "__main__":
    main()