# Simple Bamboo SETUP 
Information related to Bamboo DataCenter setup using docker-compose.  Three containers are created via the Docker-compose file:
Bamboo Server + PostgreSQL Instance + Bamboo Agent.

Instructions for the initials step for Configuring Bamboo Server via Docker Compose can be found under https://thomassueb.medium.com/atlassian-bamboo-with-docker-compose-99bf8012b26c

# MAIN DOCKER COMPOSE COMMANDS  
* Bring up Bamboo via docker compose:  
docker-compose -f bamboo_docker-compose.yml up -d

* Rebuild a single existing service:  
docker-compose -f bamboo_docker-compose.yml up -d --no-deps --build --force-recreate bamboo
docker-compose -f bamboo_docker-compose.yml up -d --no-deps --build --force-recreate postgres_db
docker-compose -f bamboo_docker-compose.yml up -d --no-deps --build --force-recreate agent

* Stop services configured in docker-compose configuration file:  
docker-compose -f bamboo_docker-compose.yml down



# Adjustments that may be reuqired for Bambbo Setup
* Verify PostgreSQL version in Docker compose file  
Higher PostgreSQL versions may be required 

* Checking errors wehen registering the Bamboo Server  
If error "...WARN [ActiveMQ Task-1] [FailoverTransport] Failed to connect to [ssl://6a8da067bfda:54663?socket.verifyHostName=false&wireFormat.maxInactivityDuration=90000] after: 1 attempt(s) with 6a8da067bfda, continuing to retry..." appears, review the failover configuration.  
The Broker client URL can be reviewed in Administration -> System -> General Configuration  
-> Bamboo JMS broker configuration  
--> Broker client URL: failover:(ssl://6a8da067bfda:54663?socket.verifyHostName=false&wireFormat.maxInactivityDuration=90000)?initialReconnectDelay=15000&maxReconnectAttempts=10
and adjust the setup with:  
1) Change protocol and hostmane from ssl://6a8da067bfda to tcp://IP_OF_BAMBOO_SERVER of the Bamboo Server  
2) Disable socket.verifyHostName=false  
After the changes, the new Broker client URL should look like this => failover:(tcp://172.19.0.3:54663?wireFormat.maxInactivityDuration=90000)?initialReconnectDelay=15000&maxReconnectAttempts=10



# LOGGING REVIEW IN Bamboo Configuration

* CHECK LOGS for Bammbo Server container
```    
➜  bamboo docker logs bamboo_server -f
INFO:root:Generating /opt/atlassian/bamboo/conf/server.xml from template server.xml.j2
INFO:root:Generating /opt/atlassian/bamboo/atlassian-bamboo/WEB-INF/classes/seraph-config.xml from template seraph-config.xml.j2
INFO:root:Generating /opt/atlassian/bamboo/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties from template bamboo-init.properties.j2
INFO:root:/var/atlassian/application-data/bamboo/bamboo.cfg.xml exists; skipping.
INFO:root:User is currently root. Will downgrade run user to bamboo
WARNING:root:Unsetting environment var JDBC_PASSWORD
INFO:root:Running Bamboo with command '/opt/atlassian/bamboo/bin/start-bamboo.sh', arguments ['/opt/atlassian/bamboo/bin/start-bamboo.sh', '-fg']

Server startup logs are located in /opt/atlassian/bamboo/logs/catalina.out

Bamboo Data Center
   Version : 11.0.4
                  

If you encounter issues starting or stopping Bamboo Server, please see the Troubleshooting guide at https://confluence.atlassian.com/display/BAMBOO/Installing+and+upgrading+Bamboo

Using BAMBOO_HOME:       /var/atlassian/application-data/bamboo
NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
28-Aug-2025 23:29:17.705 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server] failed to set property [port] to []
28-Aug-2025 23:29:17.734 WARNING [main] org.apache.tomcat.util.digester.SetPropertiesRule.begin Match [Server/Service/Connector] failed to set property [proxyPort] to []
28-Aug-2025 23:29:17.788 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent The Apache Tomcat Native library which allows using OpenSSL was not found on the java.library.path: [/usr/java/packages/lib:/usr/lib64:/lib64:/lib:/usr/lib]
28-Aug-2025 23:29:17.901 INFO [main] org.apache.coyote.http11.AbstractHttp11Protocol.configureUpgradeProtocol The ["http-nio-8085"] connector has been configured to support HTTP upgrade to [h2c]
28-Aug-2025 23:29:17.901 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8085"]
28-Aug-2025 23:29:17.905 INFO [main] org.apache.catalina.startup.Catalina.load Server initialization in [226] milliseconds
28-Aug-2025 23:29:17.911 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
28-Aug-2025 23:29:17.911 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet engine: [Apache Tomcat/9.0.107]
28-Aug-2025 23:29:22.465 INFO [main] org.apache.jasper.servlet.TldScanner.scanJars At least one JAR was scanned for TLDs yet contained no TLDs. Enable debug logging for this logger for a complete list of JARs that were scanned but no TLDs were found in them. Skipping unneeded JARs during scanning can improve startup time and JSP compilation time.
WARNING: sun.reflect.Reflection.getCallerClass is not supported. This will impact performance.
28-Aug-2025 23:29:57.160 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8085"]
28-Aug-2025 23:29:57.197 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in [39291] milliseconds
28-Aug-2025 23:30:16.319 WARNING [http-nio-8085-exec-21 url: /rest/troubleshooting/1.0/check/bamboo_admin; user: bamboo_admin] org.glassfish.jersey.server.ResourceModelConfigurator.bindProvidersAndResources Component of class class com.atlassian.troubleshooting.healthcheck.rest.AbstractLicenseUserLimitResource cannot be instantiated and will be ignored.
```    


* CHECK LOGS for Bammbo Agent container  
```    
➜  bamboo docker logs bamboo_agent -f  
+ KUBE_NUM_EXTRA_CONTAINERS_OR_ZERO=0
+ '[' -d '' ']'
+ [[ -d /pbc/kube ]]
+ exec /usr/bin/tini -- /entrypoint.py
INFO:root:Generating /var/atlassian/application-data/bamboo-agent/conf/wrapper.conf from template wrapper.conf.j2
INFO:root:User is currently root. Will change directory ownership and downgrade run user to bamboo
INFO:root:User is currently root. Will downgrade run user to bamboo
INFO:root:Running Bamboo Agent with command '/opt/java/openjdk/bin/java', arguments ['/opt/java/openjdk/bin/java', '-Dbamboo.home=/var/atlassian/application-data/bamboo-agent', '-jar', '/opt/atlassian/bamboo/atlassian-bamboo-agent-installer.jar', 'http://bamboo:8085/agentServer']
Reinstalling wrapper binaries, reason: agent either not installed or outdated
Installing agent wrapper
Installing file: /generic/conf/wrapper-license.conf to: /var/atlassian/application-data/bamboo-agent/conf/wrapper-license.conf
Installing file: /generic/lib/wrapper.jar to: /var/atlassian/application-data/bamboo-agent/lib/wrapper.jar
Installing file: /arch/linux/arm64/wrapper to: /var/atlassian/application-data/bamboo-agent/bin/wrapper
Installing file: /arch/linux/arm64/libwrapper.so to: /var/atlassian/application-data/bamboo-agent/lib/libwrapper.so
Installing file: /generic/bin/bamboo-agent.sh to: /var/atlassian/application-data/bamboo-agent/bin/bamboo-agent.sh
Installing file: /generic/lib/bamboo-agent-bootstrap-jar-with-dependencies.jar to: /var/atlassian/application-data/bamboo-agent/lib/bamboo-agent-bootstrap.jar
Unzipping /classpath.zip to /var/atlassian/application-data/bamboo-agent/classpath
Could not find source file /classpath.zip
Agent installed
...
Running [/var/atlassian/application-data/bamboo-agent/bin/bamboo-agent.sh, console]
Agent process started, shutdown hook registered, proceeding with log pump...
Running Bamboo Agent...
STATUS | wrapper  | 2025/08/28 23:29:17 | --> Wrapper Started as Console
STATUS | wrapper  | 2025/08/28 23:29:17 | Java Service Wrapper Standard Edition 64-bit 3.5.51
STATUS | wrapper  | 2025/08/28 23:29:17 |   Copyright (C) 1999-2022 Tanuki Software, Ltd. All Rights Reserved.
STATUS | wrapper  | 2025/08/28 23:29:17 |     http://wrapper.tanukisoftware.com
STATUS | wrapper  | 2025/08/28 23:29:17 |   Licensed to Atlassian Pty Ltd for Bamboo Remote Agent
STATUS | wrapper  | 2025/08/28 23:29:17 | 
INFO   | jvm ver. | 2025/08/28 23:29:18 | openjdk version "21.0.8" 2025-07-15 LTS
INFO   | jvm ver. | 2025/08/28 23:29:18 | OpenJDK Runtime Environment Temurin-21.0.8+9 (build 21.0.8+9-LTS)
INFO   | jvm ver. | 2025/08/28 23:29:18 | OpenJDK 64-Bit Server VM Temurin-21.0.8+9 (build 21.0.8+9-LTS, mixed mode, sharing)
STATUS | wrapper  | 2025/08/28 23:29:18 | Launching a JVM...
INFO   | jvm 1    | 2025/08/28 23:29:18 | WrapperManager: Initializing...
INFO   | jvm 1    | 2025/08/28 23:29:18 | 2025-08-28 23:29:18,477 INFO [WrapperSimpleAppMain] [AgentBootstrap] Starting Agent Bootstrap using Java 21.0.8 from Eclipse Adoptium. Default charset: UTF-8, file name encoding: UTF-8
...
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,186 INFO [AgentRunnerThread] [AgentRegistrationBean] Current agent remote definition: 3c81b2c1a728 Remote agent on host 3c81b2c1a728
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,411 INFO [AgentRunnerThread] [AgentRegistrationBean] Registering agent on the server,
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,703 INFO [AgentRunnerThread] [AgentRegistrationBean] Definition from the server: 3c81b2c1a728 Remote agent on host 3c81b2c1a728
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,703 INFO [AgentRunnerThread] [AgentRegistrationBean] Configuration has been changed, saving changes...
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,705 INFO [AgentRunnerThread] [CachingAdministrationConfigurationAccessor] Requesting AdministrationConfiguration
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,715 INFO [AgentRunnerThread] [CachingSerializationSecurityConfigAccessor] Administration configuration was updated from server
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,729 INFO [AgentRunnerThread] [AgentMessageListenerContainer] Configuring message selector: allowableAgents = '1998849' AND fingerprint = '-5337496098885077138'
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,740 INFO [AgentRunnerThread] [PluginSystemStartupUtils] Verifying availability of mission critical plugins...
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,740 INFO [AgentRunnerThread] [PluginSystemStartupUtils] All mission critical plugins have started.
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,740 INFO [AgentRunnerThread] [DefaultBuildAgent] Ensuring the temp path '/tmp' exists.
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,742 INFO [AgentRunnerThread] [DefaultBuildAgent] Build agent '3c81b2c1a728' started. Waiting for builds...
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,742 INFO [2-BAM::3c81b2c1a728::Agent:Thread-17] [RemoteAgentCipherProviderService] Requesting agent cipher..
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,752 INFO [AgentRunnerThread] [AgentHeartBeatJobScheduler] Scheduled AgentHeartBeatJobScheduler to run every 60s. Next run at Thu Aug 28 23:31:09 UTC 2025
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,764 INFO [AgentRunnerThread] [QuartzScheduler] Scheduler scheduler_$_NON_CLUSTERED started.
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] ********************************************************************************************************************************************
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] *                                                                                                                                          *
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] * Bamboo agent '3c81b2c1a728' ready to receive builds.
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] * Remote Agent Home: /var/atlassian/application-data/bamboo-agent
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] * Broker URL: failover:(tcp://172.19.0.3:54663?wireFormat.maxInactivityDuration=90000)?initialReconnectDelay=15000&maxReconnectAttempts=10
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] *                                                                                                                                          *
INFO   | jvm 7    | 2025/08/28 23:31:09 | 2025-08-28 23:31:09,786 INFO [AgentRunnerThread] [RemoteAgent] ********************************************************************************************************************************************
...
```

* CHECK LOGS for PostgreSQL container
```    
➜  bamboo docker logs bamboo_postgres -f

PostgreSQL Database directory appears to contain a database; Skipping initialization

2025-08-28 23:29:17.366 UTC [1] LOG:  starting PostgreSQL 14.19 (Debian 14.19-1.pgdg13+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
2025-08-28 23:29:17.366 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2025-08-28 23:29:17.366 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2025-08-28 23:29:17.367 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2025-08-28 23:29:17.369 UTC [27] LOG:  database system was shut down at 2025-08-28 23:29:11 UTC
2025-08-28 23:29:17.372 UTC [1] LOG:  database system is ready to accept connections
```