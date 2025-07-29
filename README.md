# YOYO Finance Planner 💰

A Streamlit-based personal finance planner that generates personalized financial plans using AWS Bedrock and Claude AI.

## Features

- Personalized financial planning based on your goals and situation
- Comprehensive analysis with actionable recommendations
- Budget planning with category breakdowns
- Investment guidance for beginners
- Debt management strategies
- Emergency fund planning

## Quick Start

### Prerequisites
- Python 3.8+
- AWS account with Bedrock access
- AWS credentials with `AmazonBedrockFullAccess` policy

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai_finance_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   
   Create a `.env` file:
   ```bash
   AWS_ACCESS_KEY_ID=your_aws_access_key_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
   AWS_REGION=us-east-1
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## AWS Setup

1. Enable Bedrock in AWS console
2. Create IAM user with `AmazonBedrockFullAccess` policy
3. Generate access keys for the user

## Usage

1. Enter your financial goals
2. Describe your current financial situation
3. Click "YOYO" to get personalized advice

## Example

**Financial Goals**: "Save $50,000 for a house down payment in 3 years, pay off $15,000 in student loans"

**Current Situation**: "I make $80,000/year, have $10,000 in savings, monthly expenses of $3,000, and $15,000 in student loans"

## Security

- AWS credentials stored in `.env` file (ignored by git)
- Never commit your `.env` file to version control

## License

MIT License
