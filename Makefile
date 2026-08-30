# BSP Skills Pack — Makefile
# SPDX-License-Identifier: Apache-2.0

.PHONY: help install validate test-release

help:
	@echo "make install     — install skills to agent runtimes (wraps ./install.sh)"
	@echo "make validate    — run skill structure validation (advisory mode)"

install:
	./install.sh

validate:
	python3 tools/validate.py --mode advisory

test-release:
	python3 -B -m unittest tools.test_release_contract -v
