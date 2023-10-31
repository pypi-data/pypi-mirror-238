import ftplib
import time
import threading
import argparse
import os.path as op
import os
from concurrent.futures import ThreadPoolExecutor


class LinkFTP:
    def __init__(self, name='ftpA'):
        self.f = ftplib.FTP()
        self.f.connect('ftp.avl.class.noaa.gov')
        self.f.login('', '')
        self.downloading = 0
        self.name = name
        self.lock = threading.Lock()
        self.num = 1
        print(f'{self.name}初始化完成')

    def download_file(self, remote_path, local_path):
        # 这里必须进行加锁处理，同一个FTP对象只能同时获取一个文件
        self.lock.acquire()
        print(self.name, '将下载其自己的第', self.num, '个文件', remote_path)
        with open(local_path, 'wb') as fp:
            self.f.retrbinary('RETR '+remote_path, fp.write, 2048)
        self.num += 1
        self.lock.release()

    def get_filenames(self, dir='./'):
        filenames = [filename for filename,
                     info in self.f.mlsd(dir) if info['type'] == 'file']
        return filenames

    def quit(self):
        self.f.close()


class FTPPooling:
    def __init__(self, num_ftp):
        self.num_ftp = num_ftp
        with ThreadPoolExecutor(10) as t:
            res = t.map(lambda i: LinkFTP(f'ftp{i}'), list(range(num_ftp)))
            self.ftps = list(res)
        self.threads = []

    def close(self):
        for f in self.ftps:
            f.quit()

    def setFiles(self, filepath, filenames):
        files_full_path = [f"{filepath}/{filename}" for filename in filenames]
        self.filenames = filenames
        self.filenames_group = [files_full_path[i:i+self.num_ftp]
                                for i in range(0, len(files_full_path), self.num_ftp)]

    def set_save_path(self, local_path='./', sub_dir=None):
        self.save_path = local_path
        if sub_dir:
            self.save_path = op.join(local_path, sub_dir)
        if not op.exists(self.save_path):
            os.makedirs(self.save_path)
            print('目标目录不存在，将创建目录')

    def download(self):
        for group in self.filenames_group:
            for i, filename in enumerate(group):
                basename = op.basename(filename)
                t = threading.Thread(target=self.ftps[i].download_file, args=(
                    filename, op.join(self.save_path, basename)))
                t.start()
                self.threads.append(t)
                time.sleep(0.01)
        self.wait()

    def wait(self):
        for t in self.threads:
            t.join()

    def quit(self):
        for f in self.ftps:
            f.quit()


def main(order_id, num_ftp, save_path):
    '''
    order_id: 订单号
    num_ftp: ftp最大数量
    save_path: 保存路径
    '''
    # 测试FTP可用性，以及获取对应订单的文件
    print(f'订单号为：{order_id}')
    print('-------------------')
    fi = LinkFTP('ftp测试用例')
    filepath = f'/{order_id}/001'  # 对面FTP服务上的文件夹路径
    filenames = fi.get_filenames(filepath)
    print(f'订单{order_id}有{len(filenames)}个文件')
    fi.quit()
    # 下载文件
    num_ftp = min(num_ftp, len(filenames))
    print(f'将使用{num_ftp}个ftp下载')
    print(f'保存路径为{save_path}')
    print('-------------------')
    # 下载文件
    ftp_pool = FTPPooling(num_ftp)
    ftp_pool.setFiles(filepath, filenames)
    ftp_pool.set_save_path(save_path)
    ftp_pool.download()
    ftp_pool.close()

    print("全部下载完成")


def commond():
    '''
    命令行调用
    '''
    parser = argparse.ArgumentParser(description='下载NOAA数据，比如ATMS L1 L2的数据')
    parser.add_argument('order', type=str, help='订单编号')
    parser.add_argument('--nftp', '-n', default=30,
                        type=int, help='ftp最大数量，默认为%(default)s')
    parser.add_argument('-o', dest='save_path', metavar='PATH',
                        default='./', type=str, help='保存路径，默认为当前路径')
    args = parser.parse_args()

    order_id = args.order
    num_ftp = args.nftp
    save_path = args.save_path
    main(order_id, num_ftp, save_path)


if __name__ == '__main__':
    commond()
