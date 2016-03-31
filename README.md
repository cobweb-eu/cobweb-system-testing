COBWEB System Testing
=====================

## Requirements
- A device or image with Android 4.4+
- Python 2.7 with pip
- Android Debug Bridge (Included in the Android SDK)
- Chrome


## Install

```
# Install python requirements (virtualenv recommended)
pip install -r etc/requirements.txt

# Install appium
npm install -g appium

# Install chromedriver
npm install -g chromedriver
```

## Run the tests

- Connect a device or start the Android emulator and check that is visible with the ```adb devices``` command
- Start appium in a terminal
  ```
  appium
  ```
- Start the tests in a different terminal
  ```
  # Run all tests
  py.test selenium/*.py
  ```

  ```
  # Run an individual test
  py.test selenium/cobweb_anon_use_case_tests.py
  ```
