# Build Procedure
In the calendar-service directory
1. Run `make deps` to start the virtual environment and install all the required dependencies.
2. Run `make fb-init` initialize the Firebase project directory, you will likely be prompted to type your computer password, then follow the on-screen instructions to select the following options:
    - Select "Firestore" and "Emulatorss"
    - Select "Use an existing project"
    - Select "cs121-teamhub-test (cs121-teamhub-test)" *(Note: You will need access to this Firebase project for this step, so please contact us if you need help with this)*
    - Press Enter for the following two questions
    - Select "Firestore Emulator"
2. Then run `make run` to start the Flask server.

# Test Execution
In the calendar-service directory, run `make fb-emulator & (sleep 5; make test)` to start the Firebase emulator, and then run all the tests. Make sure to kill the emulator process in the background after the tests are complete.

Alternatively,
1. In a separate Terminal window, run `make fb-emulator` to start the Firebase emulator.
2. Then in the calendar-service directory, run `make test` to run all the tests.