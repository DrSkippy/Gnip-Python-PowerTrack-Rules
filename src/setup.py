from distutils.core import setup

setup(
    name='gnip-powertrack-rules',
    version='0.1.5',
    author='Scott Hendrickson',
    author_email='scott@drskippy.net',
    packages=['gnip_rules'],
    scripts=['update_rules.py', 'create_rules.py','delete_rules.py', 'list_rules.py'],
    url='http://pypi.python.org/pypi/twacs/',
    license='LICENSE.txt',
    description='Gnip PowerTrack rules libarary and command scripts.',
    long_description=open('README.txt').read(),
)
