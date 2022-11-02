import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "XRPL dEX Python SDK"
copyright = "2022, Ripple Labs, Inc."
author = "AktaryTech <info@aktarytech.com>"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# OS path commands should be uncommented in conf.py file
# so that html utility could access the right project files to
# generate documentation.
sys.path.insert(0, os.path.abspath(".."))

extensions = ["sphinxcontrib.napoleon", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "bizstyle"
html_static_path = ["_static"]
