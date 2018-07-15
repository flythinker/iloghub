
#from distutils.core import setup
from setuptools import setup
from setuptools.command.install_scripts import install_scripts

# class InstallScripts(install_scripts):
#     def run(self):
#         setuptools.command.install_scripts.install_scripts.run(self)
#         # Rename some script files
#         for script in self.get_outputs():
#             if basename.endswith(".py") or basename.endswith(".sh"):
#                 dest = script[:-3]
#             else:
#                 continue
#             print("moving %s to %s" % (script, dest))
#             shutil.move(script, dest)

setup(
      name = "iloghub.itail",
      version = "0.0.5",
      keywords = ["iloghub",'itail','log','java', "flythinker"],
      #description = "发送电子邮件，接收电子邮件等",
      author='flythinker',
      author_email='67495224@qq.com',  # 作者邮箱
      url='https://github.com/flythinker/iloghub',
      long_description = "a instance log tail tool for iloghub",
      platforms = "any",
      license = "MIT Licence",
      packages = ['iloghub_tail'],
      install_requires=[
          'PyYAML>=3.13',
          'redis>=2.10.6'
      ],
      scripts=['itail.py'],
      # cmdclass={
      #       "install_scripts": InstallScripts
      # }
#     entry_points = {
#         'console_scripts': [
#             'test = test.help:main'
#         ]
#     }
)
