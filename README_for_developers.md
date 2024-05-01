# Проект: testat_bot

## Описание
Этот проект представляет собой Telegram-бота, который будет собирать аналитику о подписчиках канала и передавать ее в Google Таблицы. Бот должен обеспечивать проверку авторизации пользователя и позволять администраторам управлять сбором данных.

В данном README содержатся инструкции для разработчиков, включая требования к именованию веток, правила принятия пул-реквестов и порядок работы с основной веткой `develop`.

## Требования к именованию веток
Для поддержания структурированного процесса разработки, пожалуйста, используйте следующие требования к именованию веток:
- **Основная ветка**: Основная рабочая ветка проекта называется `develop`. Все новые разработки должны начинаться из этой ветки.
- **Ветки для фич**: Для разработки новой функциональности создавайте ветку в формате `feature/название_фичи`. Например, для добавления функциональности сбора данных для аналитики, можно использовать `feature/get_data_for_analytics`.
- **Ветки для исправлений багов**: Если вы работаете над исправлением ошибки, используйте формат `bugfix/название_исправления`.

## Порядок принятия пул-реквестов
Для обеспечения качественного кода и согласованного процесса разработки, следуйте этим правилам при создании пул-реквестов:

1. **Создание ветки**:
   - Начинайте с основной ветки `develop`.
   - Создайте новую ветку для вашей разработки согласно требованиям к именованию веток.
   
2. **Добавление кода**:
   - Вносите необходимые изменения в свою ветку.
   - Убедитесь, что ваш код работает корректно, пройдите все тесты.
   
3. **Создание пул-реквеста**:
   - После завершения работы, создайте пул-реквест в ветку `develop`.
   - Опишите в пул-реквесте внесенные изменения и цель вашего кода.
   
4. **Код-ревью**:
   - Пул-реквест считается успешным, когда два других разработчика проведут ревью кода.
   - После успешного ревью, тимлид может влить ваш пул-реквест в ветку `develop`.
   - Если ревьюеры выявили проблемы или предложили улучшения, внесите необходимые корректировки и снова запросите ревью.
   
## Дополнительная информация
- **Соглашения по стилю кода**: Следуйте принятому соглашению по стилю кода в проекте.

Если у вас есть вопросы или предложения по процессу разработки, пожалуйста, обратитесь к тимлиду или назначенному координатору проекта.