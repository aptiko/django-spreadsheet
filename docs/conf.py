from setuptools_scm import get_version

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "django-spreadsheet"
copyright = "2024, IRMASYS"
author = "Antonis Christofides"
version = get_version(root="..")
release = version
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
html_theme = "alabaster"
html_static_path = ["_static"]
htmlhelp_basename = "django_spreadsheetdoc"
latex_elements = {}
latex_documents = [
    (
        master_doc,
        "django_spreadsheet.tex",
        "django-spreadsheet Documentation",
        "Antonis Christofides",
        "manual",
    ),
]
texinfo_documents = [
    (
        master_doc,
        "django_spreadsheet",
        "django-spreadsheet Documentation",
        author,
        "django_spreadsheet",
        "One line description of project.",
        "Miscellaneous",
    ),
]
