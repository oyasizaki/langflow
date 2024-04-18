## Docker based Installation ![image](https://github.com/oyasizaki/langflow-additional/assets/118342512/776fe511-7519-4a2c-baa2-e0805d646ee3) 
### <b>Locally</b>
You can install Langflow Using Docker Desktop:


#### Locating Directory
```shell
git clone https://github.com/logspace-ai/langflow.git
cd langflow
```
```shell
cd langflow
```
```shell
cd docker_example
```

#### Now edit the docker-compose.yml file as shown below .
```shell
version: "3.8"

services:
  langflow:
    image: logspace/langflow:0.6.16
    ports:
      - "7860:7860"
    depends_on:
      - postgres
    environment:
      - LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@postgres:5432/langflow
      # This variable defines where the logs, file storage, monitor data and secret keys are stored.
      - LANGFLOW_CONFIG_DIR=/var/lib/langflow
    volumes:
      - langflow-data:/var/lib/langflow

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: langflow
      POSTGRES_PASSWORD: langflow
      POSTGRES_DB: langflow
    ports:
      - "5432:5432"
    volumes:
      - langflow-postgres:/var/lib/postgresql/data

volumes:
  langflow-postgres:
  langflow-data:

```
#### <b>Or</b>
* Delete the existing docker-compose.yml
* Download the docker-compose.yml from this repo
* Save it in the `docker_example` directory


#### Finally 
`Run`:
```shell
docker-compose up -d
```

#### Accessing in browser

Go to `localhost:7860`


#### Exception
`
If you face can't reach the UI then Go to the containers in Docker desktop and make sure all the langflow container are running
it should solve the problem
`


![image](https://github.com/oyasizaki/langflow-additional/assets/118342512/b275d889-5d08-460a-93a3-98d13d320e38)


