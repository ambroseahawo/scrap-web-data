import datetime

current_time = str(datetime.datetime.now())

split_time = current_time.split('.')
split_date_time = split_time[0].split()
file_name = '@'.join(split_date_time)


print(file_name)