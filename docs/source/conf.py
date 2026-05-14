# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Verilog Design Guide'
copyright = '2024, Verilog Documentation Contributors'
author = 'Verilog Documentation Contributors'

release = '1.0'
version = '1.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_sitemap',
    'sphinx_copybutton',
    'sphinx_design',
    'sphinxext.opengraph',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_baseurl = 'https://verilogguide.readthedocs.io/latest/en'
sitemap_url_scheme = "{link}"

html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Options for EPUB output
epub_show_urls = 'footnote'
