Feature: Fill personal information

  @browser
  Scenario: Applicant without citizenship tries to access personal information page
    Given user that is "applicant without citizenship"
    When I visit /applicants/personal/
    Then I should be redirected to /applicants/citizenship/

  @browser
  Scenario: Applicant with citizenship tries to access personal information page
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    Then I should not be redirected

  @browser
  Scenario: Fully fill personal information
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my personal information
    And I fill my passport information
    And I fill my address information
    And I fill my contacts information
    And I check personal data processing agreement
    And I click "Далее"
    Then I should be redirected

  @browser
  Scenario: Fully fill personal information without personal data agreement
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my personal information
    And I fill my passport information
    And I fill my address information
    And I fill my contacts information
    And I click "Далее"
    Then I should not be redirected


  @browser
  Scenario: Fully fill personal information without personal info
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my passport information
    And I fill my address information
    And I fill my contacts information
    And I check personal data processing agreement
    And I click "Далее"
    Then I should not be redirected


  @browser
  Scenario: Fully fill personal information without passport info
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my personal information
    And I fill my address information
    And I fill my contacts information
    And I check personal data processing agreement
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Fully fill personal information without contacts info
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my personal information
    And I fill my passport information
    And I fill my address information
    And I check personal data processing agreement
    And I click "Далее"
    Then I should not be redirected

  @browser
  Scenario: Fully fill personal information without address
    Given user that is "applicant with citizenship"
    When I visit /applicants/personal/
    And I fill my personal information
    And I fill my passport information
    And I fill my contacts information
    And I check personal data processing agreement
    And I click "Далее"
    Then I should be redirected
