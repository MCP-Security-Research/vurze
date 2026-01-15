# Development TODOs

- make vurze extension more dynamic. what if you dont have it installed and just try extension. try to make cli + extensioni combo as flexible as possible
- change decorate to vurze lock command
- add .env to gitignore automatically???, check if a gitignore exists
- you can use maturin's sphinx generation for documentation? and a cool website
- update to use ____ to lint rust code and ruff to lint python code
- create a standalone install script other than using pip/uv

testing:
- ensure tool works with recursive functions and classes. basic test cases using pytest, and also cargo test???
- create test cases that ensure that code runs the same after the decorators have been added
- what happens if someone deletes a decorator to a function
- can my tool be attacked by adding soooooo many decorators? like should i create a limit?
- can my tool be used against itself to attack itself
- does my tool remove decorators that are automatically created? like does it clean up after itself properly?
- add tests for multi file

compatibility:
- update to use ruff to lint python code and make the tool conform to ruff linting standards
- update to use ____ to lint rust code
- add boxes to the readme file. for compatable python versions, for tool version, and more

alt:
- kapfhammer mentioned fort knox for storing secrets? look into mise developer that made it
- dotenv github actions problem luman

---

development commands:

```text
COMMANDS I FOLLOWED TO SETUP MATURIN:
uv venv
source .venv/bin/activate
uv tool install maturin
maturin init
select pyo3

COMMANDS I FOLLOWED TO TEST MATURIN INITIALLY:
maturin develop
python -c "import vurze; print('Vurze imported successfully!')"

COMMANDS FOR TESTING CLI
source .venv/bin/activate
conda deactivate
maturin develop --release
vurze --help
```

release commands:

update the version in the init.py file, pyproject.toml, and Cargo.toml files
maturin build --release
git tag v0.1.0
git push origin main --tags
