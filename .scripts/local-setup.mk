setup-local: .venv/.finished_venv_install local.env

local.env:
	cp local.env.example local.env
	echo "Copied example env file to local.env, please adapt"

# Adapted from https://github.com/mara/mara-app/blob/master/.scripts/install.mk
.venv/.finished_venv_install:
	mkdir -p .venv
	(cd .venv && python3 -m venv .)
	.venv/bin/python3 -m pip install --upgrade pip pipdeptree
	.venv/bin/python3 -m pip install --requirement=requirements.txt.freeze
	touch $@


update-packages: .venv/.finished_venv_install
	.venv/bin/python3 -m pip install --requirement=requirements.txt --upgrade
	.venv/bin/pipdeptree --warn=fail
	.venv/bin/python3 -m pip freeze | grep -v "pkg-resources" > requirements.txt.freeze
	echo "Updated all packages, please run tests to ensure not breakage!"
