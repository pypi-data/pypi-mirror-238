from itertools import chain
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

EXTRAS_REQUIRE = {
    "gcp": ["google-cloud-datastore", "google-cloud-pubsub"]
}
EXTRAS_REQUIRE['full'] = list(set(chain(*EXTRAS_REQUIRE.values())))

setup(
    name="google-ads-house-keeper",
    version="0.0.24",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Google Inc. (gTech gPS CSE team)",
    author_email="no-reply@google.com",
    license="Apache 2.0",
    python_requires=">3.9",
    packages=find_packages(),
    install_requires=[
        "google-ads-api-report-fetcher>=1.11.1", "SQLAlchemy==1.4.46", "beautifulsoup4",
        "google-api-python-client", "psycopg2-binary"
    ],
    extras_require=EXTRAS_REQUIRE,
    setup_requires=["pytest-runner"],
    tests_requires=["pytest"],
)

