from src.read_excels import read_excel_file


def read_rfx_questions(excel_file):
    question_recs = read_excel_file(excel_file, ["Question"])
    questions = [rec["Question"] for rec in question_recs]
    return questions
