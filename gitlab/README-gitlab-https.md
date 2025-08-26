# GITLAB HTTPS SETUP 
For common http setup verify README-gitlab-hhtp.md. In this file only additional setup relate to HTTPS is included.

# MAIN DOCKER COMPOSE COMMANDS  
* Bring up Gitlab via docker compose:  
docker-compose -f gitlab-https_docker-compose.yml up -d

* Rebuild a single existing service:  
docker-compose -f gitlab-https_docker-compose.yml up -d --no-deps --build --force-recreate gitlab
docker-compose -f gitlab-https_docker-compose.yml up -d --no-deps --build --force-recreate gitlab-runner

* Stop services configured in docker-compose configuration file:  
docker-compose -f gitlab-https_docker-compose.yml down
  

# Certificate information in GITLAB_OMNIBUS_CONFIG
Gitlab setup can use Let's Encrypt certificates for valid Internet Domains of Self-signed Certificates for other domains.
In this setup, self-signed Certificates are used:

> Changes with reference to http setup in the docker-compose file:
> All references to HTTP must change to HTTPS and certificate information location must also be included.
```
      GITLAB_OMNIBUS_CONFIG: |
        letsencrypt['enable'] = false
        external_url 'https://gitlab.test:8443'
        nginx['listen_port'] = 443
        nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.test.crt"
        nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.test.key"
        registry_external_url 'https://gitlab.test:5500'
        gitlab_rails['gitlab_kas_external_url'] = 'wss://gitlab.test:8443/-/kubernetes-agent/'
        gitlab_kas_external_url "wss://gitlab.test:8443/-/kubernetes-agent/"
        gitlab_kas['gitlab_address'] = 'https://gitlab.test:443'
        gitlab_kas['env'] = {
          'SSL_CERT_DIR' => '/etc/gitlab/ssl/'
        }
```

# Self-signed Cetificate creation
In MacOS, Self-signed certificates can be creates using the "Certificate Assistant" under Keychain Access component. 
Details can be found under https://support.apple.com/guide/keychain-access/create-self-signed-certificates-kyca8916/mac

* Extract Certificate from p12 file:  
openssl pkcs12 -in gitlab.test.p12 -nokeys -legacy -out gitlab.test.crt

* Extract Private Key from p12 file:   
openssl pkcs12 -in gitlab.test.p12 -nocerts -nodes -legacy -out gitlab.test.key


# Where to copy Self-signed Certification information
The self-certificate information must be made available to every single component that interacts with Gitlab. 


> Copy Certificate + Private Key to Gitlab container
>>➜  docker cp ./gitlab.test.crt gitlab:/etc/gitlab/ssl/gitlab.test.crt  
>>Successfully copied 3.58kB to gitlab:/etc/gitlab/ssl/gitlab.test.crt  
>>Error response from daemon: Could not find the file /etc/gitlab/ssl in container gitlab  
  
>>Make sure that folder etc/gitlab/ssl exists in container gitlab and retry  

>>➜  docker cp ./gitlab.test.crt gitlab:/etc/gitlab/ssl/gitlab.test.crt  
>>Successfully copied 3.58kB to gitlab:/etc/gitlab/ssl/gitlab.test.crt  

>>➜  docker cp ./gitlab.test.key gitlab:/etc/gitlab/ssl/gitlab.test.key  
>>Successfully copied 3.58kB to gitlab:/etc/gitlab/ssl/gitlabcertificate-key.pe  


> Copy Certificate + Private Key to Gitlab-Runner container
>>➜  docker cp ./gitlab.test.crt gitlab-runner:/etc/gitlab-runner/certs/gitlab.test.crt  
>>Successfully copied 3.07kB to gitlab-runner:/etc/gitlab-runner/certs/gitlab.test.crt  

> Make sure that the trusted certificates folder is used inside Gitlab-Runner container  
>> cp /etc/gitlab/ssl/* /etc/gitlab/trusted-certs/ 

> Include certificate information in KAS helm chart command in Kubernetes setup (if in use)
>>helm upgrade --install {name} gitlab/gitlab-agent \
    --namespace gitlab-agent-{name} \
    --create-namespace \
    --set image.tag=v18.2.0 \
    --set config.token=glagent-{omitted} \
    --set config.kasAddress=wss://192.168.1.1:8443/-/kubernetes-agent/ \
    --set-file config.kasCaCert=/path/to/gitlab.test.crt
