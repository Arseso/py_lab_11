import json
from dataclasses import dataclass


@dataclass
class Work:
    name: str
    date_start: str
    date_end: str


@dataclass
class Data:
    name: str
    email: str
    phone: str
    exp: list[Work]
    edu: list[Work]
    about: str


def parse_json(json_file) -> str:
    with open(json_file, "r", encoding='utf-8') as f:
        data = json.load(f)
        exp = [Work(**job) for job in data["exp"]]
        edu = [Work(**job) for job in data["edu"]]
        data = Data(name=data["name"], email=data["email"], phone=data["phone"], exp=exp, edu=edu, about=data["about"])
        return format_resume(data)


def format_resume(data: Data) -> str:
    resume_text = f"""
================================
          Резюме
================================
ФИО: {data.name}
Электронная почта: {data.email}
Телефон: {data.phone}
--------------------------------
Опыт работы:
--------------------------------
"""
    for job in data.exp:
        resume_text += f"Название компании: {job.name}\n\tДаты: {job.date_start} - {job.date_end}\n"

    resume_text += "--------------------------------\nОбразование:\n--------------------------------\n"
    for edu in data.edu:
        resume_text += f"Учебное заведение: {edu.name}\n\tДаты: {edu.date_start} - {edu.date_end}\n"

    resume_text += f"""
--------------------------------
О себе:
--------------------------------
{data.about}
================================
"""
    return resume_text
