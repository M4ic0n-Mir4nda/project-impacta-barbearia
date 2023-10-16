from datetime import datetime, timedelta

date = datetime.strptime("01-01-2023 12:00:00", "%d-%m-%Y %H:%M:%S")
tempo = date + timedelta(hours=00, minutes=30, seconds=00)
print(tempo)
