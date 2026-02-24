#!/bin/bash
cd /home/bapi/personal_project/RoleMatch
source venv/bin/activate
python -m scripts.job_fetchers
python -m scripts.send_mail