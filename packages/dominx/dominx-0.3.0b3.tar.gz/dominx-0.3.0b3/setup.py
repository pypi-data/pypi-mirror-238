import warnings

from setuptools import Extension, find_packages, setup

setupconfig = {
    "url": "https://dominx.readthedocs.io/en/latest",
    "download_url": "https://pypi.org/project/dominx",
    "project_urls": {
        "Documentation": "https://dominx.readthedocs.io/en/latest",
        "Source": "https://github.com/zenthm/dominx",
        "Tracker": "https://github.com/zenthm/dominx/issues",
    },
    "packages": find_packages(where="src"),
    "package_dir": {"": "src"},
    "ext_modules": [
        Extension(
            name="dominx.display",
            sources=[
                "src/dominx/display.c",
                "src/dominx/_internal.c",
            ],
            include_dirs=[
                "src",
            ],
        ),
        Extension(
            name="dominx.flow",
            sources=[
                "src/dominx/flow.c",
                "src/dominx/_internal.c",
            ],
            include_dirs=[
                "src",
            ],
        ),
        Extension(
            name="dominx.stream",
            sources=[
                "src/dominx/stream.c",
                "src/dominx/_internal.c",
            ],
            include_dirs=[
                "src",
            ],
        ),
    ],
}

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    setup(**setupconfig)
