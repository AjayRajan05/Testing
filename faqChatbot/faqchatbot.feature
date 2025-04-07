Feature: FAQ Chatbot Data Loading
  As a user
  I want to load FAQ data from different file formats
  So I can get answers to my questions

  Scenario: Loading valid CSV file
    Given I have a valid CSV file
    When I load the data
    Then the data should be loaded successfully
    And the dataframe should not be empty

  Scenario: Loading valid JSON file
    Given I have a valid JSON file
    When I load the data
    Then the data should be loaded successfully
    And the dataframe should not be empty

  Scenario: Loading invalid file format
    Given I have an invalid file format
    When I try to load the data
    Then it should raise a ValueError
    And the error message should indicate unsupported format
