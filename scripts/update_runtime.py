from datetime import date
from pathlib import Path
import re


BIRTH_DATE = date(2006, 3, 12)

SVG_FILES = [
    Path("dark_mode.svg"),
    Path("light_mode.svg"),
]


def calculate_age(birth_date, today):
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1

        if today.month == 1:
            previous_year = today.year - 1
            previous_month = 12
        else:
            previous_year = today.year
            previous_month = today.month - 1

        if previous_month == 12:
            next_year = previous_year + 1
            next_month = 1
        else:
            next_year = previous_year
            next_month = previous_month + 1

        days_in_previous_month = (
            date(next_year, next_month, 1)
            - date(previous_year, previous_month, 1)
        ).days

        days += days_in_previous_month

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def update_svg(svg_file, runtime):
    content = svg_file.read_text(encoding="utf-8")

    pattern = (
        r'(<tspan class="key">Runtime</tspan>:'
        r'<tspan class="cc">[^<]*</tspan>'
        r'<tspan class="value">)'
        r'[^<]+'
        r'(</tspan>)'
    )

    updated_content, count = re.subn(
        pattern,
        rf"\g<1>{runtime}\g<2>",
        content,
        count=1
    )

    if count != 1:
        raise RuntimeError(
            f"Could not find Runtime value in {svg_file}"
        )

    svg_file.write_text(updated_content, encoding="utf-8")

    print(f"{svg_file}: {runtime}")


def main():
    today = date.today()

    years, months, days = calculate_age(
        BIRTH_DATE,
        today
    )

    runtime = f"{years} years, {months} months, {days} days"

    for svg_file in SVG_FILES:
        update_svg(svg_file, runtime)


if __name__ == "__main__":
    main()
