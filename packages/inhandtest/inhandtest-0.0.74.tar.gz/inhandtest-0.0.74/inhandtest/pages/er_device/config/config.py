# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:47
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : config.py
@IDE     : PyCharm
------------------------------------
"""
import allure

from inhandtest.base_page import BasePage
from inhandtest.pages.er_device.config.config_locators import ConfigLocators
from inhandtest.pages.er_device.locators import ErLocators


class Config(BasePage, ErLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, **kwargs):
        super().__init__(host, username, password, protocol, port, model, language, page, **kwargs)
        ErLocators.__init__(self, page, kwargs.get('locale'))

    @allure.step('config菜单中配置lan')
    def lan(self, **kwargs):
        """

        :param kwargs:
           lan_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        ip_mode: 'check'|'uncheck'
                        vlan_only_mode: 'check'|'uncheck'
                        standard: 'check'|'uncheck'
                        guest: 'check'|'uncheck'
                        vlan: int
                        ip_address_mask: str, '192.168.2.1/24'
                        dhcp_server: 'enable'|'disable'
                        dhcp_ip_range_start_ip: str, '192.168.2.1'
                        dhcp_ip_range_end_ip: str, '192.168.2.254'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('config.lan')
        self.agg_in(self.config_locators.lan_locator, kwargs)


class EAP600Config():
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, **kwargs):
        self.__config = Config(host, username, password, protocol, port, model, language, page, **kwargs)

    def lan(self, **kwargs):
        """

        :param kwargs:
           lan_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        ip_mode: 'check'|'uncheck'
                        vlan_only_mode: 'check'|'uncheck'
                        standard: 'check'|'uncheck'
                        guest: 'check'|'uncheck'
                        vlan: int
                        ip_address_mask: str, '192.168.2.1/24'
                        dhcp_server: 'enable'|'disable'
                        dhcp_ip_range_start_ip: str, '192.168.2.1'
                        dhcp_ip_range_end_ip: str, '192.168.2.254'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        return self.__config.lan(**kwargs)



if __name__ == '__main__':
    a = EAP600Config(host='10.5.33.50', username='adm',password='123456', model='EAP600', language='en')
    a.lan(lan_resource=('add', {'name':'test', 'vlan': '20', 'ip_address_mask':'192.168.3.1/24'}))