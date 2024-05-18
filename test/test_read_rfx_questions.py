from src.read_rfx_questions import read_rfx_questions


def test_read_rfx_questions():
    excel_file = "test_data/rfx_files/rfp_test_en_1.xlsx"
    questions = read_rfx_questions(excel_file)
    assert len(questions) == 6
    # check that all questions are strings
    assert all(isinstance(question, str) for question in questions)
