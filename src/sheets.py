import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC


class GoogleSheets():
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = SAC.from_json_keyfile_name('cmput.json', scope)
        client = gspread.authorize(creds)

        self.sheet = client.open('Apartments').sheet1

        # self.apartments = self.sheet.get_all_records()

    def add_apartment(self, text, index):
        # index is the row that we want to insert the apartment at
        # text is an array of strings, e.g: ["Hello", "World", "!"]
        self.sheet.insert_row(text, index)


if __name__ == "__main__":
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = SAC.from_json_keyfile_name('cmput.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('Apartments').sheet1
        apartments = sheet.get_all_records()

    except Exception as e:
        print("Error {} caught using Google Sheets!".format(e))
