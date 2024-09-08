# -*- coding: utf-8 -*-
"""GPT2_Guvi_App.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C9DcP6o9PwKZflMahOJKZltasc-TQrI4
"""

!pip install mysql.connector

!pip install streamlit

!pip install bcrypt

!pip install certifi

!npm install localtunnel

!pip install datetime

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import sqlite3
# import bcrypt
# import datetime
# import re
# import pytz
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch
# 
# st.header("GUVI LLM MODEL")
# 
# # Connect to SQLite database
# 
# con = sqlite3.connect("/content/drive/MyDrive/Colab Notebooks/test.db")
# cur = con.cursor()
# 
# # Create users table if it doesn't exist
# cur.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     registered_date TIMESTAMP,
#     last_login TIMESTAMP
# );
# ''')
# con.commit()
# 
# def username_exists(username):
#     cur.execute("SELECT * FROM users WHERE username = ?", (username,))
#     return cur.fetchone() is not None
# 
# def email_exists(email):
#     cur.execute("SELECT * FROM users WHERE email = ?", (email,))
#     return cur.fetchone() is not None
# 
# def is_valid_email(email):
#     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#     return re.match(pattern, email) is not None
# 
# def create_user(username, password, email, registered_date):
#     if username_exists(username):
#         return 'username_exists'
# 
#     if email_exists(email):
#         return 'email_exists'
# 
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     cur.execute(
#         "INSERT INTO users (username, password, email, registered_date) VALUES (?, ?, ?, ?)",
#         (username, hashed_password, email, registered_date)
#     )
#     con.commit()
#     return 'success'
# 
# def verify_user(username, password):
#     cur.execute("SELECT password FROM users WHERE username = ?", (username,))
#     record = cur.fetchone()
#     if record and bcrypt.checkpw(password.encode('utf-8'), record[0]):
#         cur.execute("UPDATE users SET last_login = ? WHERE username = ?", (datetime.datetime.now(pytz.timezone('Asia/Kolkata')), username))
#         con.commit()
#         return True
#     return False
# 
# def reset_password(username, new_password):
#     hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
#     cur.execute(
#         "UPDATE users SET password = ? WHERE username = ?",
#         (hashed_password, username)
#     )
#     con.commit()
# 
# # Load the fine-tuned model and tokenizer
# model_name_or_path = "/content/drive/MyDrive/fine_tuned_model12345"
# model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
# 
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token
# 
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
# 
# def generate_text(model, tokenizer, seed_text, max_length=100, temperature=1.0, num_return_sequences=1):
#     inputs = tokenizer(seed_text, return_tensors='pt', padding=True, truncation=True)
#     input_ids = inputs['input_ids'].to(device)
#     attention_mask = inputs['attention_mask'].to(device)
# 
#     with torch.no_grad():
#         output = model.generate(
#             input_ids,
#             attention_mask=attention_mask,
#             max_length=max_length,
#             temperature=temperature,
#             num_return_sequences=num_return_sequences,
#             do_sample=True,
#             top_k=50,
#             top_p=0.01,
#             pad_token_id=tokenizer.eos_token_id
#         )
# 
#     generated_texts = [tokenizer.decode(output[i], skip_special_tokens=True) for i in range(num_return_sequences)]
#     return generated_texts
# 
# # Session state management
# if 'sign_up_successful' not in st.session_state:
#     st.session_state.sign_up_successful = False
# if 'login_successful' not in st.session_state:
#     st.session_state.login_successful = False
# if 'reset_password' not in st.session_state:
#     st.session_state.reset_password = False
# if 'username' not in st.session_state:
#     st.session_state.username = ''
# if 'current_page' not in st.session_state:
#     st.session_state.current_page = 'login'
# 
# def home_page():
#     st.title(f"Welcome, {st.session_state.username}!")
#     st.write("This is the home page after successful login.")
#     st.info("Disclaimer: This application is a demonstration of a language model and is not affiliated with GUVI. The content generated by the model may not always be accurate or appropriate. Use it at your own discretion.")
# 
#     st.subheader("Generate Text")
#     seed_text = st.text_input("Enter text:")
#     max_length = st.slider("Max length", min_value=10, max_value=500, value=100)
# 
#     if st.button("Generate"):
#         with st.spinner("Generating..."):
#             generated_texts = generate_text(model, tokenizer, seed_text, max_length, temperature=0.000001, num_return_sequences=1)
#             for i, text in enumerate(generated_texts):
#                 st.write(f"Generated Text {i + 1}:\n{text}\n")
# 
# def login():
#     st.subheader(':blue[**Login**]')
# 
#     # Using st.form to create a form for login
#     with st.form(key='login_form'):
#         username = st.text_input(label='Username', placeholder='Enter Your Username')
#         password = st.text_input(label='Password', placeholder='Enter Your Password', type='password')
#         login_submitted = st.form_submit_button('login')
# 
#     # Handle form submission after the form block
#     if login_submitted:
#         if not username or not password:
#             st.error("Please fill out all fields.")
#         elif verify_user(username, password):
#             st.session_state.login_successful = True
#             st.session_state.username = username
#             st.session_state.current_page = 'home'
#             st.experimental_rerun()  # Trigger a rerun after successful login
#         else:
#             st.error("Incorrect username or password. If you don't have an account, please sign up.")
# 
#     # Navigation buttons outside of the form
#     if not st.session_state.login_successful:
#         c1, c2 = st.columns(2)
#         with c1:
#             st.write(":red[New user?]")
#             if st.button('Go to Sign Up'):
#                 st.session_state.current_page = 'sign_up'
#                 st.experimental_rerun()  # Trigger a rerun to go to sign-up page
#         with c2:
#             st.write(":red[Forgot Password?]")
#             if st.button('Reset Password'):
#                 st.session_state.current_page = 'reset_password'
#                 st.experimental_rerun()  # Trigger a rerun to go to reset password page
# 
# # Decide which page to render based on the current state
# if st.session_state.current_page == 'login':
#     login()
# elif st.session_state.current_page == 'sign_up':
#     signup()  # Make sure signup() is defined
# elif st.session_state.current_page == 'reset_password':
#     reset_password_page()  # Make sure reset_password_page() is defined
# elif st.session_state.current_page == 'home':
#     home_page()  # Make sure home_page() is defined
# 
# def signup():
#     st.subheader(':blue[**Sign Up**]')
# 
#     # Using st.form to create a form for sign up
#     with st.form(key='signup_form'):
#         email = st.text_input(label='Email', placeholder='Enter Your Email')
#         username = st.text_input(label='Username', placeholder='Enter Your Username')
#         password = st.text_input(label='Password', placeholder='Enter Your Password', type='password')
#         re_password = st.text_input(label='Confirm Password', placeholder='Confirm Your Password', type='password')
#         signup_submitted = st.form_submit_button('Sign Up')
# 
#     # Handle form submission after the form block
#     if signup_submitted:
#         registered_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
#         if not email or not username or not password or not re_password:
#             st.error("Please fill out all fields.")
#         elif not is_valid_email(email):
#             st.error("Please enter a valid email address.")
#         elif len(password) <= 3:
#             st.error("Password too short.")
#         elif password != re_password:
#             st.error("Passwords do not match. Please re-enter.")
#         else:
#             result = create_user(username, password, email, registered_date)
#             if result == 'username_exists':
#                 st.error("Username already registered. Please use a different username.")
#             elif result == 'email_exists':
#                 st.error("Email already registered. Please use a different email.")
#             elif result == 'success':
#                 st.success(f"Username {username} created successfully! Please login.")
#                 st.session_state.sign_up_successful = True
#                 st.session_state.current_page = 'login'
#                 st.experimental_rerun()  # Trigger a rerun to go to the login page
#             else:
#                 st.error("Failed to create user. Please try again later.")
# 
#     if st.session_state.sign_up_successful:
#         if st.button('Go to Login'):
#             st.session_state.current_page = 'login'
#             st.experimental_rerun()
# 
# # Ensure signup() is only called after it's defined
# if st.session_state.current_page == 'login':
#     login()
# elif st.session_state.current_page == 'sign_up':
#     signup()
# elif st.session_state.current_page == 'reset_password':
#     reset_password_page()
# elif st.session_state.current_page == 'home':
#     home_page()
# 
# def reset_password_page():
#     st.subheader(':blue[Reset Password]')
# 
#     # Using st.form to create a form for resetting the password
#     with st.form(key='reset_password_form'):
#         username = st.text_input(label='Username', placeholder='Enter Your Username')
#         new_password = st.text_input(label='New Password', placeholder='Enter Your New Password', type='password')
#         confirm_password = st.text_input(label='Confirm New Password', placeholder='Confirm Your New Password', type='password')
#         reset_password_submitted = st.form_submit_button('Reset Password')
# 
#     # Handle form submission after the form block
#     if reset_password_submitted:
#         if not username or not new_password or not confirm_password:
#             st.error("Please fill out all fields.")
#         elif len(new_password) <= 3:
#             st.error("Password too short.")
#         elif new_password != confirm_password:
#             st.error("Passwords do not match. Please re-enter.")
#         else:
#             reset_password(username, new_password)
#             st.success(f"Password for {username} has been reset successfully!")
#             st.session_state.reset_password = True
#             st.session_state.current_page = 'login'
#             st.experimental_rerun()  # Trigger a rerun to go to the login page
# 
#     if st.session_state.reset_password:
#         if st.button('Go to Login'):
#             st.session_state.current_page = 'login'
#             st.experimental_rerun()
# 
# # Ensure the reset_password_page() function is only called after it's defined
# if st.session_state.current_page == 'login':
#     login()
# elif st.session_state.current_page == 'sign_up':
#     signup()
# elif st.session_state.current_page == 'reset_password':
#     reset_password_page()
# elif st.session_state.current_page == 'home':
#     home_page()
# 
#

!streamlit run /content/app.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com