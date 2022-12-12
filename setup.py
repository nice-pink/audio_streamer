with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='audio_streamer',
    version='0.0.1',
    author='Raffael @ Nice Pink',
    author_email='r@nice.pink',
    description='Audio streaming',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nice-pink/audio_streamer',
    project_urls = {
        "Bug Tracker": "https://github.com/nice-pink/audio_streamer/issues"
    },
    license='MIT',
    packages=['audio_streamer'],
    install_requires=[],
)