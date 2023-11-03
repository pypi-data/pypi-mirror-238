import yaml

from . import assist_utils


class GxlNode(dict):
    frozen = False

    def __init__(self, input_dict):
        super(GxlNode, self).__init__(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, dict):
                self[key] = GxlNode(value)
            else:
                self[key] = value

    def __getattr__(self, name):
        """
        当你访问一个对象的属性，而该属性不存在时，Python 会自动调用 __getattr__ 方法
        ，以便你有机会定义一个默认的行为或返回一个替代值
        """
        if name in self:
            value = self[name]
            if isinstance(value, dict):
                return GxlNode(value)
            else:
                return value
        else:
            return None

    @property
    def is_frozen(self):
        return self.frozen

    def make_frozen(self):
        self.frozen = True

    def break_frozen(self):
        self.frozen = False

    def __setattr__(self, name, value):
        if self.is_frozen:
            raise AttributeError(
                "Attempted to set {} to {}, but GxlNode is immutable".format(
                    name, value
                )
            )
        else:
            if isinstance(value, dict):
                self[name] = GxlNode(value)
            else:
                self[name] = value

    def __str__(self):
        """
        当你使用 str(obj) 函数或内置的 print(obj) 函数时，如果对象定义了 __str__ 方法，
        Python 将调用该方法来获取对象的字符串表示形式。
        yaml格式
        """
        r = ""
        s = []
        for k, v in sorted(self.items()):
            seperator = "\n" if isinstance(v, GxlNode) else " "
            attr_str = "{}:{}{}".format(str(k), seperator, str(v))
            attr_str = assist_utils.indent(attr_str, 2)
            s.append(attr_str)
        r += "\n".join(s)
        return r

    def __repr__(self):
        """
        当你使用 repr(obj) 函数时，如果对象定义了 __repr__ 方法, Python 将调用该方法
        """
        return "{}({})".format(self.__class__.__name__, super(GxlNode, self).__repr__())

    @classmethod
    def get_config_from_yaml(cls, file_path: str):
        with open(file_path, 'rt', encoding='utf-8') as f:
            dict_1 = yaml.safe_load(f)
        return cls(dict_1)


if __name__ == '__main__':
    gxl = GxlNode.get_config_from_yaml('./config.yaml')
    print(gxl.dataset)
