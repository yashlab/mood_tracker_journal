# mood_tracker_journal
Trying to develop a personal mood tracker and journal app using python's Flask web application framework.

## Clone the Repository

    git clone https://github.com/yashlab/mood_tracker_journal.git

Switch to the repository

## Build a local Docker Image
    docker build -t flask-mooder .

## Run your own mood-journal App

    docker run -d -p 5001:5000 \
     -v mooderapp:/app \
     --restart unless-stopped flask-mooder

A really basic version with a lot of potential to improve. I plan to scale it much higher incorporating sentiment analysis with a highly interactive user interface.

