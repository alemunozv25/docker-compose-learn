. Start services configured in docker-compose configuration file 
docker-compose -f python-app-with-grafana_docker-compose.yml up -d


.Rebuild a single existing service:
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate nginx
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate nginx-exporter
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate python_app
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate prometheus
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate grafana
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate redis
docker-compose -f python-app-with-grafana_docker-compose.yml up -d --no-deps --build --force-recreate redis-exporter


.Stop services configured in docker-compose configuration file
docker-compose -f python-app-with-grafana_docker-compose.yml down

.Remove initially created images
docker rmi python-app-with-grafana-nginx:latest 
docker rmi python-app-with-grafana-python_app:latest
docker rmi redis:latest



