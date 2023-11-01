# Changelog

## Changes from [0.0.3][0.0.3] to [0.1.0][0.1.0]

- ➕ add support for async session makers

## Changes from [0.0.2][0.0.2] to [0.0.3][0.0.3]

- ➕ Session.commit() is now a true commit, FSM will create a transaction per test and
  rollback the transaction as teardown
- 📝 a CODE_OF_CONDUCT.md
- 📝 more info in CONTRIBUTING.md
- ⚙️ pytest fixtures for shorter tests
- ⚙️ more tests

## Changes from [0.0.1][0.0.1] to [0.0.2][0.0.2]

- 📝 this CHANGELOG.md
- 📝 more info in CONTRIBUTING.md and README.md
- ⚙️ better test code design and quality
- 📝 add a CODE_OF_CONDUCT.md
- 📝 add a MERGE_REQUEST_TEMPLATE.md
- ➕ Session.commit() isn't forbidden anymore, but behavior is changed to only perform a
  Session.flush()
- ⚙️ quality testing: tox won't try to test with py312 anymore until fake_session_maker
  is py312 compatible

[0.0.1]: https://lab.frogg.it/dorianturba/fake_session_maker/-/releases/0.0.1

[0.0.2]: https://lab.frogg.it/dorianturba/fake_session_maker/-/releases/0.0.2

[0.0.3]: https://lab.frogg.it/dorianturba/fake_session_maker/-/releases/0.0.3

[0.1.0]: https://lab.frogg.it/dorianturba/fake_session_maker/-/releases/0.1.0
