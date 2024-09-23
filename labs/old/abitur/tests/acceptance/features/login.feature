Feature: Login

  @browser
  Scenario: Access for unregistered user
    Given anonymous user
    When I visit /
    Then I should be redirected to /accounts/login/

  @browser
  Scenario: Login as existing user
    Given logged out user
    When I visit /accounts/login/
    And I fill email with my email
    And I fill password with my password
    And i click "Войти"
    Then I should be redirected

  @browser
  Scenario: Login as non-existent user
    Given anonymous user
    When I visit /accounts/login/
    And I fill email with my email
    And I fill password with my password
    And I click "Войти"
    Then I should see "Неверное имя пользователя или пароль"

  @browser
  Scenario: Access login page as logged in user
    Given logged in user
    When I visit /accounts/login/
    Then I should be redirected

  @browser
  Scenario: Try to login without email
    Given anonymous user
    When I visit /accounts/login/
    And I fill password with my password
    And I click "Войти"
    Then I should not be redirected

  @browser
  Scenario: Try to login without password
    Given anonymous user
    When I visit /accounts/login/
    And I fill email with my email
    And I click "Войти"
    Then I should not be redirected

  @browser
  Scenario: Try to login as unconfirmed user
    Given unconfirmed user
    When I visit /accounts/login/
    And I fill email with my email
    And I fill password with my password
    And I click "Войти"
    Then I should see "Аккаунт не был подтвержден"