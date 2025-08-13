VENV_DIR      := .venv
PYTHON        := $(VENV_DIR)/bin/python
PIP           := $(VENV_DIR)/bin/pip
SRC_DIR       := src
MAIN_SCRIPT   := $(SRC_DIR)/app.py
DIST_DIR      := dist
APP_NAME      := rubiktool

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV_DIR)/Scripts/python.exe
	PIP := $(VENV_DIR)/Scripts/pip.exe
endif

.PHONY: help venv install run clean distclean package

help:
	@echo "Available targets:"
	@echo " make venv             - Create Virtual Environment"
	@echo " make install          - Install the app + dependencies"
	@echo " make run              - Install the app and run it"
	@echo " make package          - Build an installer"
	@echo " make clean            - Remove build artifacts"
	@echo " make distclean        - Remove venv along with all artifacts"

venv: $(VENV_DIR)/touchfile

$(VENV_DIR)/touchfile:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@touch $@

install: venv requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) $(MAIN_SCRIPT)

package: install
	$(PIP) install pyinstaller
	$(PYTHON) -m PyInstaller --onefile --name $(APP_NAME) $(MAIN_SCRIPT)

clean:
	rm -rf __pycache__ build *.spec
	rm -rf $(DIST_DIR)/*

distclean: clean
	rm -rf $(VENV_DIR)
