# GITLAB HTTP SETUP 
Information related to GITLAB HTTP setup is included in this file.

# MAIN DOCKER COMPOSE COMMANDS  
* Bring up Gitlab via docker compose:  
docker-compose -f gitlab-http_docker-compose.yml up -d

* Rebuild a single existing service:  
docker-compose -f gitlab-http_docker-compose.yml up -d --no-deps --build --force-recreate gitlab
docker-compose -f gitlab-http_docker-compose.yml up -d --no-deps --build --force-recreate gitlab-runner

* Stop services configured in docker-compose configuration file:  
docker-compose -f gitlab-http_docker-compose.yml down
  

# GITLAB INITIAL START
* To get initial password of root:  
sudo docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password  
  

# CREATE SSH keys 
Command to create ssh keys to be used with GIT SETUP:  
- ssh-keygen -t ed25519 -C "<gmail_user>@gmail.com"

a) Make sure local ssh-agent knows about the newly generated key: 
- eval "$(ssh-agent -s)"  
Agent pid 25567
 
- ssh-add -l  
The agent has no identities.

- ssh-add -L  
The agent has no identities.

b) Add new ssh key
- ssh-add gitlab_ed25519  
Identity added: gitlab_ed25519 (<gmail_user>@gmail.com)

c) Copy newly created SSH key to Gitlab  
- This is done under each user in the Gitlab instance

d) Perform git clone using SSH to Gitlab Instance  
- git clone ssh://git@gitlab.test:2424/it-infrastructure/empty-project.git
 


# LOGGING REVIEW IN GITLAB INSTANCE

* LOGS DIR FOR GITLAB CONTAINER  
docker exec -it gitlab bash  
root@gitlab:/# cd /var/log/gitlab  
root@gitlab:/var/log/gitlab#  
root@gitlab:/var/log/gitlab# ls   
alertmanager  gitlab-exporter  gitlab-rails  gitlab-workhorse  nginx              postgresql  puma         redis           registry  sshd
gitaly        gitlab-kas       gitlab-shell  logrotate         postgres-exporter  prometheus  reconfigure  redis-exporter  sidekiq  
...Check individual folders logs for Gitlab container depending on needs


* CHECK LOGS FOR GITLAB-RAILS  
docker exec -it gitlab bash  
root@gitlab:/# cd /var/log/gitlab/gitlab-rails  
root@gitlab:/var/log/gitlab/gitlab-rails# pwd  
/var/log/gitlab/gitlab-rails   
root@gitlab:/var/log/gitlab/gitlab-rails# ls -als  
  

* CHECK LOGS FOR GITLAB SHELL   
docker exec -it gitlab bash  
root@gitlab:/# more /var/log/gitlab/gitlab-shell/gitlab-shell.log   
...


* CHECK LOGS for GIT IN GITLAB
root@gitlab:/var/log/gitlab# gitlab-ctl tail nginx | grep git-upload-pack  
```
172.19.x.x - - [02/Aug/2025:22:18:53 +0000] "GET /it-infrastructure/empty-project.git/info/refs?service=git-upload-pack HTTP/1.1" 401 348 "" "git/2.43.0" - 
172.19.x.x - gitlab-ci-token [02/Aug/2025:22:18:53 +0000] "GET /it-infrastructure/empty-project.git/info/refs?service=git-upload-pack HTTP/1.1" 200 163 "" "git/2.43.0" -
172.19.x.x - gitlab-ci-token [02/Aug/2025:22:18:53 +0000] "POST /it-infrastructure/empty-project.git/git-upload-pack HTTP/1.1" 200 215 "" "git/2.43.0" -
172.19.x.x - gitlab-ci-token [02/Aug/2025:22:18:53 +0000] "POST /it-infrastructure/empty-project.git/git-upload-pack HTTP/1.1" 200 5514 "" "git/2.43.0" -
```

* Other directories that may be of interest are nginx, gitlab-workhorse, logrotate depending on need.


# GITLAB RUNNERS / RUNNERS REGISTRATION 
A "GitLab Runner is an application that works with GitLab CI/CD to run jobs in a pipeline" according to https://docs.gitlab.com/runner/.  It is where the 
CI/CD instructions are executed when connect to Gitlab.  There are several types of runners in gitlab which are called executor.  The most common are shell 
and different types of docker setups.  

In the main docker-compose setup, there is a container for a Gitlab runner container.   
 

# GITLAB RUNNERS REGISTRATION 
Base doc is at https://docs.gitlab.com/runner/register/

1) Create the Gitlab runner under Admin -> Runners of the Administrative console of Gitlab Instance


2) Runner Registration:  
2.1) For DOCKER EXECUTOR 
docker exec -it gitlab-runner bash  
root@b9c38ab59a5b:/# gitlab-runner register  --url http://gitlab.test  --token <TOKEN-INFO>  
Runtime platform                                    arch=arm64 os=linux pid=36 revision=cc489270 version=18.2.1
Running in system-mode.
```                            
Enter the GitLab instance URL (for example, https://gitlab.com/):  
[http://gitlab.test]:   
Verifying runner... is valid                        correlation_id=01K1H3VF2JMJYDHPY4MV63WR9S runner=2HrqUGAer
Enter a name for the runner. This is stored only in the local config.toml file:  
[b9c38ab59a5b]:  
Enter an executor: parallels, virtualbox, docker-windows, docker+machine, docker-autoscaler, docker, kubernetes, instance, custom, shell, ssh:  
docker  
Enter the default Docker image (for example, ruby:3.3):  
ubuntu:24.04  
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!  
Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml"
```
```
root@b9c38ab59a5b:/#
root@b9c38ab59a5b:/#
root@b9c38ab59a5b:/# more /etc/gitlab-runner/config.toml
concurrent = 1
check_interval = 0
shutdown_timeout = 0
[session_server]
  session_timeout = 1800
[[runners]]
  name = "b9c38ab59a5b"
  url = "http://gitlab.test"
  id = 1
  token = <TOKEN-INFO>
  token_obtained_at = 2025-07-31T20:47:49Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "ubuntu:24.04"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
    network_mtu = 0
root@b9c38ab59a5b:/#
```

