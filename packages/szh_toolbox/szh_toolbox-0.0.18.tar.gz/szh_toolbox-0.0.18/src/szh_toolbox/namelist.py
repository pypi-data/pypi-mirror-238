''' 用于读取修改WRF的namelist文件
    这里面的英文注释都是使用github copilot自动生成的，所以不是中文
    使用方法：
    import Namelist as nl

    config = nl.load("data/namelist.input")
    print(nl.dump(config))
'''
import re
from collections import OrderedDict


def load(filename):
    """从文件中加载namelist，返回一个字典，是每个值是Python对象"""
    with open(filename, 'r') as f:
        data = OrderedDict()
        flag_section = False  # 表示是否进入了某个section
        section = None  # 当前的section
        for i, line in enumerate(f, 1):
            line = line.replace(" ", "")  # 去掉空格
            line = re.sub('!.*', '', line)  # 去掉注释
            if not flag_section:
                m = re.search(r'^&(\w+)', line)
                if m:
                    section = m.group(1)
                    data[section] = OrderedDict()
                    flag_section = True
            else:
                # 上个section结束之前，不应该再出现下一个sectiond的开头
                if re.search(r'^&(\w+)', line):
                    raise ValueError(f"没检测到&{section}的结束标志'/'")
                # 匹配section的结尾
                elif re.search(r'\/', line):
                    flag_section = False
                # 匹配每个section之内的key=value
                else:
                    m = re.search(r'^(\w*)\s*=(.*?),?$', line)
                    if m:
                        if m.group(1) == '' or m.group(2) == '':
                            raise ValueError(f"第{i}行：{m.group(1)}={m.group(2)}不合法")
                        else:
                            data[section][m.group(1)] = decode(m.group(2))
    return data


def dump(data, output_file=None):
    """将一个python字典转换为namelist文件格式的字符串
       并且可以选择将其写入文件中
    """
    s = ""
    for section in data.keys():
        s += " &%s\n" % section
        for k, v in data[section].items():
            try:
                v = encode(v)
            except ValueError:
                raise ValueError(f"{k}的值不合法")
            s += " {:<30} = {:<},\n".format(k, v)
        s += " /\n\n"
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(s)
    else:
        return s


def decode(string):
    """将一个字符串转换为Python对象。

    该函数将一个字符串转换为Python对象。它支持以下类型：

    * .true. -> True
    * .false. -> False
    * 整数值 -> int
    * 浮点数值 -> float
    * 其他任何值 -> str

    Args:
        string (str): 输入字符串。

    Returns:
        转换后的值。

    Raises:
        ValueError: 如果输入字符串为空。
    """
    # 如果输入字符串为空，则抛出异常。
    if string == '':
        raise ValueError("value是空值")

    # 将输入字符串按逗号分隔成单独的值。
    values = string.split(",")

    # 将每个值转换为其适当的类型。
    new_values = []
    for value in values:
        if value == '.true.':
            new_values.append(True)
        elif value == '.false.':
            new_values.append(False)
        else:
            try:
                new_values.append(int(value))
            except ValueError:
                try:
                    new_values.append(float(value))
                except ValueError:
                    new_values.append(value)

    # 返回转换后的值的列表。
    if len(new_values) == 1:
        return new_values[0]
    else:
        return new_values


def encode(objs):
    """将Python对象转换为Fortran namelist值"""
    s = []  # 用于存储结果的列表
    if not isinstance(objs, list):  # 如果输入不是列表，则将其转换为列表
        objs = [objs]
    for obj in objs:  # 遍历列表
        if isinstance(obj, bool):  # 如果是布尔值，将其转换为Fortran布尔值
            if obj:
                s.append(".true.")
            else:
                s.append(".false.")
        elif isinstance(obj, (int, float)):  # 如果是整数或浮点数，将其转换为字符串
            s.append(str(obj))
        elif isinstance(obj, str):  # 如果是字符串，则直接添加
            s.append(obj)
        else:  # 如果是不支持的类型，则抛出异常
            raise ValueError("输入的值不合法")
    return ",".join(s)  # 将列表转换为字符串并返回


def modify(nl_file, varname, new_value, save_path=None):
    """直接修改namelist文件中的某个变量的值
    nl_file: namelist文件的路径
    varname: 变量名
    new_value: 新值
    save_path: 保存路径，如果为None，则覆盖原文件
    """
    with open(nl_file, 'r') as f:
        content = f.read()

    # 提取注释和非注释
    try:
        m = re.search(rf'^( *{varname}[^\n!]*)( *!?.*?)$', content, re.MULTILINE)
        desc, comment = m.group(1), m.group(2)
    except AttributeError:
        raise ValueError(f"没找到变量{varname}")
    # 用正则表达式匹配变量的值
    try:
        m = re.search(rf'^( *{varname}\s*=\s*)([^\n!]*?)(,? *)$', desc, re.MULTILINE)
        new = f'{m.group(1)}{new_value}{m.group(3)}{comment}'
    except AttributeError:
        raise ValueError(f"没找到变量{varname}的值")
    # 替换文本内容
    content = re.sub(rf"^ *{varname}[^\n]+$", new, content, flags=re.MULTILINE)
    # 保存文件
    if not save_path:
        save_path = nl_file
    with open(save_path, 'w') as f:
        f.write(content)
