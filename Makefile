# Authors:      Qullègues of Grigori
# Description:  Makefile to create the "grigorify" package

# Define constant values
PYTHON = python3

SOURCEDIR = src
BUILDDIR = build

PYPROJECT = pyproject.toml
BUILD_PYPROJECT = $(patsubst %.toml, $(BUILDDIR)/%.toml, $(PYPROJECT))

README = README.md
BUILD_README = $(patsubst %.md, $(BUILDDIR)/%.md, $(README))

SRC_PYTHON_FILES = $(wildcard $(SOURCEDIR)/*.py)
BUILD_PYTHON_FILES = $(patsubst $(SOURCEDIR)/%.py, $(BUILDDIR)/%.py, $(SRC_PYTHON_FILES))

# Build rules
all: $(BUILD_PYTHON_FILES) $(BUILD_PYPROJECT) $(BUILD_README)
	@cd $(BUILDDIR) && python3 -m build

clean:
	@rm -rf $(BUILDDIR)

build/%.py: src/%.py
	@echo "Creating $@ file"
	@mkdir -p $(BUILDDIR)
	@cp $< $@

build/%.toml: %.toml
	@echo "Creating $@ file"
	@mkdir -p $(BUILDDIR)
	@cp $< $@

build/%.md: %.md
	@echo "Creating $@ file"
	@mkdir -p $(BUILDDIR)
	@cp $< $@
