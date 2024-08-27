#!/bin/bash

# Pull the latest changes from the master branch
git pull origin master

# Activate the virtual environment
source /home/applications/myLibrary/venv/bin/activate  # Adjust path to your virtual environment

# Install any new dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart the Django development server (stop it if it's already running)
sudo pkill -f 'manage.py runserver'  # Kill existing server process if running

# Start the Django development server in the background
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
