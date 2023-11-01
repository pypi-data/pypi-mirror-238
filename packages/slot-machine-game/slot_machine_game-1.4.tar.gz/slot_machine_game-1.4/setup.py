from setuptools import setup

setup(
    name='slot_machine_game',
    version="1.4",
    py_modules=["slot_machine_game"],
    install_requires=[
        "numpy",
        ],
    entry_points={
        "console_scripts":[
            "slot-machine=slot_machine:main",
        ],
    },
    setup_requires=['wheel'],
)