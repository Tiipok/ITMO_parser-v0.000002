import requests  
from datetime import datetime
from ics import Calendar, Event
from pprint import pprint

def main():
    START_DAY = '10' # input('input start day(01, 02, 11, 15...): ')
    LAST_DAY = '20' # input('input last day(01, 02, 11, 15...): ')
    MONTH = '09' # input('input month(01, 02, 11...): ')
    YEAR = '2023'
    TOKEN = "Bearer eyJhbGciOiJ..."
    
    headers = {"Authorization": TOKEN}
    url = f'https://my.itmo.ru/api/schedule/schedule/personal?date_start={YEAR}-{MONTH}-{START_DAY}&date_end={YEAR}-{MONTH}-{LAST_DAY}'
    schedule = requests.get(url=url, headers=headers).json()['data']

    calendar = Calendar()

    for day in schedule:
        date = day['date']
        for lesson in day['lessons']:
            
            try:
                event = Event()
                event.description = lesson['building']
                event.name = lesson['subject']
                event.begin = datetime.fromisoformat(f'{date}T{lesson["time_start"]}+03:00')
                event.end = datetime.fromisoformat(f'{date}T{lesson["time_end"]}+03:00')
            
                calendar.events.add(event)

            except TypeError:
                pprint(lesson)
    
    open('schedule.ics', 'w', encoding="utf-8").close()

    with open("schedule.ics", "w", encoding="utf-8") as f:
        f.write(calendar.serialize())
    
    print('Done')
              

if __name__ == '__main__':
    main()
