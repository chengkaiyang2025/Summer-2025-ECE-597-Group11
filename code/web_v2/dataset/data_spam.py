import streamlit as st

spam_samples = [
    {
        "subject": "Congratulations! You've won a $1000 gift card!",
        "body": """Dear user,
💴💴💴💴
You have been selected as a winner of our $1000 gift card giveaway.  
Click the link below to claim your prize immediately:

http://fake-prize-link.com

Hurry, this offer expires soon!"""
    },
    {
        "subject": "URGENT: Your account has been compromised!",
        "body": """Dear Customer,

We detected suspicious activity on your account.  
Please verify your information by clicking the secure link below:

http://fake-secure-link.com

Failure to do so will result in account suspension."""
    },
    {
        "subject": "Make $5000 per week working from home!",
        "body": """Hello,

Want to earn thousands of dollars weekly without leaving your house?  
Join our work-from-home program and start making money today!

Sign up now at http://fake-work-link.com

No experience required."""
    }
]
