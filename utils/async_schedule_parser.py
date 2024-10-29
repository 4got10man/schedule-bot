import asyncio
from pprint import pp

import aiohttp
from bs4 import BeautifulSoup

URL = "https://www.lit.msu.ru/study/timetable/"
START_GRADE = 5
END_GRADE = 11


async def parse_schedule_by_grade(
    grade: str, URL: str = URL
) -> dict[str, dict[str, str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}{grade}") as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            weekdays = soup.thead.get_text(" ", strip=True).split(" ")
            rows = soup.tbody.find_all("tr")
            grade_schedule = {}

            for row in rows:
                if not row.get_text(strip=True):
                    continue
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


async def parse_all_schedules() -> dict[str, dict[str, str]]:
    tasks = [
        parse_schedule_by_grade(str(grade))
        for grade in range(START_GRADE, END_GRADE + 1)
    ]
    results = await asyncio.gather(*tasks)
    all_schedules = {}

    for result in results:
        all_schedules.update(result)

    return all_schedules


# all_data = asyncio.run(parse_all_schedules())
# pp(tuple(all_data.keys()))
