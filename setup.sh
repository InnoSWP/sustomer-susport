#! /bin/bash


# python -m virtualenv .venv
# source .venv/bin/activate

# pip install -r requirements.txt

read -p "[TEST] Enter your telegram id: " tg_chat_id
read -p "Enter your telegram bot token: " tg_token

cd ./telegram_server
echo "TG_TOKEN=$tg_token" > .env
cd ..


cd ./flask_server
echo "TEST_CHAT_ID=$tg_chat_id" > .env
cd ..

echo '\n'
echo "In case of typos you can correct it in .env files"
echo "Bye"
