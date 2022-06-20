# Seamless Customer Support

## Description
An open-source web-application easily embeddable into customer's service for seamless usability both for clients (people who ask the questions) and volunteers (people who answer questions)

For that purpose we provide 
- embeddable (via iframe) website
- API for bots
- semantical text parsing (to recognize already asked questions and show answers for them)

## How to run
you need 
- `python` > 3.5
- `pip` corresponding to your python version

### Add telegram token
- move to bot directory\

```cd ./telegram_server```
- copy `.env.tpl`

```cp .env.tpl .env```
- add your token to `.env` file (Use any text editor)

```vim .env```
- go back to project root

```cd ..```

### Install python requirements
- you may wish to use python virtual env
- install dependencies via `pip`

```pip install -r requirements.txt```

### Run server
```python ./master_router.py```

## For developers
- we provide `run.sh` script and `ts.config` to automate process of recompiling 
- if you write on js, be aware, script deletes content of `./flask_server/static/js`
