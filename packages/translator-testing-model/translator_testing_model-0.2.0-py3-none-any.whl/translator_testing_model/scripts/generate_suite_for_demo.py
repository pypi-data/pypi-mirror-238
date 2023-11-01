from src.translator_testing_model.datamodel.pydanticmodel import TestAsset, TestCase, TestSuite
import csv
import json


def parse_tsv(filename):
    """
    Parse a TSV file and return a list of dictionaries.

    :param filename: The path to the TSV file.
    :return: A list of dictionaries, where each dictionary represents a row in the TSV.
    """
    with open(filename, newline='', encoding='utf-8') as tsvfile:
        # Use csv.DictReader, specifying the delimiter as a tab
        reader = csv.DictReader(tsvfile, delimiter='\t')

        # Convert the reader into a list of dictionaries
        return list(reader)


# Functions to create TestAssets, TestCases, and TestSuite
def create_test_assets_from_tsv(test_assets):
    assets = []
    for row in test_assets:
        if row.get("Query") == "":
            continue
        ta = TestAsset(id=row.get("id"),
                       name=row.get("id"),
                       description=row.get("id"))
        ta.input_id = row.get("InputID, node normalized")
        ta.input_name = row.get("InputName (user choice)")
        ta.predicate = row.get("Query")
        ta.output_id = row.get("OutputID")
        ta.output_name = row.get("OutputName")
        ta.runner_settings = [row.get("Settings").lower()]
        if row.get("Expected Result / Suggested Comparitor") == "4_NeverShow":
            ta.expected_output = "number_4_NeverShow"
        elif row.get("Expected Result / Suggested Comparitor") == "3_BadButForgivable":
            ta.expected_output = "number_3_BadButForgivable"
        elif row.get("Expected Result / Suggested Comparitor") == "2_Acceptable":
            ta.expected_output = "number_2_Acceptable"
        elif row.get("Expected Result / Suggested Comparitor") == "1_TopAnswer":
            ta.expected_output = "number_1_TopAnswer"
        else:
            print(row.get("Expected Result / Suggested Comparitor"))

        if row.get("Well Known") == "yes":
            ta.well_known = True
        else:
            ta.well_known = False
        assets.append(ta)

    return assets


def create_test_cases_from_test_assets(test_assets, test_case_model):
    test_cases = []
    for idx, test_asset in enumerate(test_assets):
        test_case_id = f"TestCase_{idx}"
        test_case = test_case_model(id=test_case_id, test_assets=[test_asset])
        test_cases.append(test_case)
    return test_cases


def create_test_suite_from_test_cases(test_cases, test_suite_model):
    test_suite_id = "TestSuite_1"
    test_cases_dict = {test_case.id: test_case for test_case in test_cases}
    return test_suite_model(id=test_suite_id, test_cases=test_cases_dict)


# Reading the TSV file
tsv_file_path = 'pf_test_assets_2023_10_30.tsv'

tsv_data = parse_tsv(tsv_file_path)

# Create TestAsset objects
test_assets = create_test_assets_from_tsv(tsv_data)

# Create TestCase objects
test_cases = create_test_cases_from_test_assets(test_assets, TestCase)
#
# Assemble into a TestSuite
test_suite = create_test_suite_from_test_cases(test_cases, TestSuite)
#
# Convert to JSON and save to file
test_suite_json = test_suite.json(indent=4)


suite_json_output_path = 'test_suite_output.json'

with open(suite_json_output_path, 'w') as file:
    file.write(test_suite_json)

for i, item in enumerate(test_cases):
    file_prefix = item.id
    filename = f"{file_prefix}.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(item.dict(), file, ensure_ascii=False, indent=4)

for i, item in enumerate(test_assets):
    file_prefix = item.id
    filename = f"{file_prefix}.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(item.dict(), file, ensure_ascii=False, indent=4)
