# Static Analysis Issues – parking_lot_system.py

Line numbers refer to the original (before-fix) file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605) | Security – High | 64 | `os.system("echo ... " + filename)` runs a shell command built from user input, so a crafted filename can run arbitrary commands. | Removed `os.system` and used `print()` to show the message. |
| Weak MD5 hash (B324) | Security – High | 53 | `hashlib.md5` is cryptographically broken and can be attacked with collisions. | Replaced with `hashlib.sha256`. |
| Use of `eval` (B307 / W0123) | Security – Medium | 48 | `eval(surge_expr)` runs any string as Python code, which allows code injection. | Removed `eval`; the function now takes a numeric `surge_multiplier` and computes `base_rate * surge_multiplier`. |
| Hardcoded secret | Security – Medium | 76, 85 | The barrier key is hardcoded in the source and printed to the console. | Read the key from the `GATE_BARRIER_KEY` environment variable and print only whether it is set. |
| Mutable default argument (W0102) | Bug – Medium | 15 | `entry_logs=[]` is shared between calls, so logs pile up from earlier calls. | Default set to `None`, with a new list created inside the function. |
| Bare `except: pass` (W0702 / E722 / B110) | Bug – Medium | 32-33 | Every error, including real bugs, is silently swallowed. | Catch only `KeyError`, report the missing slot and return `False`. |
| Use of `global` (W0603) | Code Quality – Medium | 12, 16 | A global variable is changed from inside a function, so state is hard to track. | Replaced with a module-level `parking_stats` dict that is updated without `global`. |
| File opened without `with` / encoding (R1732 / W1514) | Bug – Medium | 61-63 | The file may stay open if an error occurs, and the encoding depends on the platform. | Used `with open(filename, "w", encoding="utf-8")`. |
| Insecure random generator (B311) | Security – Low | 57 | `random.randint` is predictable and should not be used for ticket PINs. | Used `secrets.randbelow(9000) + 1000`. |
| Unused import / variables (W0611 / W0612 / F401 / F841) | Code Quality – Low | 4, 37, 47, 69 | `math`, `overtime_fee`, `base_rate` and the loop variable `s` are never used. | Removed `math`, `overtime_fee` and `s`; `base_rate` is now used in the fee calculation. |
| Comparison to None (C0121 / E711) | Style – Low | 38 | Used `== None` instead of `is None`. | Changed to `is None`. |
| Simplifiable if / else after return (R1703 / R1705) | Code Quality – Low | 40-43 | An `if/else` that returns `True`/`False` is redundant. | Replaced with `return not ...["is_occupied"]`. |
| Redefined outer name (W0621) | Code Quality – Low | 67 | The parameter `parking_slots` hides the global of the same name. | Renamed the parameter to `slots`. |
| Non snake_case names (C0103) | Style – Low | 12, 15, 27, 36, 46, 52, 56, 60, 67 | camelCase function names and a lowercase constant break PEP 8. | Renamed functions to snake_case (e.g. `park_vehicle`) and removed the global. |
| Missing docstrings (C0114 / C0116) | Style – Low | 1, 15-75 | No module docstring or function docstrings. | Added a docstring to the module and to every function. |
| Line too long / old-style formatting (C0301 / E501 / C0209) | Style – Low | 7-9, 23 | Lines exceed the length limit, and `%` formatting is used. | Split lines and used an f-string. |
| Missing final newline (C0304 / W292) | Style – Low | 88 | The file does not end with a newline. | Added a trailing newline and an `if __name__ == "__main__":` guard. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.10 / 10 | 10.00 / 10 |
| Flake8 | 10 issues | 0 issues |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | 0 issues |
