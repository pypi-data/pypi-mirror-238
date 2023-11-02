"""Setup logitfy
"""

import subprocess
import os
import re
import json
import setuptools

_VERSION_FILE_PATH = os.path.join('logitfy', 'VERSION')
_REQUIREMENTS_FILE_PATH = os.path.join('logitfy', 'REQUIREMENTS')

if not os.path.isfile(_VERSION_FILE_PATH):
    logitfy_version = (
        subprocess.run(
            ["git", "describe", "--tags"],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout
        .decode('utf-8')
        .strip()
    )

    print(logitfy_version)

    assert re.fullmatch(r"\d+\.\d+\.\d+", logitfy_version), \
        f"No valid version found: {logitfy_version}!"

    with open(_VERSION_FILE_PATH, 'w', encoding="utf-8") as f:
        f.write(logitfy_version)
else:
    with open(_VERSION_FILE_PATH, 'r', encoding="utf-8") as f:
        logitfy_version = f.read().strip()

if not os.path.isfile(_REQUIREMENTS_FILE_PATH):
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requires = f.read().split()

    with open(_REQUIREMENTS_FILE_PATH, 'w', encoding="utf-8") as f:
        json.dump(requires, f)
else:
    with open(_REQUIREMENTS_FILE_PATH, 'r', encoding="utf-8") as f:
        requires = json.load(f)

setuptools.setup(
    name="logitfy",
    version=logitfy_version,  # determined by release in github
    author="Matthias Rieck",
    author_email="Matthias.Rieck@tum.de",
    description="Create Logging Reports for git Repositories",
    long_description="Create Logging Reports for git Repositories",
    url="https://github.com/MatthiasRieck/changelog-service",
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"logitfy": [
        "VERSION",
        "REQUIREMENTS",
        "logitfy-app/dist/*",
    ]},
    include_package_data=True,
    install_requires=requires,  # determined by requirements.txt
)