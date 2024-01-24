# test_currencies
## Описание
Приложение для получения курса валютной пары USDRUB и значенй предыдущих 10 запросов.
Предусмотрена пауза между запросами к внешнему API в 10 секунд. Если пришел запрос до исечения 10 секунд, то показывается результат предыдущего запроса.


GET запрос к [127.0.0.1:8000/get-current-usd/](http://127.0.0.1:8000/get-current-usd/)


## Запуск проекта
1. Клонировать репозиторий:
   ```
   git clone git@github.com:DOSuzer/test_currencies.git
   ```
2. Создать файл .env с содержимым из .env.example.

3. Вставить свой APIKEY ключ к сервису [openexchangerates.org](https://openexchangerates.org/)
   
4. Запустить сборку:
   ```
   docker-compose up -d
   ```
5. Перейти по ссылке [127.0.0.1:8000/get-current-usd/](http://127.0.0.1:8000/get-current-usd/)
