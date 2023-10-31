import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
import os
import argparse
from .namelist_wps import mercator_in_wps as miw
from . import namelist as nl


class MyFrame(wx.Frame):
    def __init__(self, parent, title, wps_file):
        super(MyFrame, self).__init__(parent, title=title, size=(1200, 800))
        self.wps_file = wps_file

        # 创建一个Figure对象
        self.figure = Figure(figsize=(2, 2), dpi=100)
        self.canvas = FigureCanvas(self, -1, self.figure)

        # 创建输入框
        self.e_we_box = wx.TextCtrl(self, value="150", size=(100, 30))
        self.e_sn_box = wx.TextCtrl(self, value="150", size=(100, 30))
        self.ref_lat_box = wx.TextCtrl(self, value="23", size=(100, 30))
        self.ref_lon_box = wx.TextCtrl(self, value="112", size=(100, 30))
        self.true_lat_box = wx.TextCtrl(self, value="35", size=(100, 30))
        self.stand_lon_box = wx.TextCtrl(self, value="110", size=(100, 30))
        self.dx_box = wx.TextCtrl(self, value="20000", size=(100, 30))

        # 创建标签
        self.e_we_label = wx.StaticText(self, label="e_we:")
        self.e_sn_label = wx.StaticText(self, label="e_sn:")
        self.ref_lat_label = wx.StaticText(self, label="ref_lat:")
        self.ref_lon_label = wx.StaticText(self, label="ref_lon:")
        self.true_lat_label = wx.StaticText(self, label="true_lat:")
        self.stand_lon_label = wx.StaticText(self, label="stand_lon:")
        self.dx_label = wx.StaticText(self, label="dx:")

        # 创建按钮
        self.update_button = wx.Button(
            self, label="Update Map", size=(150, 30))
        self.update_button.Bind(wx.EVT_BUTTON, self.on_update_button_click)

        # 用网格布局
        grid_sizer = wx.GridBagSizer(vgap=10, hgap=10)
        grid_sizer.Add(self.e_we_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.e_we_box, pos=(0, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.e_sn_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.e_sn_box, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.ref_lat_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.ref_lat_box, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.ref_lon_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.ref_lon_box, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.dx_label, pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.dx_box, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.true_lat_label, pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.true_lat_box, pos=(5, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.stand_lon_label, pos=(6, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.stand_lon_box, pos=(6, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        grid_sizer.Add(self.update_button, pos=(7, 0), span=(1, 2), flag=wx.ALIGN_CENTER|wx.ALL, border=5)
    
        # 创建提示信息
        info = '''投影方式只支持Mercator；\nstand_lon最好和ref_lon比较接近；\n在Mercator投影中，dy无论\n设置多少，都是等于dx的'''
        rich_text = wx.StaticText(self, label=info, style=wx.ALIGN_LEFT|wx.LEFT)

        # 创建显示边界的输入框
        north_label = wx.StaticText(self, label='北')
        south_label = wx.StaticText(self, label='南')
        west_label = wx.StaticText(self, label='西')
        east_label = wx.StaticText(self, label='东')
        bound_info_label = wx.StaticText(self, label='计算得到的边界（不能修改）')
        self.north_box = wx.TextCtrl(self, value="40", size=(100, 30), style=wx.TE_READONLY)
        self.south_box = wx.TextCtrl(self, value="20", size=(100, 30), style=wx.TE_READONLY)
        self.west_box = wx.TextCtrl(self, value="100", size=(100, 30), style=wx.TE_READONLY)
        self.east_box = wx.TextCtrl(self, value="120", size=(100, 30), style=wx.TE_READONLY)
        bound_grid_sizer = wx.GridBagSizer(vgap=10, hgap=10)
        bound_grid_sizer.Add(bound_info_label, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(north_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(self.north_box, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(south_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(self.south_box, pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(west_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(self.west_box, pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(east_label, pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        bound_grid_sizer.Add(self.east_box, pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)

        # 创建保存文件与读取文件
        self.path_str = wx.StaticText(self, label='未选择文件', size=(200, 50))
        self.hint_str = wx.StaticText(self, label='', size=(200, 50))
        open_file_button = wx.Button(self, label="Open WPS File")
        open_file_button.Bind(wx.EVT_BUTTON, self.on_open_file)
        save_file_button = wx.Button(self, label="Save File")
        save_file_button.Bind(wx.EVT_BUTTON, self.on_save_file)

        # 创建BoxSizer
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vertical_sizer1 = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer2 = wx.BoxSizer(wx.VERTICAL)
        # 设置布局
        vertical_sizer1.Add(rich_text, proportion=0)
        vertical_sizer1.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        vertical_sizer1.Add(bound_grid_sizer, proportion=0, flag=wx.EXPAND)
        vertical_sizer2.Add(self.path_str, proportion=0, flag=wx.EXPAND)
        vertical_sizer2.Add(self.hint_str, proportion=0, flag=wx.EXPAND)
        vertical_sizer2.Add(open_file_button, 0, wx.EXPAND | wx.BOTTOM, 20)
        vertical_sizer2.Add(save_file_button, proportion=0, flag=wx.EXPAND)
        vertical_sizer2.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        vertical_sizer2.Add(grid_sizer, proportion=1, flag=wx.EXPAND) 
        horizontal_sizer.Add(self.canvas, proportion=1, flag=wx.EXPAND)
        horizontal_sizer.Add(vertical_sizer1, proportion=0,flag=wx.ALL | wx.EXPAND, border=20)
        horizontal_sizer.Add(wx.StaticLine(self, style=wx.VERTICAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        horizontal_sizer.Add(vertical_sizer2, proportion=0,flag=wx.ALL | wx.EXPAND, border=20)

        # 设置窗口的主 sizer
        self.SetSizer(horizontal_sizer)

        # 使用Basemap创建地图
        self.ax = self.figure.add_subplot(111)
        self.draw_map()

    def on_update_button_click(self, event):
        self.ax.clear()
        self.draw_map()

    def on_open_file(self, event):
        # 定义文件路径
        if self.wps_file:
            wps_file = os.path.abspath(self.wps_file)
            folder_path = os.path.dirname(wps_file)
            file_name = os.path.basename(wps_file)
        else:
            folder_path = os.getcwd()
            file_name = 'namelist.wps'
        # 创建文件选择器对话框
        file_dialog = wx.FileDialog(self, message="Choose a file",
                                    defaultDir=folder_path,
                                    defaultFile=file_name,
                                    wildcard="*.*",
                                    style=wx.FD_OPEN)

        # 显示文件选择器，如果用户点击“确定”，则获取选择的文件路径
        if file_dialog.ShowModal() == wx.ID_OK:
            selected_file = file_dialog.GetPath()
            print(f"Selected file: {selected_file}")
            self.load_wps_file(selected_file)
            self.path_str.SetLabel(selected_file)
            self.Layout()
            self.nl_file = selected_file

        # 销毁文件选择器以释放资源
        file_dialog.Destroy()

    def on_save_file(self, event):
        nl.modify(self.nl_file, 'e_we', self.e_we_box.GetValue())
        nl.modify(self.nl_file, 'e_sn', self.e_sn_box.GetValue())
        nl.modify(self.nl_file, 'ref_lat', self.ref_lat_box.GetValue())
        nl.modify(self.nl_file, 'ref_lon', self.ref_lon_box.GetValue())
        nl.modify(self.nl_file, 'truelat1', self.true_lat_box.GetValue())
        nl.modify(self.nl_file, 'stand_lon', self.stand_lon_box.GetValue())
        nl.modify(self.nl_file, 'dx', self.dx_box.GetValue())
        nl.modify(self.nl_file, 'dy', self.dx_box.GetValue())
        self.hint_str.SetLabel('修改成功')

    def load_wps_file(self, file_path):
        try:
            config = nl.load(file_path)
            # 读取namelist.wps中的参数
            ref_lat = config['geogrid']['ref_lat']
            ref_lon = config['geogrid']['ref_lon']
            true_lat = config['geogrid']['truelat1']
            stand_lon = config['geogrid']['stand_lon']
            delta = config['geogrid']['dx']
            e_we = config['geogrid']['e_we']
            e_sn = config['geogrid']['e_sn']
            self.e_we_box.SetValue(str(e_we))
            self.e_sn_box.SetValue(str(e_sn))
            self.ref_lat_box.SetValue(str(ref_lat))
            self.ref_lon_box.SetValue(str(ref_lon))
            self.true_lat_box.SetValue(str(true_lat))
            self.stand_lon_box.SetValue(str(stand_lon))
            self.dx_box.SetValue(str(delta))
            self.hint_str.SetLabel('namelist.wps文件成功加载')
            self.on_update_button_click(None)
        except KeyError:
            self.hint_str.SetLabel('namelist.wps文件读取失败')

    def draw_map(self):
        # 获取输入框的值
        e_we = int(self.e_we_box.GetValue())
        e_sn = int(self.e_sn_box.GetValue())
        ref_lat = float(self.ref_lat_box.GetValue())
        ref_lon = float(self.ref_lon_box.GetValue())
        dx = float(self.dx_box.GetValue())
        true_lat = float(self.true_lat_box.GetValue())
        north, west, south, east = miw(
            ref_lat, ref_lon, true_lat, dx, e_we, e_sn)

        self.map = Basemap(
            projection='merc',
            llcrnrlat=south,
            urcrnrlat=north,
            llcrnrlon=west,
            urcrnrlon=east,
            lat_ts=true_lat,
            resolution='l',
            ax=self.ax
        )
        self.map.drawcoastlines()
        self.map.drawcountries()
        self.map.fillcontinents(color='lightgray', lake_color='aqua', zorder=1)
        self.map.drawmapboundary(fill_color='white')

        # 绘制经纬线
        self.map.drawparallels(range(-90, 90, 5), labels=[
                               1, 0, 0, 0], linewidth=0.5, color='gray')
        self.map.drawmeridians(range(-180, 180, 5), labels=[
                               0, 0, 0, 1], linewidth=0.5, color='gray')

        # 更新画布
        self.canvas.draw()

        # 更新边界输入框的值
        self.north_box.SetValue(str(north))
        self.south_box.SetValue(str(south))
        self.west_box.SetValue(str(west))
        self.east_box.SetValue(str(east))


def main():
    parser = argparse.ArgumentParser(description='这是一个计算namelist.wps经纬度范围的程序')
    parser.add_argument('file', nargs='?', default=None, type=str, help='输入的namelist.wps文件')
    args = parser.parse_args()
    app = wx.App()
    frame = MyFrame(None, '地图投影计算器', args.file)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
