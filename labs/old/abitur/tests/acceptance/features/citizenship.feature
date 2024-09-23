Feature: Set citizenship

  @browser
  Scenario: User without citizenship tries to access applicants root page
    Given user that is "applicant without citizenship"
    When I visit /applicants/
    Then I should be redirected to /applicants/citizenship/

  @browser
  Scenario: Unauthenticated user tries to access citizenship page
    Given anonymous user
    When I visit /applicants/citizenship/
    Then I should be redirected to /accounts/login/

  @browser
  Scenario Outline: Authorized users try to access citizenship page
    Given user that is "<user>"
    When I visit /applicants/citizenship/
    Then I should not be redirected
    Then I should see "Я являюсь гражданином Российской Федерации"
    Then I should see "Я являюсь гражданином другого государства"

    Examples: users
      | user                           |
      | applicant without citizenship  |
      | applicant with citizenship     |

  @browser
  Scenario Outline: Authorized user selects Russian Federation as their citizenship
    Given user that is "<user>"
    When I visit /applicants/citizenship/
    And I click "Подать заявление"
    Then I should be redirected
    Examples: users
      | user                           |
      | applicant without citizenship  |
      | applicant with citizenship     |

  @browser
  Scenario Outline: Authorized user selects Belarus as their citizenship
    Given user that is "<user>"
    When I visit /applicants/citizenship/
    And I click "Выбрать страну"
    And I select "Республика Беларусь" as country
    And I click "Далее"
    Then I should be redirected
    Examples: users
      | user                           |
      | applicant without citizenship  |
      | applicant with citizenship     |
