Feature: Select specialities

  @browser
  Scenario: Applicant without citizenship tries to access specialities
    Given user that is "applicant without citizenship"
    When I visit /applicants/specialities/
    Then I should be redirected to /applicants/citizenship/

  @browser
  Scenario: Applicant with citizenship tries to access specialities
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    Then I should not be redirected

  @browser
  Scenario: Pass without selecting any speciality
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Pass selecting 1 speciality
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    And I select 1 speciality
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Pass selecting 2 specialities
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    And I select 2 specialities
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Select 7 specialities
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    And I select 7 specialities
    Then 7 specialities are selected

  @browser
  Scenario: Select 8 specialities
    Given user that is "applicant with citizenship"
    When I visit /applicants/specialities/
    And I select 8 specialities
    Then 7 specialities are selected
