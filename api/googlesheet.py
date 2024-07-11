# import gspread 
# from google.oauth2.service_account import Credentials

# scopes = [
#     'https://spreadsheets.google.com/feeds'
# ]
# creds = Credentials.from_service_account_file('secrets.json', scopes=scopes)
# client = gspread.authorize(creds)


# sheet_id = "11og1HDSYE4EM1tr1eNR0znW3dUqHp8Yp5OzffutkSZc"
# sheet = client.open_by_key(sheet_id)
# worksheet = sheet.sheet1
# data = worksheet.get_all_values()

# headers = data[0]
# formatted_data = []
# for row in data[1:]:
#     formatted_row = {headers[i]: row[i] for i in range(len(headers))}
#     formatted_data.append(formatted_row)

# print(formatted_data)