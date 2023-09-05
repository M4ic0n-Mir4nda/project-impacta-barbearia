from datetime import datetime, timedelta

dt = datetime.strptime("2023-08-22 14:30:00", "%Y-%m-%d %H:%M:%S")

print(dt + timedelta(hours=2))


