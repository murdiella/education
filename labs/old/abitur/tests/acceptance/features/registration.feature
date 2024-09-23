Feature: Registration

  @browser
  Scenario: Access registration from the login page
    Given anonymous user
    When I visit /accounts/login/
    And I click "Получить доступ"
    Then I should be redirected to /accounts/manage/

  @browser
  Scenario: Access signup page from the registration page
    Given anonymous user
    When I visit /accounts/manage/
    And I click "Подать заявление"
    Then I should be redirected to /accounts/manage/signup/

  @browser
  Scenario: Possible to signup with email
    Given anonymous user
    When I visit /accounts/manage/signup/
    And I fill email with my email
    And I fill password with my password
    And I click "Зарегистрироваться"
    Then I should see "подтвердите свой email"
    And I should see my email

  @browser
  Scenario: Impossible to signup without email
    Given anonymous user
    When I visit /accounts/manage/signup/
    And I fill password with my email
    And I click "Зарегистрироваться"
    Then I should not be redirected

  @browser
  Scenario: Impossible to signup without a password
    Given anonymous user
    When I visit /accounts/manage/signup/
    And I fill email with my email
    And I click "Зарегистрироваться"
    Then I should not be redirected

  @browser
  Scenario: Impossible to signup twice
    Given logged out user
    When I visit /accounts/manage/signup/
    And I fill email with my email
    And I fill password with my password
    And I click "Зарегистрироваться"
    Then I should see "Пользователь с таким email уже существует"

  @browser
  Scenario: Authenticated user cannot access signup page
    Given logged in user
    When I visit /accounts/manage/signup/
    Then I should be redirected

  # TODO test for expired token
