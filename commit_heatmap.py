import subprocess
import matplotlib.pyplot as plt
import datetime
from collections import Counter

# Get commit dates from git
output = subprocess.check_output(
    ['git', 'log', '--since=1 year ago', '--pretty=format:%ad', '--date=short']
).decode('utf-8').splitlines()

dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in output]
counter = Counter(dates)

# Prepare data for 52 weeks x 7 days
start_date = datetime.date.today() - datetime.timedelta(days=365)
heatmap = [[0]*7 for _ in range(52)]

for date, count in counter.items():
    delta = (date - start_date).days
    week = delta // 7
    day = date.weekday()
    if 0 <= week < 52:
        heatmap[week][day] = count

plt.imshow(heatmap, cmap='Greens', interpolation='nearest', aspect='auto')
plt.title("Commit Heatmap (Last Year)")
plt.show()
