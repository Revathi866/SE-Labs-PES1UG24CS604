# Static Code Analysis Issues

| Issue | Tool | Description | Fix |
|---|---|---|---|
| Hardcoded password | Bandit | Password stored in source code | Read password from environment variable |
| Unsafe eval() | Bandit | Arbitrary expressions could be executed | Added restricted arithmetic evaluation |
| Weak MD5 hash | Bandit | MD5 flagged as weak for security | Marked hash as non-security fingerprint |
| Mutable default argument | Pylint | Shared list between function calls | Changed default to None |
| Bare exception | Pylint/Flake8 | Errors were silently ignored | Removed broad exception handling |
| Naming and formatting | Pylint/Flake8 | Inconsistent names and whitespace | Improved naming and formatting |
