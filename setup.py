from setuptools import setup, find_packages

setup(
    name="hornet",
    version="0.1.0",
    packages=find_packages(where="src"),   # src 폴더 안에서 패키지 찾기
    package_dir={"": "src"},               # src 폴더를 패키지의 루트로 설정
    install_requires=[
        "cryptography>=44.0.0",
        "rich>=13.9.4",
        "psutil>=6.1.0",
        "requests>=2.32.3"
    ],
    entry_points={
        "console_scripts": [
            "hornet-decrypt=hornet.decrypt:decrypt_directory_walk",
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Blueteam Ransomware Simulation Package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)
