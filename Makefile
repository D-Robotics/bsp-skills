# BSP Skills Pack — Makefile
# SPDX-License-Identifier: Apache-2.0

.PHONY: help install validate

help:
	@echo "make install     — install skills to agent runtimes (wraps ./install.sh)"
	@echo "make validate    — run skill structure validation (advisory mode)"

install:
	./install.sh

validate:
	python3 tools/validate.py --mode advisory
