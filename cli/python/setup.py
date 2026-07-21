from setuptools import setup, find_packages

setup(
    name="agent-toolkit",
    version="0.1.0",
    packages=find_packages(),
    description="AI Agent开发、管理和监控工具集",
    author="Erich956389473",
    author_email="erichlee1327@gmail.com",
    url="https://github.com/Erich956389473/agent-toolkit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "agent-toolkit=agent_toolkit.main:main",
        ],
    },
)