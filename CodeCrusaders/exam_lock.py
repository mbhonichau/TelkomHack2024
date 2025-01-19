import tkinter as tk
import ctypes
import threading
import cv2
import sys
import random
from tkinter import messagebox
import webbrowser

# Function to block Alt+Tab and other key combinations (Windows only)
def block_keys():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.SystemParametersInfoW(0x1001, 0, 0x00000002 | 0x00000001, 0)

# Function to unblock keys when the exam ends
def unblock_keys():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.SystemParametersInfoW(0x1001, 0x1001, 0x00000002, 0)

# Function to close the window after the exam
def close_window():
    unblock_keys()
    if cap.isOpened():
        cap.release()
    root.destroy()
    webbrowser.open("user_interface.html")  # Redirect to user_interface.html

# Function to track faces using OpenCV
def face_tracking():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    global cap
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Check if a face is detected
        if len(faces) == 0:
            root.after(0, display_face_not_detected)
        else:
            root.after(0, display_face_detected)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Face Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to change display when face is not detected
def display_face_not_detected():
    # Hide all elements
    scenario_description.pack_forget()
    code_text.pack_forget()
    submit_button.pack_forget()
    results_label.pack_forget()
    recommendations_label.pack_forget()
    next_attempt_button.pack_forget()
    end_button.pack_forget()

# Function to change display when face is detected
def display_face_detected():
    # Show all elements
    scenario_description.pack(pady=20)
    code_text.pack(pady=20)
    submit_button.pack(pady=30)
    results_label.pack(pady=10)
    recommendations_label.pack(pady=10)
    next_attempt_button.pack_forget()  # Ensure this is hidden initially
    end_button.pack(pady=30)

# Define scenarios with grading criteria
scenarios = {
    "Software Developer": {
        "description": "A web application crashes when users submit forms. Write a function to log errors and notify admins.",
        "expected_function": "log_error",
        "correct_code": """
def log_error(message):
    print(f'Error: {message}')  # Simple logging
""",
        "points": 100
    },
    "Data Analyst": {
        "description": "You need to generate a report from a CSV file containing sales data. Write a script to analyze total sales per product.",
        "expected_function": "analyze_sales",
        "correct_code": """
import pandas as pd

def analyze_sales(file_path):
    df = pd.read_csv(file_path)
    return df.groupby('product')['sales'].sum()
""",
        "points": 100
    },
}

# Initialize attempt counter
attempts = 0
max_attempts = 2

# Function to assess the submitted code and provide feedback
def assess_code(user_code, career):
    expected_function = scenarios[career]["expected_function"]
    correct_code = scenarios[career]["correct_code"]
    max_points = scenarios[career]["points"]

    score = 0
    if expected_function in user_code:
        if user_code.strip() == correct_code.strip():
            score = max_points
            return score, "Excellent work! You understood the concept."
        else:
            score = max_points // 2
            return score, "The logic is partially correct. Please review the requirements."
    else:
        return score, "Your function is missing. Make sure to define it."

# Function to recommend study modules based on the score
def recommend_modules(score, max_points):
    percentage = (score / max_points) * 100
    if percentage < 50:
        return ["Introduction to Python", "Error Handling in Python", "Pandas for Data Analysis"]
    elif percentage < 75:
        return ["Intermediate Python", "Data Analysis with Pandas"]
    else:
        return ["Advanced Programming Concepts", "Software Design Patterns"]

# Function to save results to a file
def save_results(score, recommendations):
    with open("exam_results.txt", "a") as file:
        file.write(f"Score: {score}, Recommendations: {', '.join(recommendations)}\n")

# Function to submit code
def submit_code():
    global attempts
    user_code = code_text.get("1.0", tk.END)
    score, feedback = assess_code(user_code, career)

    # Calculate percentage
    percentage = (score / scenarios[career]["points"]) * 100
    feedback_message = f"{feedback}\nYour score: {score}/{scenarios[career]['points']} ({percentage:.2f}%)"

    # Update the results label with the feedback
    results_label.config(text=feedback_message)

    # Get recommended modules based on the assessment
    recommendations = recommend_modules(score, scenarios[career]["points"])
    recommendation_text = "Recommended Modules:\n" + "\n".join(recommendations)
    
    # Update the recommendations label
    recommendations_label.config(text=recommendation_text)

    # Save results
    save_results(score, recommendations)

    # Increase the attempt count
    attempts += 1
    if attempts >= max_attempts:
        messagebox.showinfo("Info", "You have reached the maximum number of attempts. Returning to the main page.")
        close_window()
    else:
        next_attempt_button.pack(pady=10)
        submit_button.config(state='disabled')

# Function for the next attempt
def next_attempt():
    global attempts, career
    code_text.delete("1.0", tk.END)
    results_label.config(text="")
    recommendations_label.config(text="")
    submit_button.config(state='normal')
    next_attempt_button.pack_forget()

    career = random.choice(list(scenarios.keys()))
    scenario_description.config(text=scenarios[career]["description"])

# Set up the main Tkinter window
root = tk.Tk()
root.title("Exam Mode")
root.attributes("-fullscreen", True)

# Retrieve career from command line arguments
if len(sys.argv) != 3:
    print("Usage: python exam_lock.py <career> <level>")
    sys.exit(1)

career = sys.argv[1]
level = sys.argv[2]

# Display the scenario description based on career
scenario_description = tk.Label(root, text=scenarios[career]["description"], font=("Helvetica", 16), bg="white", fg="black")
scenario_description.pack(pady=20)

# Text area for user to input their code
code_text = tk.Text(root, height=15, width=100)
code_text.pack(pady=20)

# Submit button
submit_button = tk.Button(root, text="Submit Code", command=submit_code, font=("Helvetica", 16), bg="blue", fg="white")
submit_button.pack(pady=30)

# Label for displaying assessment results
results_label = tk.Label(root, text="", font=("Helvetica", 14), fg="black", wraplength=600)
results_label.pack(pady=10)

# Label for displaying recommended modules
recommendations_label = tk.Label(root, text="", font=("Helvetica", 14), fg="black", wraplength=600)
recommendations_label.pack(pady=10)

# Next attempt button (initially hidden)
next_attempt_button = tk.Button(root, text="Next Attempt", command=next_attempt, font=("Helvetica", 16), bg="orange", fg="black")
next_attempt_button.pack_forget()

# End button to close the program
end_button = tk.Button(root, text="End", command=close_window, font=("Helvetica", 16), bg="red", fg="white")
end_button.pack(pady=30)

# Start face tracking in a separate thread immediately
threading.Thread(target=face_tracking, daemon=True).start()

# Run the window
root.mainloop() 