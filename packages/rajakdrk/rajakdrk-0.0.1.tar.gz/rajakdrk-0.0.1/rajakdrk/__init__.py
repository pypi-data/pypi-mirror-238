from datetime import date, datetime


def name():
    return "DUDEKULA RAJAK"

def age(born=datetime(2000, 2, 13)):
    today = date.today()
    return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day))) + " years old."

def aboutYourself():
    return "I am a fourth-year student pursuing Computer Science Engineering at JNTUA University, SVR Engineering College. Additionally, I am currently in my third year of study in Data Science and Programming at the esteemed Indian Institute of Technology Madras (IITM). Over the past five years, I have acquired proficiency in various technologies and have had the privilege of imparting this knowledge to both my peers and students. I have had the opportunity to instruct a cohort of over 200 individuals, with a primary focus on teaching the Python programming language."

def portfolio():
    return "https://rajakdrk.github.io/mrdrk/"

