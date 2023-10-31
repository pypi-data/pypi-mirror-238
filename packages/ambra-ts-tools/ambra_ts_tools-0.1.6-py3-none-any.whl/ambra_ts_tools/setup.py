from distutils.core import setup

setup(
    name='ambra_ts_tools',
    version='"0.1.6"',
    author='Ethan York',
    description='Internal TS tools for Ambra Health utilizing public API',
    url='https://github.com/EthanYork/public-ambra-ts-scripts',
    packages=["ambra_ts_tools","ambra_ts_tools.Ambra_Clone","ambra_ts_tools.Ambra_Clone.V2"]
)