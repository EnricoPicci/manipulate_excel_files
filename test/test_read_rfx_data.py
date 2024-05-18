from src.read_excels import records_from_excel_files
from src.read_rfx_data import records_from_rfx


def test_records_from_rfx():
    folder_path = "test_data/excel_files"
    languages = ["en", "it", "fr", "de", "es"]

    records = records_from_excel_files(folder_path)
    new_records = records_from_rfx(records, languages)

    assert len(new_records) > 10
    assert all(
        [
            "Question" in record
            and "Answer" in record
            and "Language" in record
            and "Domain" in record
            and "Date" in record
            and "File Path" in record
            for record in new_records
        ]
    )


def test_records_from_rfx():
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
    languages = ["en", "it", "fr", "de", "es"]

    records = records_from_excel_files(folder_path, mandatory_columns)
    new_records = records_from_rfx(records, languages)

    assert len(new_records) > 10
    assert all(
        [
            "Question" in record
            and "Answer" in record
            and "Language" in record
            and "Domain" in record
            and "Date" in record
            and "File_Path" in record
            for record in new_records
        ]
    )
