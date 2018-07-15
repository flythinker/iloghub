
from distutils.core import setup

setup(
      name = "iloghub.itail",
      version = "0.0.2",
      keywords = ("iloghub",'log','java', "flythinker"),
      #description = "发送电子邮件，接收电子邮件等",
      author='flythinker',
      author_email='67495224@qq.com',  # 作者邮箱
      url='https://github.com/flythinker/iloghub',
      long_description = "a instance log tail tool for iloghub",
      platforms = "any",
      license = "MIT Licence",
      packages = ['iloghub_tail']
#     install_requires = [],
#     scripts = [],
#     entry_points = {
#         'console_scripts': [
#             'test = test.help:main'
#         ]
#     }
)
