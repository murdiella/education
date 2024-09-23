Feature: Restore forgotten password
  @browser
  Scenario: Access restore password page
    Given anonymous user
    When I visit /accounts/manage/
    And I click "Восстановить пароль"
    Then I should be redirected to /accounts/forgot/

  @browser
  Scenario: Restore password for existing user
    Given logged out user
    When I visit /accounts/forgot/
    And I fill email with my email
    And I click "Сбросить пароль"
    Then I should see my email
    And I should see "было отправлено письмо"
    And a letter with reset password token is sent to user

  @browser
  Scenario: Restore password for non-existent user
    Given anonymous user
    When I visit /accounts/forgot/
    And I fill email with my email
    And I click "Сбросить пароль"
    Then I should see my email
    And I should see "было отправлено письмо"
    But a letter with reset password token was not sent to user

  @browser
  Scenario: Try to restore password without email
    Given anonymous user
    When I visit /accounts/forgot/
    And I click "Сбросить пароль"
    Then I should not be redirected

  @browser
  Scenario: Restore password for unconfirmed user
    Given unconfirmed user
    When I visit /accounts/forgot/
    And I fill email with my email
    And I click "Сбросить пароль"
    Then I should see my email
    And I should see "было отправлено письмо"

  @browser
  Scenario: Restore password with invalid token
    Given anonymous user
    When I visit /accounts/reset/invalid_token/
    Then I should see "недействителен"

  @browser
  Scenario: Restore password with token
    Given user that has requested password reset
    When I visit my reset password link
    And I fill password with "some password"
    And I click "Установить новый пароль"
    Then I should be redirected

  @browser
  Scenario: Use password reset token twice
    Given user that has requested password reset
    When I visit my reset password link
    And I fill password with "some password"
    And I click "Установить новый пароль"
    And I visit /accounts/reset/valid_token/
    Then I should see "недействителен"

  # TODO try to use token after expiration