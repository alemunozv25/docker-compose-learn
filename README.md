# docker-compose-learn
Different tests with docker-compose setups.

# Folders
* python-app-with-grafana:  
Docker-compose setup to test use of Grafana monitoring Nginx, Redis and basic Python app created with Flask.  Prometheus is integrated for the scraping of the relevant metrics for each component. More details on how to bring up the environment is provided in the Readme file inside the folder.

* gitlab:  
Docker-compose setup to test use of GitLab CE together with Gitlab Runner. More details on how to bring up the environment is provided in the Readme file inside the folder.

* bamboo-setup:  
Docker-compose setup to test Bamboo DataCenter.  Three containers are created via the Docker-compose file: Bamboo Server + PostgreSQL Instance + Bamboo Agent.