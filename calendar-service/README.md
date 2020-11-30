# Build Procedure
In the calendar-service directory
1. Run `make deps` to start the virtual environment and install all the required dependencies.
2. Run `make fb-init` initialize the Firebase project directory, you will likely be prompted to type your computer password, then follow the on-screen instructions to select the following options:
    - Select "Firestore" and "Emulatorss"
    - Select "Use an existing project"
    - Select "cs121-teamhub-test (cs121-teamhub-test)" *(Note: You will need access to this Firebase project for this step, so please contact us if you need help with this)*
    - Press Enter for the following two questions
    - Select "Firestore Emulator"
2. Then Run `make run` to start the Flask server.

# Test Execution
1. In a separate Terminal window, run `make fb-emulator` to start the firebase emulator.
2. Then in the calendar-service directory, run `make test` to run all the tests and view the test output.