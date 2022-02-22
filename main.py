import os
import re
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style

my_dpi=96
user = "Pryxy Striqs"

conn = sqlite3.connect('levels.db')
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS levels(user TEXT, skill TEXT, unix REAL, datestamp TEXT, level INT, PRIMARY KEY(skill, level)) ")


def onboard_images_to_db():
    image_dir = f"/home/tom/.runelite/screenshots/{user}/Levels/"
    level_files = os.listdir(image_dir)

    for level_file in level_files:
        if match := re.findall(r'(\w+)\((\d+)\)\s(.+)\.png', level_file):
            (skill, level, date) = match[0]
            date = datetime.strptime(date, '%Y-%m-%d_%H-%M-%S')
            level = int(level)

            c.execute(f"INSERT OR IGNORE INTO levels VALUES('{user}', '{skill}', {date.timestamp()}, '{date.isoformat()}', {level})")

    conn.commit()
    kek = 1


def graph_data():
    plt.title(f"{user} OSRS Levels Over Time")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())


    c.execute("SELECT distinct skill FROM levels")
    skills = c.fetchall()
    skills = [skill[0] for skill in skills]

    for skill in skills:
        kek = f"SELECT datestamp, level FROM levels WHERE skill = '{skill}' order by unix"
        c.execute(f"SELECT datestamp, level FROM levels WHERE skill = '{skill}' order by unix")
        data = c.fetchall()

        dates = []
        values = []

        for row in data:
            dates.append(parser.parse(row[0]))
            values.append(row[1])

        plt.plot_date(dates, values, '-', label=skill)

    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig('levels.png', dpi=my_dpi)

if __name__ == "__main__":
    create_table()
    onboard_images_to_db()
    graph_data()
    c.close()
    conn.close()