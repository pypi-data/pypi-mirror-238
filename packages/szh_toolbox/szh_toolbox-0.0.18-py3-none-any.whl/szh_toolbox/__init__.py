import numpy as np
from pyproj import CRS, Transformer
import re
import h5py
from anytree import Node, RenderTree
import os
from colorama import Fore, Style


def get_zenith_angle(sat_lon, sat_lat, sat_alt, obs_lon, obs_lat, obs_alt=None):
    """
    计算卫星与地面观测点之间的天顶角（本地入射角）
    :参数 sat_lon: 卫星经度（单位：度）
    :参数 sat_lat: 卫星纬度（单位：度）
    :参数 sat_alt: 卫星高度（单位：千米）
    :参数 obs_lon: 观测点经度（单位：度）
    :参数 obs_lat: 观测点纬度（单位：度）
    :参数 obs_alt: 观测点高度（单位：米），可选，默认为0
    :return: 卫星与地面观测点之间的天顶角（单位：度）
    """

    # 预处理
    obs_shape = obs_lat.shape
    obs_lat = obs_lat.flatten()
    obs_lon = obs_lon.flatten()
    obs_alt = obs_alt.flatten() if obs_alt is not None else np.zeros_like(obs_lat)
    sat_alt = sat_alt * 1000  # 卫星高度:km转换为米

    # 创建坐标转换器（从WGS84经纬度坐标转换到地心惯性坐标系）
    crs_lla = CRS("EPSG:4326")  # WGS84经纬度坐标系统
    crs_ecef = CRS("EPSG:4978")  # 地心惯性坐标系
    transformer = Transformer.from_crs(crs_lla, crs_ecef, always_xy=True)

    # 将卫星位置、地面观测点位置从WGS84经纬度和高度转换为地心惯性坐标系下的坐标
    sat_ecef = transformer.transform(sat_lon, sat_lat, sat_alt)
    obs_ecef = transformer.transform(obs_lon, obs_lat, obs_alt)

    # 计算卫星与地面观测点之间的向量
    obs_vec = np.array(obs_ecef)
    obs_sat_vec = np.array(sat_ecef)[:, np.newaxis] - obs_vec
    obs_sat_dist = np.linalg.norm(obs_sat_vec, axis=0)
    obs_dist = np.linalg.norm(obs_vec, axis=0)

    # 计算卫星与地面观测点之间的夹角（单位：度）
    theta = np.rad2deg(
        np.arccos(np.sum(obs_vec*obs_sat_vec, axis=0) / obs_sat_dist / obs_dist))

    return theta.reshape(obs_shape)


class ShellScriptVariable:
    '''
    这个类用于读取和修改shell脚本中的变量值。可以通过实例化对象或使用类方法来完成操作。
    '''
    def __init__(self, script_path, **kwargs):
        '''
        初始化方法，为对象赋予脚本路径，并读取脚本内容。
        :param script_path: shell脚本的路径
        :param **kwargs: 传递给打开文件的其他参数
        '''
        self.script_path = script_path
        with open(script_path, 'r', **kwargs) as f:
            self.content = f.read()

    def get(self, variable_name):
        '''
        获取脚本中指定变量的值。
        :param variable_name: 需要获取的变量名
        :return: 返回变量值
        :raises ValueError: 如果变量不存在，抛出ValueError异常
        '''
        pattern = rf"({variable_name}\s*=\s*)([^\s\n][^\n]*)"
        match = re.search(pattern, self.content)
        if match:
            return match.group(2)
        else:
            raise ValueError(f"变量 {variable_name} 不存在")

    def update(self, variable_name, new_value, count=1):
        '''
        更新脚本中指定变量的值。
        :param variable_name: 需要更新的变量名
        :param new_value: 变量更新后的值
        :param count: 需要更新的匹配项数量，默认为1，设置为0时将更新所有匹配项
        '''
        pattern = rf"({variable_name}\s*=\s*)([^\s\n][^\n]*)"
        # 确认是否存在变量，不存在会抛出异常
        self.get(variable_name)
        new_str = f"{variable_name}={new_value}"
        self.content = re.sub(pattern, new_str, self.content, count=count)

    def save(self, save_path=None):
        '''
        将修改后的脚本内容保存到文件。
        :param save_path: 保存的路径，默认为None，将覆盖原始脚本文件
        '''

        if not save_path:
            save_path = self.script_path
        with open(save_path, 'w') as f:
            f.write(self.content)

    def show(self):
        '''
        显示脚本的内容。
        '''
        print(f'-------{self.script_path}----------')
        print(self.content)
        print('------------------------------------')

    @classmethod
    def modify(cls, script_path, variable_name, new_value, save_path=None, count=1, **kwargs):
        '''
        类方法，修改脚本的变量值并保存。
        :param script_path: shell脚本的路径
        :param variable_name: 需要更新的变量名
        :param new_value: 变量更新后的值
        :param save_path: 保存的路径，默认为None，将覆盖原始脚本文件
        :param count: 需要更新的匹配项数量，默认为1，设置为0时将更新所有匹配项
        :param **kwargs: 传递给打开文件的其他参数
        '''
        ssv = cls(script_path, **kwargs)
        ssv.update(variable_name, new_value, count=count)
        ssv.save(save_path)





def build_tree(obj, name='', parent=None, matlab=False):
    if isinstance(obj, h5py.Group):
        if name=="":
            node = parent
        else:
            node = Node(name, parent=parent)
        for key, value in obj.items():
            build_tree(value, key, parent=node, matlab=matlab)
    elif isinstance(obj, h5py.Dataset):
        dims = obj.shape
        if matlab==True:
            dims = dims[::-1]
        name = f"{name:<30} 维度：{dims}"
        Node(name, parent=parent)

def read_hdf5_recursively(filename, matlab=False):
    with h5py.File(filename, 'r') as f:
        root = Node(os.path.abspath(filename))
        build_tree(f, parent=root, matlab=matlab)
        for pre, _, node in RenderTree(root):
            print("%s%s" % (pre, node.name))

# 使用示例
def get_hdf5_tree(h5file, matlab=False):
    if matlab:
        print(Fore.YELLOW + "警告哦: python读取和矩阵维度和matlab读取的矩阵维度是转置关系" + Style.RESET_ALL)
    read_hdf5_recursively(h5file, matlab)
