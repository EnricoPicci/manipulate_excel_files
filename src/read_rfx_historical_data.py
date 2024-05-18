# records_from_rfx is a function that takes a list of dictionaries containing the following fields
# Question_en	Question_it	Question_fr	Question_de	Question_es	Answer_en	Answer_it	Answer_fr	Answer_de	Answer_es	Domain_1	Domain_2	Domain_3
# the postfix _en, _it, _fr, _de, _es are the languages of the questions and answers
# and returns a list of dictionaries containing the following fields
# Question	Answer	Language    Domain
# where Language is one of en, it, fr, de, es
# and Domain is one of Domain_1, Domain_2, Domain_3
import pandas as pd


def records_from_rfx_historical_data(records, languages):
    """
    Extracts relevant information from the given records based on the specified languages.

    Args:
        records (list): A list of records containing questions and answers in multiple languages.
        languages (list): A list of languages to consider.

    Returns:
        list: A list of dictionaries containing the extracted information, including the question,
              answer, language, and domain for each record.
    """
    new_records = []
    for record in records:
        for language in languages:
            # if there is no question in the language, skip
            if pd.isna(record[f"Question_{language}"]):
                print(f">>>>>>> Skipping record with no question in {language}")
                continue
            # if there is no answer in the language, skip
            if pd.isna(record[f"Answer_{language}"]):
                print(f">>>>>>> Skipping record with no answer in {language}")
                continue
            new_record = {
                "Question": record[f"Question_{language}"],
                "Answer": record[f"Answer_{language}"],
                "Language": language,
                "Domain": record["Domain_1"],
                "Date": record["date"],
                "File_Path": record["file_path"],
            }
            new_records.append(new_record)
    return new_records


#
