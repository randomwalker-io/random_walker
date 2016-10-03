# Random Walker Setup

Install Docker following the section in [`Random Walker Webapp
Setup`](https://github.com/randomwalker-io/random_walker_webapp/blob/master/setup.md)

## Virtual Environment

`Virtualenv` is a tool to keep the dependencies required by different
projects in separate places, by creating virtual Python environments
for them

To setup the virtual environment, we will need to install virtualenv.

```
pip install virtualenv

```

Create the environment folder and install the required packages.

```
cd random_walker
virtualenv venv/
pip install -r requirements.txt
```

To activate the virtual environment
```
source venv/bin/activate
```

All Python packages used should be installed through `pip`, and all
current packages should be updated and saved to a requirement file.

```
pip freeze > requirements.txt
```

To deactivate the virtual environment just simply type
```
deactivate
```
