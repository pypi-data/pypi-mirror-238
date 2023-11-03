from distutils.core import setup
import setuptools

packages = ['gxl_ai_utils', 'gxl_ai_utils.utils',
            'gxl_ai_utils.config', 'gxl_ai_utils.run',
            'gxl_ai_utils.thread','gxl_ai_utils.gxl_dataset']  # 唯一的包名，自己取名
setup(name='gxl_ai_utils',
      version='1.0.3',
      author='Xuelong Geng',
      description='这个工具包模块是耿雪龙的, 耿雪龙是小睿宝的',
      author_email='3349495429@qq.com',
      packages=packages,
      package_dir={'requests': 'requests'}, )
