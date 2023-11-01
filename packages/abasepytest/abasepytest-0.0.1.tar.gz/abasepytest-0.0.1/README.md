# Platform Specific Wheel
 

## Note

This package currently only support on python version 3.10 or lower , because pyarmor module is still in development for version 3.11 or higher , so you need to wait for upgrading your virtual_environment to python 3.11

This package does not need platform specific wheel it runs on devices that have python. currently it is OS independent

**IMPORTANT**
python is intrepreter language , hiding its source code from public is not easy , we are taking difficult path to hide by using pyarmor module , we are using trial version and it can only take upto 8000 lines of code i think , you need to be updated on changes that happen to pyarmor modules and its bugs and fixes

PyPi is open-source distribution , so source will be visible , we are just only encrypting it. 
If you are ok with Users or Developers seeing the source code but not public , you can just share the wheel file that have extension .whl to the users without being to uploading into PyPi repo(it is meant for open source distributers) . So in this way you can remove the use of pyarmor encryption

# Steps To Reproduce
 + install pyarmor 
	 + `pip install pyarmor`
 + make sure your python version is 3.10 or below
	 + `python --version`
+ FILE STRUCTURE
	 + ![file_structure](file_structure.png)
+ Now run pyarmor on project folder
	+ `pyarmor gen --obf-mod=1 .`
	+ if it is successful there should be dist folder 
	+ dist folder will contains two folder *pyarmor_runtime_00000* and *src*
	+  replace orginal `src` folder with `src` folder in dist folder. you can see codes in `src` folder in dist is in encrypted form
	+ move `pyarmor_runtime_00000` folder to src folder 
	+ delete `dist` folder
	+ now your file structure should be like this
    + ![after_pyarmor](after_pyarmor.png) 
+ now open pyproject.toml file and type this
    + ![pyproject](pyproject.png)

+ check your file structure for any mistakes
+ now run this in parent directory
	+ `python -m build wheel`.
	+ this will create a `dist` folder that contains wheel file
	+ you can now share this wheel file to users you want , without having to uploading into PyPI
	
# Importing the Package
`from package_name.base import DatabaseConnector , AgentRunner`
# Uploading to PyPI
The first thing you’ll need to do is register an account on PyPI, To register an account, go to [https://pypi.org/account/register/](https://pypi.org/account/register/) and complete the steps on that page. You will also need to verify your email address before you’re able to upload any packages. 

To securely upload your project, you’ll need a PyPI [API token](https://pypi.org/help/#apitoken). Create one at [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens), setting the “Scope” to “Entire account”. **Don’t close the page until you have copied and saved the token — you won’t see that token again.**

Now that you are registered, you can use [twine](https://packaging.python.org/en/latest/key_projects/#twine) to upload the distribution packages. You’ll need to install Twine:

## Installing twine
`python3  -m  pip  install  --upgrade  twine`

## Uploading with twine
Once installed, run Twine to upload all of the archives under `dist`:

*run this command on package directory*
`python3  -m  twine  upload  --repository  pypi dist/*`

You will be prompted for a username and password. For the username, use `__token__`. For the password, use the token value (API token that created in PyPI earlier), including the `pypi-` prefix.

Once uploaded your package should be visible on PyPI . Try to install it from there

# Uploading to PyPi with wheel
+ download the wheel file i send to you
+ you only need the wheel file for this , you don't need other project files


The first thing you’ll need to do is register an account on PyPI, To register an account, go to [https://pypi.org/account/register/](https://pypi.org/account/register/) and complete the steps on that page. You will also need to verify your email address before you’re able to upload any packages. 

To securely upload your project, you’ll need a PyPI [API token](https://pypi.org/help/#apitoken). Create one at [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens), setting the “Scope” to “Entire account”. **Don’t close the page until you have copied and saved the token — you won’t see that token again.**

Now that you are registered, you can use [twine](https://packaging.python.org/en/latest/key_projects/#twine) to upload the distribution packages. You’ll need to install Twine:

## Installing twine
`python3  -m  pip  install  --upgrade  twine`

## Uploading with twine
Once installed, run Twine to upload all of the archives under `dist`:

run this command on folder that contains download wheel file
`python3  -m  twine  upload  --repository  pypi *type wheel name here*`

You will be prompted for a username and password. For the username, use `__token__`. For the password, use the token value (API token that created in PyPI earlier), including the `pypi-` prefix.

Once uploaded your package should be visible on PyPI . Try to install it from there

# IMPORTANT
*if some issue persist in future , try downgrading pyarmor , and build the package by referring above steps to reproduce ,
there is change in pyarmor commands . refer to pyarmor docs*

