Feature: Fill exams information

  @browser
  Scenario: Applicant without citizenship tries to access educational information
    Given user that is "applicant without citizenship"
    When I visit /applicants/exams/
    Then I should be redirected to /applicants/citizenship/

  @browser
  Scenario: Applicant with citizenship tries to access personal information page
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    Then I should not be redirected

  @browser
  Scenario: Skip exams section
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Add exam
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    And I click "Добавить экзамен"
    And I select "Математика" as subject[]
    And I select "2020" as year[]
    And I fill mark[] with 90
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Add exam without mark
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    And I click "Добавить экзамен"
    And I select "Математика" as subject[]
    And I select "2020" as year[]
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Add exam without subject
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    And I click "Добавить экзамен"
    And I select "2020" as year[]
    And I fill mark[] with 90
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Add exam without year
    Given user that is "applicant with citizenship"
    When I visit /applicants/exams/
    And I click "Добавить экзамен"
    And I select "Математика" as subject[]
    And I fill mark[] with 90
    And I click "Далее"
    Then I should not be redirected