2.2) For SHELL EXECUTOR 
docker exec -it gitlab-runner bash  
root@b9c38ab59a5b:/# gitlab-runner register  --url http://gitlab.test  --token <TOKEN-INFO>  
Runtime platform                                    arch=arm64 os=linux pid=58 revision=cc489270 version=18.2.1
Running in system-mode.                            
```              
Enter the GitLab instance URL (for example, https://gitlab.com/):
[http://gitlab.test]: 
Verifying runner... is valid                        correlation_id=01K1H4Z3THWGJXR1P54PQEJ5RG runner=3ufUY60zK
Enter a name for the runner. This is stored only in the local config.toml file:
[b9c38ab59a5b]: 
Enter an executor: docker+machine, kubernetes, shell, ssh, docker, docker-windows, docker-autoscaler, instance, custom, parallels, virtualbox:
shell
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
 
Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml"
```
root@b9c38ab59a5b:/# 
root@b9c38ab59a5b:/# more /etc/gitlab-runner/config.toml
```
[[runners]]
  name = "b9c38ab59a5b"
  url = "http://gitlab.test"
  id = 2
  token = <TOKEN-INFO>
  token_obtained_at = 2025-07-31T21:07:18Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "shell"
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
```



2.3) SETTING UP A CUSTOM NETWORK DURING GITLAB-RUNNER REGISTRATION:
If a non default network is used during the docker-compose configuration, it is necessary to include information about the network to 
establish proper communication between the Gitlab runner and the Gitlab instance. For this option, the "--docker-network-mode" option 
can be used during the Runner registration
 
gitlab-runner register  --url http://gitlab.test  --token <TOKEN-INFO> --docker-network-mode gitlab_gitlab_net  
root@956bef7206a5:/etc/gitlab-runner# gitlab-runner register  --url http://gitlab.test  --token <TOKEN-INFO>  --docker-network-mode gitlab_gitlab_net  
Runtime platform                                    arch=arm64 os=linux pid=352 revision=cc489270 version=18.2.1
Running in system-mode.                            
```                   
Enter the GitLab instance URL (for example, https://gitlab.com/):
[http://gitlab.test]: 
Verifying runner... is valid                        correlation_id=01K204C8T0JE188RJZG8R300WN runner=T9s67m7ns
Enter a name for the runner. This is stored only in the local config.toml file:
[956bef7206a5]: DockerRunner4
Enter an executor: custom, ssh, parallels, virtualbox, docker, docker-windows, kubernetes, instance, shell, docker+machine, docker-autoscaler:
[docker]: 
Enter the default Docker image (for example, ruby:3.3):
[alpine:3.22]: 
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
 
Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml" 
```


2.4) RECONFIGURE URL to use to communicate to Gitlab Instance
Sometimes the defined URL used to communicate can have issues (port missmatch or others) and therefore it may be necessary to make sure the URL of the 
Gitlab instance is well defined. For this, the option "--clone-url" can be used.

gitlab-runner register --url http://gitlab.test --token <TOKEN-INFO> --docker-network-mode gitlab_gitlab_net --clone-url http://gitlab.test:80  

root@956bef7206a5:/etc/gitlab-runner# gitlab-runner register --url http://gitlab.test --token <TOKEN-INFO> --clone-url http://gitlab.test:80 --docker-network-mode gitlab_gitlab_net  
Runtime platform                                    arch=arm64 os=linux pid=370 revision=cc489270 version=18.2.1
Running in system-mode.                            
```                                                 
Enter the GitLab instance URL (for example, https://gitlab.com/):  
[http://gitlab.test]: 
Verifying runner... is valid                        correlation_id=01K205B8AR4JPWE7D5HHP0R33K runner=JAI5xsNG8
Enter a name for the runner. This is stored only in the local config.toml file:
[956bef7206a5]: DockerRunner5
Enter an executor: custom, shell, ssh, parallels, virtualbox, docker-windows, kubernetes, docker-autoscaler, docker, docker+machine, instance:
[docker]: 
Enter the default Docker image (for example, ruby:3.3):
[alpine:3.22]: 
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
 
Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml"
```


2.5) Example of RUNNER using both "clone_url" and "network_mode" options  

root@b9c38ab59a5b:/# more /etc/gitlab-runner/config.toml
```
[[runners]]
  name = "dind1"
  url = "http://gitlab.test"
  id = 5
  token = <TOKEN-INFO>
  token_obtained_at = 2025-08-05T15:57:35Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  clone_url = "http://gitlab.test:80"
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "docker:24.0.5"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    network_mode = "gitlab_gitlab_net"
    shm_size = 0
    network_mtu = 0
```

---
---

# CHECKING LOGS FOR GITLAB-RUNNER CONTAINER
docker logs --follow gitlab-runner   
```  
Getting source from Git repository      job=119 project=3 runner=wDCSWtmM3
Executing on /runner-wdcswtmm3-project-3-concurrent-0-4ebac8d1bfe6410f-predefined the #!/usr/bin/env bash

trap exit 1 TERM
```


