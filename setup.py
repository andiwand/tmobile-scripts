from setuptools import setup

setup(
	name="tmobile-scripts",
	version="0.0.1",
	url="https://github.com/andiwand/tmobile-scripts",
	license="GNU General Public License",
	author="Andreas Stefl",
	author_email="stefl.andreas@gmail.com",
	description="t-mobile austria quota scripts",
	long_description="",
	platforms="any",
	entry_points={"console_scripts":["check_pool = check_pool", "check_single = check_single"]},
)
