import pytest
from pytest_bdd import scenarios, given, when, then
import pandas as pd
import os
from unittest.mock import patch, MagicMock

# Import the functions we want to test
from faqChatbot.CodeRound3 import load_data

# Load the feature file
scenarios('../features/faqchatbot.feature')

# Fixtures for test data
@pytest.fixture
def valid_csv_file(tmp_path):
    csv_path = os.path.join(tmp_path, "test.csv")
    with open(csv_path, "w") as f:
        f.write("question,answer\nWhat is this?,Test answer")
    return csv_path

@pytest.fixture
def valid_json_file(tmp_path):
    json_path = os.path.join(tmp_path, "test.json")
    with open(json_path, "w") as f:
        f.write('[{"question": "What is this?", "answer": "Test answer"}]')
    return json_path

@pytest.fixture
def invalid_file(tmp_path):
    invalid_path = os.path.join(tmp_path, "test.xyz")
    with open(invalid_path, "w") as f:
        f.write("invalid content")
    return invalid_path

# Step definitions
@given("I have a valid CSV file", target_fixture="file_path")
def valid_csv_file_fixture(valid_csv_file):
    return valid_csv_file

@given("I have a valid JSON file", target_fixture="file_path")
def valid_json_file_fixture(valid_json_file):
    return valid_json_file

@given("I have an invalid file format", target_fixture="file_path")
def invalid_file_fixture(invalid_file):
    return invalid_file

@when("I load the data", target_fixture="loaded_data")
@when("I try to load the data", target_fixture="loaded_data")
def load_the_data(file_path):
    """Step to load data and capture any exceptions"""
    try:
        return load_data(file_path)
    except ValueError as e:
        return e

@then("the data should be loaded successfully")
def check_data_loaded(loaded_data):
    assert isinstance(loaded_data, pd.DataFrame), "Loaded data is not a DataFrame"
    assert not loaded_data.empty, "DataFrame is empty"

@then("the dataframe should not be empty")
def check_dataframe_not_empty(loaded_data):
    assert not loaded_data.empty, "DataFrame is empty"

@then("it should raise a ValueError")
def check_value_error(loaded_data):
    assert isinstance(loaded_data, ValueError), "Expected ValueError was not raised"

@then("the error message should indicate unsupported format")
def check_error_message(loaded_data):
    assert "Unsupported file format" in str(loaded_data) or "Error loading data" in str(loaded_data), "Error message does not indicate unsupported format"