# Random Walker Setup

Follow the setup guide for the [`Random Walker Webapp`](https://github.com/randomwalker-io/random_walker_webapp/blob/master/setup.md)

A initialisation script is provided, simply run the following to complete the
setup.

```
sudo sh init.sh
```

Details of the execution is provided below


## Virtual Environment

`Virtualenv` is a tool to keep the dependencies required by different
projects in separate places, by creating virtual Python environments
for them

To setup the virtual environment, we will need to install virtualenv.

```
pip install virtualenv

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

If a requirement file which lists all the package required, they can
be installed via

```
pip install -r requirements.txt
```

To deactivate the virtual environment just simply type
```
deactivate
```


## Configuration

The `random walker` app requires additional credentials to be executed. The
credential is stored on AWS S3 for security reason.

