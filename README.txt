изменить токен в config.yml
Запустить бота:
1. Подключаетесь по ssh
2. screen -r -d
3. bash run_bot.bash
--------------------
для импорта данных в json
poetry run python tiktok_bot/db/utils/backup.py

для импорта данных в txt
poetry run python tiktok_bot/db/utils/import.py


--------------------
