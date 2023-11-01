import os

pkg_name = "Pytmosph3R"

pkg_dir = os.path.dirname(os.path.abspath(__file__))
"""Directory containing sources of Pytmosph3R module"""

root_dir = os.path.join(pkg_dir, "..", "..")
"""Root directory of Pytmosph3R repository"""

relative_dir = root_dir
"""Directory relative to root directory, for simpler paths in configuration file"""
