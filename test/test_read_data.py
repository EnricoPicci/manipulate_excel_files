from src.read_data import get_excel_file_paths, records_from_excel_files


def test_get_excel_file_paths():
    folder_path = "test_data/excel_files"
    excel_files = get_excel_file_paths(folder_path)
    assert len(excel_files) == 4


def test_read_excel_files():
    folder_path = "test_data/excel_files"
    mandatory_columns = [
        "Question_en",
        "Question_it",
        "Question_fr",
        "Question_de",
        "Question_es",
        "Answer_en",
        "Answer_it",
        "Answer_fr",
        "Answer_de",
        "Answer_es",
        "Domain_1",
        "Domain_2",
        "Domain_3",
    ]

    records = records_from_excel_files(folder_path, mandatory_columns)

    assert len(records) > 10
