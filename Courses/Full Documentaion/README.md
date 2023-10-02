# langflow

## 📦 Direct Installation
### <b>Locally</b>
You can install Langflow from pip:

```shell
pip install langflow
```

Next, run:

```shell
python -m langflow
```
or
```shell
langflow # or langflow --help
```
### <b>Conflicting Dependency</b>

IF YOU Face any dependency version related problem then set the version while installing langflow using pip:
* first clone the github repo of langflow with git clone command
* then use cd langflow to go to the lanflow folder inside the terminal. Finally, use this command:

```shell
pip3 install "opentelemetry-sdk >=1.14.0,<1.20.0" langflow
```



## 📦 Docker based Installation
### <b>Locally</b>
You can install Langflow Using Docker Desktop:

```shell
git clone https://github.com/logspace-ai/langflow.git
cd langflow-dev
```
Next, run:

```shell
docker build -f dev.Dockerfile . -t dev.dockerfile
```
Then, run:
```shell
docker-compose up -d
```
