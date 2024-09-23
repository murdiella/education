Feature: fill education information

  @browser
  Scenario: Applicant without citizenship tries to access educational information
    Given user that is "applicant without citizenship"
    When I visit /applicants/educations/
    Then I should be redirected to /applicants/citizenship/

  @browser
  Scenario: Applicant with citizenship tries to access personal information page
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    Then I should not be redirected

  @browser
  Scenario: Fully fill education information
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Fill education information without level
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Fill education information without document type
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Fill education information without school name
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill series with "1234"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Fill education information without series
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Fill education information without number
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill issued_date with "01.01.1990"
    And I select "2020" as year
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Fill education information without issued date
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill number with "123456"
    And I select "2020" as year
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Fill eduction information without year
    Given user that is "applicant with citizenship"
    When I visit /applicants/educations/
    And I select "Среднее общее" as level
    And I select "Аттестат" as document_type
    And I fill name with "Название школы"
    And I fill series with "1234"
    And I fill number with "123456"
    And I fill issued_date with "01.01.1990"
    And I click "Далее"
    Then I should not be redirected
