from setuptools import setup
setup(
    name="mazegen",
    version="1.0.0",
    author="labdalla, naldibis",
    description="A lightweight procedural maze generator for 42 curriculum",
    packages=["maze_generation"],
    install_requires=[
        "requests>=2.25.1",
    ],
    python_requires=">=3.6",
)
