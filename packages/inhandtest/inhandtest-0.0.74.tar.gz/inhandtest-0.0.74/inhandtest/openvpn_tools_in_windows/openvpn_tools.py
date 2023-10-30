# -*- coding: utf-8 -*-
# @Time    : 2023/10/9 14:22:52
# @Author  : Pane Li
# @File    : openvpn_tools.py
"""
openvpn_tools, 使用前请先安装openvpn客户端在windows系统上，由于虚拟网卡的原因，同一时间只能连接一个客户端
windows 系统上安装版本建议控制在2.4.9

"""
import os
import logging
import time
from inhandtest.tools import check_windows_process
from subprocess import Popen, PIPE
from os.path import abspath


class OpenvpnClientWindows:

    def __init__(self, vpn_bin_path: str, vpn_config_path: str):
        """

        :param vpn_bin_path:  C:\\Program Files\\OpenVPN\\bin
        :param vpn_config_path:  C:\\Program Files\\OpenVPN\\bin\\liwei@inhand.com.cn.ovpn
        """
        self.vpn_bin_path = vpn_bin_path
        self.vpn_config_path = vpn_config_path
        self.vpn_exe_path = os.path.join(self.vpn_bin_path, 'openvpn.exe')
        self.__connect_status = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def connect_status(self) -> bool:
        return self.__connect_status

    def connect(self, vpn_config_path=None, retry=5):
        """

        :param vpn_config_path:  配置文件路径, 默认为初始化时传入的配置文件路径
        :param retry:  5次， 每次间隔10秒
        :return:
        """
        self.vpn_config_path = abspath(vpn_config_path) if vpn_config_path else abspath(self.vpn_config_path)
        logging.info(f'Connecting to vpn {self.vpn_config_path}')
        check_windows_process('openvpn.exe', True)  # kill openvpn.exe  只能启动一个，原因是虚拟网卡的问题
        self.__connect_status = False
        command = [f'{self.vpn_exe_path}', '--config', f'{self.vpn_config_path}']
        for i in range(retry):
            process = Popen(command, cwd=self.vpn_bin_path, stdout=PIPE, encoding='utf-8', universal_newlines=True,
                            errors='ignore')
            for line in process.stdout:
                logging.debug(line.strip())
                if 'Initialization Sequence Completed' in line:
                    self.__connect_status = True
                    break
                if 'check your network connectivity' in line:
                    raise ConnectionError(
                        f'Connected to vpn {self.vpn_config_path} failed! check your network connectivity')
            if self.connect_status:
                break
            logging.warning(f'Connect to vpn {self.vpn_config_path} failed! 10s later retry {i + 1} times ...')
            time.sleep(10)
        else:
            raise ConnectionError(f'Connect to vpn {self.vpn_config_path} failed!')

    def disconnect(self):
        check_windows_process('openvpn.exe', True)
        self.__connect_status = False
        logging.info("Disconnected all openvpn client")


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    vpn = OpenvpnClientWindows("D:/Program Files/OpenVPN/bin", 'D:/Program Files//OpenVPN/bin/liwei@inhand.com.cn.ovpn')
    vpn.connect()
    # vpn.connect('D:/Program Files/OpenVPN/bin/testsss@alibaba.com.ovpn')
    # vpn.disconnect()
