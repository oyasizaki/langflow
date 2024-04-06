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

## Issues

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

### <b>DB / alembic / user id issue</b>
Delete the files inside of the folder shown in the image and rerun langflow to solve the problem
![WhatsApp Image 2024-04-06 at 7 52 26 AM](https://github.com/oyasizaki/langflow-additional/assets/118342512/4f8f2ad7-c618-4594-972e-24ed7bbb1f0c)


