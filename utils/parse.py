from pprint import pp

import requests
from bs4 import BeautifulSoup

URL = "https://www.lit.msu.ru/study/timetable/"


def parse_schedule_by_grade(grade: str, URL: str = URL) -> dict:
    response = requests.get(URL + grade)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    weekdays = soup.thead.get_text(" ", strip=True).split(" ")
    rows = soup.tbody.find_all("tr")
    grade_schedule = {}

    for row in rows:
        if row.get_text(strip=True):
            cells = []

            for cell in row.find_all("td"):
                cell_text = cell.get_text(strip=True)
                cells.append(cell_text if cell_text else "Нет урока")

            if cells[5].startswith(f"{grade}_"):
                class_name = cells[5]
                lessons = {}
                grade_schedule.setdefault(class_name, lessons)
            else:
                lesson_schedule = (
                    f"{cells[0]}. {cells[1].zfill(5)} - {cells[2].zfill(5)}"
                )

                for day, schedule, lesson in zip(
                    weekdays,
                    (lesson_schedule,) * len(weekdays),
                    cells[3 : len(weekdays) + 3],
                ):
                    lessons.setdefault(day, []).append(f"{schedule}   {lesson}")

    for grade in grade_schedule:
        for day in grade_schedule[grade]:
            grade_schedule[grade][day] = "\n".join(grade_schedule[grade][day])

    return grade_schedule


def parse_all_schedules(URL: str) -> list:
    all_schedules = []

    for grade in range(5, 12):
        all_schedules.append(parse_schedule_by_grade(URL, str(grade)))

    return all_schedules


# pp(parse_all_schedules(URL))
# pp(parse_schedule_by_grade("11"))
