from pyproj import Transformer
from . import namelist as nl
from math import ceil, floor
import argparse
import os


def mercator_in_wps(rlat, rlon, tlat, delta, e_we, e_sn):
    '''
    用于计算namelist.wps中的参数计算经纬度范围
    rlat: 中心纬度
    rlon: 中心纬度
    tlat: 真实经纬度true_lat
    delta: 网格间距dx,dy你设置成不一样的，也会是一样的
    e_we: 东西方向格点数
    e_sn: 南北方向格点数
    返回：north, west, south, east
    '''
    # 创建自定义麦卡托投影的定义字符串
    mercator_proj = f"+proj=merc +lon_0=100 +lat_ts={tlat} +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs"

    # 创建转换器实例
    tf1 = Transformer.from_crs("EPSG:4326", mercator_proj)
    tf2 = Transformer.from_crs(mercator_proj, "EPSG:4326")

    # 将经纬度坐标转换为自定义麦卡托投影坐标
    rx, ry = tf1.transform(rlat, rlon)

    north, west = tf2.transform(rx - delta*e_we / 2, ry + delta*e_sn / 2)
    south, east = tf2.transform(rx + delta*e_we / 2, ry - delta*e_sn / 2)

    return north, west, south, east


def main():
    parser = argparse.ArgumentParser(description='这是一个计算namelist.wps经纬度范围的程序')
    parser.add_argument('file', nargs='?', type=str, help='输入的namelist.wps文件')
    args = parser.parse_args()

    wps_file = args.file
    if wps_file is None:
        wps_file = os.path.join(os.getcwd(), 'namelist.wps')
        print(f"未设置文件路径，将尝试在当前路径下读取{wps_file}")
    try:
        config = nl.load(wps_file)
    except FileNotFoundError:
        print(f"文件{wps_file}不存在，请检查文件路径是否正确")
        exit(1)

    # 读取namelist.wps中的参数
    map_proj = config['geogrid']['map_proj']
    ref_lat = config['geogrid']['ref_lat']
    ref_lon = config['geogrid']['ref_lon']
    true_lat = config['geogrid']['truelat1']
    stand_lon = config['geogrid']['stand_lon']
    delta = config['geogrid']['dx']
    e_we = config['geogrid']['e_we']
    e_sn = config['geogrid']['e_sn']
    # 诊断信息
    if map_proj == 'mercator':
        print("error 本命令支持麦克托投影方式")
    # 计算经纬度范围
    north, west, south, east = mercator_in_wps(ref_lat, ref_lon, true_lat, delta, e_we, e_sn)
    # 诊断信息
    oppsite_lon = (stand_lon + 180) - 360 * (stand_lon + 180 > 180)
    if oppsite_lon < east and oppsite_lon > west:
        print("stand_lon应该有问题，应该设置比较接近中心经度的值，你可以使用plotgrids.ncl来确认经纬度范围")
    # 向外取整
    north = ceil(north)
    west = floor(west)
    south = floor(south)
    east = ceil(east)
    print(f"向外取整后： 北{north},  西{west},  南{south},  东{east}")


if __name__ == "__main__":
    main()
