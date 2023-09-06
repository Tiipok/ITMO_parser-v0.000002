import requests  
from datetime import datetime
from ics import Calendar, Event
from PyQt5 import QtWidgets, uic
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() 
        uic.loadUi('mainWindow.ui', self)
        self.addFunc() 
        self.show() 
    
    def addFunc(self):
        self.ImportButton.clicked.connect(lambda:self.ImportSchedule())

    def ImportSchedule(self):

        start_date = self.dateEdit_1.text().split('.')
        end_date = self.dateEdit_2.text().split('.')
        
        START_DAY = start_date[0]
        END_DAY = end_date[0]

        START_MONTH = start_date[1]
        END_MONTH = end_date[1]

        START_YEAR = start_date[2]
        END_YEAR = end_date[2]

        TOKEN = self.lineEdit.text()
        
        headers = {"Authorization": TOKEN}
        url = f'https://my.itmo.ru/api/schedule/schedule/personal?date_start={START_YEAR}-{START_MONTH}-{START_DAY}&date_end={END_YEAR}-{END_MONTH}-{END_DAY}'

        schedule = requests.get(url=url, headers=headers).json()['data']

        calendar = Calendar()

        try:
            for i, day in enumerate(schedule):
                self.label_4.setText(f'{i+1}/{len(schedule)}')
                date = day['date']
                for lesson in day['lessons']:
                    
                    event = Event()
                    event.description = lesson['building']
                    event.name = lesson['subject']
                    event.begin = datetime.fromisoformat(f'{date}T{lesson["time_start"]}+03:00')
                    event.end = datetime.fromisoformat(f'{date}T{lesson["time_end"]}+03:00')
                    
                    calendar.events.add(event)

                    with open(f"{self.dateEdit_1.text()}-{self.dateEdit_2.text()}.ics", "w", encoding="utf-8") as f:
                        f.write(calendar.serialize())
                        self.label_4.setText('Done')

        except TypeError:
            self.label_4.setText('error, perhaps your\ntoken is invalid')
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    window = Ui() 
    app.exec_()
