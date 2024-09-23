# Глоссарий проекта

| Домен | Термин | Перевод | Тип | Сущности и значения | Синхронизация с 1С |
| :---: | :---: | :---: | :---: | --- | :---: |
| applications | Applicant | Абитуриент | Сущность | user: User, citizenship: Country, applications: Application[], registration_address: Address, postal_address: Address | push&pull |
| applications | Application | Заявление | Сущность | campaign: AdmissionCampaign, applicant: Applicant | push&pull |
| campaigns | AdmissionCampaign | Приемная Кампания | Сущность | level: EducationLevel, basis: BudgetBasis, form: EducationForm | pull |
| geography | Country | Страна | Сущность | Сущность, содержащая всю информацию о стране, необходима для управления гражданством абитуриентов | pull |
| geography | Address | Адрес | Значение | Город, Улица, Дом, Корпус, Квартира, Почтовый индекс | - |
| accounts | User | Пользователь | Сущность | Сущность, которая представляет пользователя web-приложения, нужна для унификации всех процессов, связанных с доставкой приложения по HTTP, содержит значения: **email**, password (read-only) | - |
