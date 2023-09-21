# This readme file describes how to setup local TA environment
## Prerequisites
1.  PyCharm
2.  Python 3.10+

## Installation

### Install Allure
1. Install Allure cmd tool
   - Mac: `brew install allure`
   - Linux debian:
   ```
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```
   - Windows:
      `scoop install allure`
2. Install Java and add JAVA and JAVA_HOME to enw variables

More details you can find by the [link](https://docs.qameta.io/allure/#_installing_a_commandline)

### Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate
```

### Install packages
In PyCharm Open `requirements.txt` -> Right click -> Install All Packages 

OR

`pip install -r requirements.txt`

## Configuration
### Behave configuration 

The configuration for behave plugin located in `behave.ini` file:

[behave.userdata]

`AllureFormatter.link_pattern` - pattern for TMS link 

`AllureFormatter.issue_pattern` - pattern for issue link 

Example of using: 
````
@allure.link.TMS_CP-111:CP-111 @allure.issue.BUG_CP-222:CP-222
Scenario: Successful login
````

[behave]

`default_features` - your feature file .feature

`format` - formatter for behave plugin, alternative of `-f` in cmd

`outfiles` - Allure result folder

### Test configuration
To configure tests environment create `.env` file based on `.env_example`. 

```
BASE_URL= "http://cp-local:8080/"
BROWSER = "chrome"
HEADLESS = "False"
MAXIMIZE = "True"
```

## Build and Test
To build all packages, run:
`python setup.py install`  
To run tests, run shall command:
`behave`

## Setup debug for the PyCharm
#### Setting up PyCharm CE debugger to run Behave
1. Go to "Run" in the top and click "Edit configurations…"
2. Specify the type of target as "module name"
3. Type Behave, since this is the module is the one we want to execute.
4. In the parameters section point to your features' directory.
5. In the work directory specify root folder.
6. That's it! Now all you have to do is place your breakpoints and hit the bug icon.
In this case all feature files will be run. You can configure which feature should be run in `behave.ini` file:

#### Use Runner 
1. Go to "Run" in the top and click "Edit configurations…"
2. Add new configuration and select Python
3. In script path select ./features/runner.py
4. In the work directory specify root folder.
5. You can configure which feature should be run in `./features/runner.py` by adding `fixture_to_run.feature`
6. That's it! Now all you have to do is place your breakpoints and hit the bug icon. 

## Generate and open Allure report
After test run, behave_allure generate result folder.
To Open generated Allure report, run shall command:

`allure serve test_result`