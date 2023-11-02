from setuptools import setup, find_packages


setup(
    name="replicate_whisper_diarization",
    packages=find_packages(),
    version="0.1.0",
    description="A short description of the project.",
    author="team-collectiveai",
    author_email="team.collective.ai@gmail.com",
    url="https://github.com/collectiveai-team/whisper-diarization",
    install_requires=[
        "replicate==0.15.5",
        "rich==13.6.0",
        # "soundfile==0.12.1",
        # "librosa==0.10.1",
        # "deepmultilingualpunctuation==1.0.1",
    ],
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
