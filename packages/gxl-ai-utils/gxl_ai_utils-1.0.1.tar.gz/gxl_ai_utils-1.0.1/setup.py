from distutils.core import setup
import setuptools

packages = ['gxl_ai_utils', 'gxl_ai_utils.utils', 'gxl_ai_utils.audio_dataset', 'gxl_ai_utils.audio_handler',
            'gxl_ai_utils.audio_model', 'gxl_ai_utils.config', 'gxl_ai_utils.gxl_model_warehouse', 'gxl_ai_utils.run',
            'gxl_ai_utils.store_data', 'gxl_ai_utils.store_model', 'gxl_ai_utils.thread']  # 唯一的包名，自己取名
setup(name='gxl_ai_utils',
      version='1.0.1',
      author='Xuelong Geng',
      packages=packages,
      package_dir={'requests': 'requests'}, )
