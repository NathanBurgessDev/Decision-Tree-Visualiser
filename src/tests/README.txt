###################################
Run tests in the following way:
###################################

 - Navigate to an appropriate directory (in the exmple I use the src directory)

 - run the following command
   >> python -m pytest --cov-report=html --cov=callbacks/callbacks/ tests/test_callbacks

 - --cov-report=html creates the index.html file to display the
   code coverage

 - --cov=callbacks/callbacks/ specifies the path from the
   current directory to the src code being tested

 - tests/test_callbacks specifies the path from the current
   directory to the location where the tests are stored

This creates an index.html page in src/htmlcov/, which can be
viewed to asses code line coverage

To run all tests and asses line coverage of all src files you can run

>> python -m pytest --cov-report=html --cov=../src  tests/

###################################
Requirements:
###################################

 - pytest
 - coverage

###################################
Install using the following cmds:
###################################

>> python -m pip install pytest
>> python -m pip install coverage

Example unit testing of dash callbacks can be found
in tests/test_callbacks/test_SettingCallbacks.py