# langflow

### 📦 <b>Installing packaged langflow (version control)</b>

```shell
git clone https://github.com/oyasizaki/langflow-additional.git
```
```shell
cd Version_Control
```


```shell
pip install -r requirements_<version>.txt
```

## 🔥 Direct Installation
### <b>Locally</b>
You can install Langflow from pip:

```shell
pip install langflow
```

Next, run:
```shell
langflow run # or langflow --help
```

or

```shell
python -m langflow
```
### <b>Version</b>
To install a specific version of langflow 
```shell
pip install langflow==<version>
```
For example:
```shell
pip install langflow==0.5.0
```
Acc setup:
```shell
langflow superuser --username=test --password=test
```
To run:
```shell
langflow run
```




### <b>Dependencies</b>
CTransformers
```shell
pip install ctransformers
```
llama-cpp-python
```shell
pip install llama-cpp-python
```
sentence-transformers
```shell
pip install -U sentence-transformers
```



### <b>Conflicting Dependency</b>

IF YOU Face any dependency version related problem then set the version while installing langflow using pip:
* first clone the github repo of langflow with git clone command
* then use cd langflow to go to the lanflow folder inside the terminal. Finally, use this command:
```shell
pip3 install "dependency_name >=Supported_version_begining_number,<Supported_version_ending_number" langflow
```
For example :
```shell
pip3 install "opentelemetry-sdk >=1.14.0,<1.20.0" langflow
```
##### jq problem solution for windows
```shell
pip install langflow==0.6.3a1
```




![image](https://github.com/oyasizaki/langflow-additional/assets/118342512/776fe511-7519-4a2c-baa2-e0805d646ee3) 

## Docker based Installation
### <b>Locally</b>
You can install Langflow Using Docker Desktop:

```shell
git clone https://github.com/logspace-ai/langflow.git
cd langflow
```
Next, run:
```shell
cp .env.example .env
```
Now edit the .env file and fill -up the detalis
```shell
# Description: Example of .env file
# Usage: Copy this file to .env and change the values
#        according to your needs
#        Do not commit .env file to git
#        Do not change .env.example file

# Database URL
# Postgres example: LANGFLOW_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/langflow
# SQLite example:
LANGFLOW_DATABASE_URL=sqlite:///./langflow.db

# Cache type
LANGFLOW_LANGCHAIN_CACHE=SQLiteCache

# Server host
# Example: LANGFLOW_HOST=127.0.0.1
LANGFLOW_HOST=127.0.0.1

# Worker processes
# Example: LANGFLOW_WORKERS=1
LANGFLOW_WORKERS=1

# Server port
# Example: LANGFLOW_PORT=7860
LANGFLOW_PORT=7860

# Logging level
# Example: LANGFLOW_LOG_LEVEL=critical
LANGFLOW_LOG_LEVEL=critical

# Path to the log file
# Example: LANGFLOW_LOG_FILE=logs/langflow.log
LANGFLOW_LOG_FILE=logs/langflow.log

# Path to the frontend directory containing build files
# Example: LANGFLOW_FRONTEND_PATH=/path/to/frontend/build/files
LANGFLOW_FRONTEND_PATH=/path/to/frontend/build/files

# Whether to open the browser after starting the server
# Values: true, false
# Example: LANGFLOW_OPEN_BROWSER=true
LANGFLOW_OPEN_BROWSER=true

# Whether to remove API keys from the projects saved in the database
# Values: true, false
# Example: LANGFLOW_REMOVE_API_KEYS=false
LANGFLOW_REMOVE_API_KEYS=false

# Whether to use RedisCache or InMemoryCache
# Values: memory, redis
# Example: LANGFLOW_CACHE_TYPE=memory
# If you want to use redis then the following environment variables must be set:
# LANGFLOW_REDIS_HOST (default: localhost)
# LANGFLOW_REDIS_PORT (default: 6379)
# LANGFLOW_REDIS_DB (default: 0)
# LANGFLOW_REDIS_CACHE_EXPIRE (default: 3600)
LANGFLOW_CACHE_TYPE=memory

# Superuser username
# Example: LANGFLOW_SUPERUSER=admin
LANGFLOW_SUPERUSER=admin

# Superuser password
# Example: LANGFLOW_SUPERUSER_PASSWORD=123456
LANGFLOW_SUPERUSER_PASSWORD=123456

# STORE_URL
# Example: LANGFLOW_STORE_URL=https://api.langflow.store
LANGFLOW_STORE_URL=https://api.langflow.store

# DOWNLOAD_WEBHOOK_URL
#
LANGFLOW_DOWNLOAD_WEBHOOK_URL=

# LIKE_WEBHOOK_URL
#
LANGFLOW_LIKE_WEBHOOK_URL=
```
Then, run:
```shell
docker-compose up -d
```
#### exception
```shell
docker build -f dev.Dockerfile . -t dev.dockerfile
```

