from setuptools import find_packages, setup

long_description = """
Fast and effective Instagram Private API wrapper (public+private requests and challenge resolver).

Use the most recent version of the API from Instagram.

Features:

1. Performs Public API (web, anonymous) or Private API (mobile app, authorized)
   requests depending on the situation (to avoid Instagram limits)
2. Challenge Resolver have Email (as well as recipes for automating receive a code from email) and SMS handlers
3. Support upload a Photo, Video, IGTV, Clips (Reels), Albums and Stories
4. Support work with User, Media, Insights, Collections, Location (Place), Hashtag and Direct objects
5. Like, Follow, Edit account (Bio) and much more else
6. Insights by account, posts and stories
7. Build stories with custom background, font animation, swipe up link and mention users
8. In the next release, account registration and captcha passing will appear
"""

requirements = [
    "requests<3.0,>=2.25.1",
    # "PySocks==1.7.1",
    # "pydantic==1.10.9",
    # "pycryptodomex==3.18.0",
]
# requirements = [
#     line.strip()
#     for line in open('requirements.txt').readlines()
# ]

setup(
    name="mangoplateapi",
    version="1.0.15",
    author="8ㅁ8",
    # author_email="heeya8876@naver.com",
    license="MIT",
    #url="http://github.com/subzeroid/instagrapi",
    install_requires=requirements,
    keywords=[
        "mangoplate api",

    ],
    description="Fast and effective Mangoplate Private API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)