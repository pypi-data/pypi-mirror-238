
  

# 2023_assignment1_urluckynum

  

*Software Development Process* course

Academic Year 2023-24

Master's degree course in Computer Science

University of Milan-Bicocca

  

  

## Group members

  

  

  

- Cristian Piacente 866020

  

  

- Marco Gherardi 869138

  

  

- Matteo Cavaleri 875050

  

  

  

## Application

  

  

  

This Python application shows the user's lucky number.

  

  

Through a database, it stores the lucky number associated with a certain user and returns it. If the user is not registered, it generates a number, saves it to the database, and returns it to the user.

  

  

## Pipeline

  

This CI/CD pipeline is based on the **python:3.8** image, as our application was written in Python.

  

---

  

### Services

  

-  **mysql**: Used for starting the MySQL server.

-  **python**: Used for performing various tasks in the pipeline jobs.

  

---

  

### Global Variables

  

-  `MYSQL_ROOT_PASSWORD`: Required for the MySQL service; it stores the password for the MySQL root user, which is, by default, the same as the `$MYSQL_PASSWORD` variable.

-  `MYSQL_DATABASE`: Specifies the database name to use in the MySQL service; by default, it's *sys*.

-  `MYSQL_USER`: A project-level variable containing the username of the desired MySQL user.

-  `MYSQL_PASSWORD`: A project-level variable containing the MySQL user password.

-  `TWINE_TOKEN`: A project-level variable containing the PyPI token, used for publishing the Python application in the release stage.

  

`TWINE_TOKEN` is protected, accessible only on protected branches of the repository, like other project-level variables. It's also masked to avoid displaying its content when `twine` is invoked. `MYSQL_USER` and `MYSQL_PASSWORD` do not need to be masked because no task outputs them in the console.

  

---

  

### Cached Paths

  

The following paths are stored in the global cache:

  

-  `venv/`: The Python virtual environment.

-  `urluckynum/app/__pycache__/`: The Python directory that contains the bytecode.

  

---

  

### before_script

  

Since every job requires Python, the following two commands are executed before each job:

  

-  `python -m venv venv`

-  `source venv/bin/activate`

  
  
  
  

---

  

### Build stage

  

#### Script

  

    pip install -r urluckynum/requirements.txt

  

#### Explanation

  

All the dependencies are stored in a file named **requirements.txt** (located in the urluckynum directory), and they are automatically installed by pip during this stage. Afterward, the cache mechanism is used to make the packages available for the next stages.

  

---

  

### Verify stage

  

#### Script

  

    prospector
    
    bandit -r urluckynum/

  

#### Explanation

  

This stage utilizes two libraries, **prospector** and **bandit**, for code quality checks and security analysis to ensure project quality.

  

Bandit, which performs security analysis on the code, takes the parameter `-r` to specify the path and check for security vulnerabilities in that directory and its subdirectories.

  

---

  

### Unit test stage

  

#### Script

  

    pytest -k "unit"

  
  

#### Explanation

  
  

This stage conducts a unit test using **pytest**.

  

Unit tests verify the functionality of individual code units, such as functions. In this case, the test focuses on the generation of a random number.

  

Pytest can distinguish between unit and integration tests by examining **markers** defined above the signature of a test function, and these markers are specified in the pytest.ini configuration file.

  

The `-k` parameter specifies the marker.

---

  

### Integration test stage

  

#### Job variables

  

-  `DB_HOST`: MySQL hostname, specifying the host to connect to. By default, it's set to *mysql* because this setting is required to connect to the GitLab MySQL service. However, our Python application also supports connections to external servers.

-  `DB_PORT`: MySQL port, with a default value of 3306.

  

#### Script

  

    pytest -k "integration" --gitlab-user=$GITLAB_USER_LOGIN --db-name=$MYSQL_DATABASE --db-host=$DB_HOST --db-port=$DB_PORT --db-user=$MYSQL_USER --db-password=$MYSQL_PASSWORD

  
  

#### Explanation

  

This stage conducts integration tests using **pytest**. Integration tests verify that different parts of a system work together correctly, in this case, the **backend** and **database**. These tests are labeled with the integration marker, ensuring that pytest runs only those specific tests.

  

In addition, this stage provides the GitLab user and MySQL database credentials to the tests, enabling them to interact with these systems.

  

In this scenario, the application attempts to execute all the necessary tasks to display the user's lucky number. First, it connects to the database, then it executes queries to retrieve the user's lucky number (or stores it if the user is new). The user is identified by the `$GITLAB_USER_LOGIN` predefined variable, which contains the GitLab username.

  
  

---

  

### Package stage

  

#### Script

  

    python setup.py sdist bdist_wheel

  

#### Artifacts

  

-  `dist/*.whl`: Built Distribution

-  `dist/*.tar.gz`: Source Distribution

  

#### Explanation

  

In this stage, we used the libraries **setuptools** and **wheel**. We created a file, `setup.py`, to configure the package's structure correctly. The command `python setup.py sdist bdist_wheel` has two parameters because we need to create two artifacts: `sdist` is responsible for the creation of the source distribution (.tar.gz file), and `bdist_wheel` is responsible for the creation of the built distribution (.whl file). These two files are essential for the release stage.

  

---

  

### Release stage

  

The job that implements this stage can only be executed in the main branch.

  

#### Script

  
  

    echo "[pypi]" > .pypirc
    echo "username = __token__" >> .pypirc
    echo "password = $TWINE_TOKEN" >> .pypirc
    
    twine upload --config-file .pypirc dist/*

  

#### Explanation

  

The release stage exploits the **twine** library to publish the two artifacts produced in the previous stage (package) on **PyPI**, using a token (defined in a project-level variable).

  

Before using twine, this stage creates a .pypirc configuration file which has this structure:

  

    [pypi]
    username = __token__
    password = $TWINE_TOKEN

  

The first line is the file header. The username must be `__token__` to specify a PyPI token is being used instead of credentials. Then, the $TWINE_TOKEN variable, used as the password, contains the secret needed to perform the upload.

  

---

  

### Docs stage

  

The job that implements this stage can only be executed in the main branch.

  

#### Script

  

    pdoc -o public urluckynum/app

  

#### Artifacts

  

-  `public/`: This directory contains the static website generated by the pdoc library.

  
  

#### Explanation

  

The `docs` stage is implemented by the `pages` job. This job automatically generates a static website using the Python **pdoc** library, which retrieves information from the docstrings defined for each function in the `urluckynum/app` module. The command `pdoc -o public urluckynum/app` generates the website in the `public` folder using the `-o` parameter. The generated website is made available for the next automatic job, `pages:deploy`, which publishes the files on GitLab Pages based on the content in the `public` folder.

  
  

---

  



## Issues encountered

  
  

 - ### Testing
   
     
   
   #### Problem
   
     
   
   The tests, which are located in the ./tests folder, face the issue of
   not being able to access the app modules stored in ./urluckynum/app.
   For example, the unit test stage requires the use of the
   `generate_lucky_number` function defined in `urluckynum.app.lucky`.
   
     
   
   #### Solution
   
     
   
   To address this issue, we added the following line of code:
   
     
   
   >  `sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")`
   
     
   
   This code fixes the problem by adding the project root folder to the
   path variable, allowing the test files to access the "urluckynum"
   package and consequently, the app module that contains `lucky.py` and
   other essential Python source code files.
