import gspread 
from google.oauth2.service_account import Credentials
from django.http.response import JsonResponse
import google.generativeai as genai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройка доступа к Google Sheets
scopes = [
    'https://spreadsheets.google.com/feeds'
]
creds = Credentials.from_service_account_file('./api/secrets.json', scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "11og1HDSYE4EM1tr1eNR0znW3dUqHp8Yp5OzffutkSZc"

# Настройка модели Gemini
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка уведомления ментора
MENTOR_EMAIL = 'zhkainazarov@gmail.com'
SENDER_EMAIL = 'kdamir2004@gmail.com'
SENDER_PASSWORD = ''

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

# Основная функция для оценки студентов
def evaluate_applicants(request):
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()

    headers = data[0]
    formatted_data = [{headers[i]: row[i] for i in range(len(headers))} for row in data[1:]]

    results = []
    for index, applicant in enumerate(formatted_data, start=2):  # Начинаем с 2, так как первая строка это заголовки
        prompt = f"Evaluate the following applicant:\n\n{applicant}\n\nProvide a verdict (Pass, Fail, 50/50) and a summary of the reasons."
        response = model.generate_content(prompt)
        text = response.text

        # Пример простой логики для извлечения вердикта и саммари из текста ответа модели
        verdict = "50/50"
        summary = "No summary available."
        if "Pass" in text:
            verdict = "Pass"
        elif "Fail" in text:
            verdict = "Fail"

        # Пример поиска строки с саммари
        for line in text.split('\n'):
            if "Summary:" in line:
                summary = line.split("Summary:")[1].strip()
                break

        if verdict in ['Pass', 'Fail']:
            worksheet.update_cell(index, 20, verdict)  # Колонка с вердиктом
            worksheet.update_cell(index, 21, summary)  # Колонка с саммари
        else:
            notify_mentor(applicant, summary)

        results.append({'applicant': applicant, 'verdict': verdict, 'summary': summary})

    return JsonResponse({'results': results})
