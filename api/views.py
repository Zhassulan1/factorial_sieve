import gspread
from google.oauth2.service_account import Credentials
from django.http.response import JsonResponse
import google.generativeai as genai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re

# Настройка доступа к Google Sheets
scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets'
]
creds = Credentials.from_service_account_file('./api/secrets.json', scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "11og1HDSYE4EM1tr1eNR0znW3dUqHp8Yp5OzffutkSZc"

# Настройка модели Gemini
genai.configure(api_key="AIzaSyBBuruMdnZYU6r-cf7mQqM2O0qRZCyh_34")
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка уведомления ментора
MENTOR_EMAIL = 'zhkainazarov@gmail.com'
SENDER_EMAIL = 'kdamir2004@gmail.com'
SENDER_PASSWORD = 'aaoxjilpebmbqxel'

def notify_mentor(applicant, summary):
    subject = f"Review Required: {applicant['ФИО']}"
    message = f"Please review the following applicant:\n\n{applicant}\n\nSummary: {summary}"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = MENTOR_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, MENTOR_EMAIL, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_applicant(email, verdict):
    subject = ""
    message = ""

    if verdict == "Pass":
        subject = "Поздравляем! Вы прошли на второй этап"
        message = "Поздравляем! Вы успешно прошли на второй этап нашего инкубатора."
    elif verdict == "Fail":
        subject = "Попробуйте в следующем году"
        message = "К сожалению, вы не прошли на второй этап. Пожалуйста, попытайтесь снова в следующем году."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def create_prompt(applicant):
    prompt = f"""
    Applicant Information:

    - Timestamp: {applicant.get("Отметка времени", "N/A")}
    - Full Name: {applicant.get("ФИО", "N/A")}
    - Email: {applicant.get("email", "N/A")}
    - Date of Birth: {applicant.get("Дата рождения", "N/A")}
    - Phone Number: {applicant.get("номер телефона", "N/A")}
    - Programming Skill Level: {applicant.get("Какое из вариантов лучше всего описывает ваш уровень навыков программирования?", "N/A")}
    - Willingness to Pay: {applicant.get("Готовность участвовать на платной основе", "N/A")}
    - Telegram Profile: {applicant.get("Профиль в Telegram", "N/A")}
    - LinkedIn Profile: {applicant.get("Ссылка LinkedIn", "N/A")}
    - GitHub Profile: {applicant.get("Ссылка GitHub", "N/A")}
    - CV: {applicant.get("CV", "N/A")}
    - Educational Institution: {applicant.get("Место учебы", "N/A")}
    - University Major: {applicant.get("Специальность в университете", "N/A")}
    - Current/Previous Employer: {applicant.get("Место работы (если есть)", "N/A")}
    - Programming Experience Description: {applicant.get("Подробное описание Вашего опыта в программировании", "N/A")}
    - Past Programming Projects: {applicant.get("Прошлые проекты по программированию", "N/A")}
    - Most Impressive Achievements: {applicant.get("Ваши самые впечатляющие достижения (в программировании, учебе, спорте и пр.)", "N/A")}
    - Availability in Almaty (June 5 - August 9, 2024): {applicant.get("Можете ли Вы находиться в Алматы на время инкубатора (5 июня - 9 августа 2024г)?", "N/A")}
    - Need for Accommodation: {applicant.get("Необходимо ли вам место проживания?", "N/A")}
    - Mentor Verdict: {applicant.get("Mentor verdict", "N/A")}

    Evaluation Instructions:

    1. Automatic Fails:
       - If the answer to "Availability in Almaty" is "no" or "false".
       - If the applicant has no programming experience.
       - If the applicant is under 15 years old.

    2. Scoring System:
       - LinkedIn Profile: +5 if present, -10 if absent.
       - Past Projects: +15 if present, -15 if absent.
       - Programming Experience Description: +20 if good, -15 if poor.
       - Impressive Achievements: +20 if present, -5 if absent.
       - GitHub Profile: +20 if present, -5 if absent.
       - Telegram Profile: +20 if present, -5 if absent.

    3. Final Verdict:
       - Calculate the total score based on the scoring system.
       - Consider the mentor's verdict and adjust the score accordingly.
       - Final Score:
         - 70-100: Pass
         - 50-69: 50/50
         - 0-49: Fail

    4. Summary:
       - Provide a concise summary explaining the final verdict. Include the total score and the key factors that influenced the decision.

    Output Format:

    Verdict: [Pass/Fail/50/50]
    Total Score: [Score]
    Summary: [Explanation of the verdict and key factors]
    """

    return prompt

# Функция для оценки кандидатов
def evaluate_applicants(request):
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()

    headers = data[0]
    formatted_data = [{headers[i]: row[i] for i in range(len(headers))} for row in data[1:]]

    results = []
    for index, applicant in enumerate(formatted_data, start=2):
        if applicant.get('verdict') and applicant.get('summary'):
            continue

        prompt = create_prompt(applicant)
        response = model.generate_content(prompt)
        text = response.text

        # Extract the summary and verdict using regex
        verdict = "50/50"
        if "Pass" in text:
            verdict = "Pass"
        elif "Fail" in text:
            verdict = "Fail"

        summary_match = re.search(r"Summary:\s*(.*)", text, re.DOTALL)

        summary = summary_match.group(1).strip() if summary_match else "No summary available."

        if verdict in ['Pass', 'Fail']:
            worksheet.update_cell(index, 20, verdict)
            worksheet.update_cell(index, 21, summary)
        else:
            notify_mentor(applicant, summary)
            worksheet.update_cell(index, 20, verdict)
            worksheet.update_cell(index, 21, summary)

        results.append({'applicant': applicant, 'verdict': verdict, 'summary': summary})

    return JsonResponse({'results': results})

# Новый эндпойнт для уведомления всех кандидатов
def notify_all_applicants(request):
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()

    headers = data[0]
    formatted_data = [{headers[i]: row[i] for i in range(len(headers))} for row in data[1:]]

    for applicant in formatted_data:
        email = applicant.get('email')
        verdict = applicant.get('Mentor verdict')

        if email and verdict:
            notify_applicant(email, verdict)

    return JsonResponse({'status': 'Notifications sent to all applicants'})

