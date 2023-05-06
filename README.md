# Treasure Hunt

API for TreasureHut used by LoyalBart.

# Run

* Create a virtual environment and install the required dependencies
bash
```
pyenv virtualenv 3.11.2 TreasureHunt
pyenv activate TreasureHunt
pip install -r requirements.txt
```

* Start gunicorn server witn PM2
bash
```
pm2 --name TreasureHunt start start.sh
```

# Deploy in Docker

* Build the container

```
docker build -t treasurehunt .
```

* Start the container

```
docker run treasurehunt
```