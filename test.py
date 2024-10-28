# from pprint import pp

# import requests
# from bs4 import BeautifulSoup

# URL = "https://www.lit.msu.ru/study/timetable/"
# response = requests.get(URL + "8")
# response.raise_for_status()
# soup = BeautifulSoup(response.text, "lxml")
# weekdays = soup.thead.get_text(" ", strip=True).split(" ")
# rows = soup.tbody.find_all("tr")
# grade_schedule = {}

# for row in rows:
#     if row.get_text(strip=True):
#         cells = []

#         for cell in row.find_all("td"):
#             cell_text = cell.get_text(strip=True)
#             cells.append(cell_text if cell_text else "Нет урока")

#         if cells[5].startswith("8_"):
#             class_name = cells[5]
#             lessons = {}
#             grade_schedule.setdefault(class_name, lessons)
#         else:
#             lesson_schedule = f"{cells[0]}. {cells[1].zfill(5)} - {cells[2].zfill(5)}"

#             for day, schedule, lesson in zip(
#                 weekdays,
#                 (lesson_schedule,) * len(weekdays),
#                 cells[3 : len(weekdays) + 3],
#             ):
#                 lessons.setdefault(day, []).append(f"{schedule}   {lesson}")

# pp(grade_schedule)
