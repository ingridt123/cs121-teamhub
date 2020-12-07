## Users Service

### Setup

Run `make deps` to install dependencies in a virtualenv.

The users service expects an untracked file `config.py` with the following
variables defined, like in this example:

```py
API_KEY = "foo"
FIREBASE_AUTH_URL = "http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts"
FIRESTORE_URL = "http://localhost:8080/v1/projects/cs121-teamhub-test/databases/(default)/documents"
SCHOOL_ID = "my-school"
```

### Testing

The emulator is set up by the Firebase CLI. Log in with Google credentials and
connect to the `cs121-teamhub-test`, then enable the emulator with the
authentication and Firestore services. The emulator is then started in the
background with `firebase emulators:start`.

Then run `make test` to populate the emulator and run all tests.
