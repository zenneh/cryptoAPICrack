# Crypto API Crack
This is a python script to download market data for free

## Usage
To generate the api keys, use the tool keygen.py
```python
python3 keygen.py
```
these keys kan be used by datacrack.py to download the data

Downloading the data can be done by running:
```python
python3 datacrack.py
```
> Note, The market can be set in source code -> working on config file

## How it works
Well...in this repo you can find 2 scripts. One for extracting keys, the other for dowloading the data.

**keygen.py**
To generate keys the scripts uses 2 api's.
- 1secmail -> for generating temp mails
- coinapi.io -> to request a free key

First we create an inbox with the 1secmail api. When we have this inbox we need to request a key on coinapi.io. This can be done by bypassing the google recaptcha token. And use this token in the header. Once we received the key, it will be added to a text file

## Working on
- Config file: User defined config of markets to download
- Multitreaded downloading: download data faster with multiple threads

**Config file**
Todo:
- [ ] Define config file format
- [ ] Parse the file
- [ ] Apply to program


**Better estimate**
Todo:
- [ ] Find difference between start time and current time
- [ ] Based on request size and timespan calculate te number of iterations + buffer
