# Fireside
Fireside p2p chat

## Installation

```bash

# Install fireside
pip3 install . --no-use-pep517

# Create softlink to fireside
ln -s /usr/local/Cellar/python@3.9/3.9.1_6/Frameworks/Python.framework/Versions/3.9/bin/fireside /usr/local/bin/fireside

```

---

## How to start fireside

```bash

fireside

```
+ if username not provided, randomID will be assign as username
+ if pub & sub address is not provided, fireside will start a session with default pub & sub address


```bash

# to assign user name
fireside -username user1

# start session of specific pub and sub address
fireside -pub tcp://0.0.0.0:5000 -sub tcp://0.0.0.0:5001 -username user1

```


## How to join fireside session

After the first fireside session is started, it will show the command for the other fireside to join current session

```text

    _______                _     __
   / ____(_)_______  _____(_)___/ /__
  / /_  / / ___/ _ \/ ___/ / __  / _ \
 / __/ / / /  /  __(__  ) / /_/ /  __/
/_/   /_/_/   \___/____/_/\__,_/\___/


Welcom to Fireside!!!
 >  username: dc847b4f-403b-4e0e-9224-2b1781e01245
 >  pub_address: tcp://0.0.0.0:5000
 >  sub_address: tcp://0.0.0.0:5001
Connect to this Fireside
 >  fireside -pub tcp://0.0.0.0:5000 -sub tcp://0.0.0.0:5001
 ```

The other machine just enter the command to start fireside and it will join the current session automatically

```bash
# join with randomID
fireside -pub tcp://0.0.0.0:5000 -sub tcp://0.0.0.0:5001

# join with username
fireside -pub tcp://0.0.0.0:5000 -sub tcp://0.0.0.0:5001 -username user2
 ```
