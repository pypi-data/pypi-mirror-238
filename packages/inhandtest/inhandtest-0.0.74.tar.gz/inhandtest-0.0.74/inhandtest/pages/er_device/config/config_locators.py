# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:47
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : config_locators.py
@IDE     : PyCharm
------------------------------------
"""
from playwright.sync_api import Page


class ConfigLocators():
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def wan_locator(self) -> list:
        return [
            ('type', {
                'locator': {'DEFAULT': self.page.locator('#ipType'),
                            'EAP600': self.page.locator('#ipType')}, 'type': 'select'}),
            ('ip_address', {
                'locator': {'DEFAULT': self.page.locator('#ip'),
                            'EAP600': self.page.locator('#ip')}, 'type': 'fill'}),
            ('mask', {
                'locator': {'DEFAULT': self.page.locator('#mask'),
                            'EAP600': self.page.locator('#mask')}, 'type': 'fill'}),
            ('gateway_address', {
                'locator': {"DEFAULT": self.page.locator('#gateway'),
                            "EAP600": self.page.locator('#gateway')},
                'type': 'input'}),
            ('main_dns', {
                'locator': {"DEFAULT": self.page.locator('#dns1'),
                            'EAP600': self.page.locator('#dns1')}, 'type': 'fill', }),
            ('secondary_dns', {
                'locator': {"DEFAULT": self.page.locator('#dns2'),
                            'EAP600': self.page.locator('#dns2')}, 'type': 'fill'}),
            ('mtu', {
                'locator': {"DEFAULT": self.page.locator('#mtu'),
                            'EAP600': self.page.locator('#mtu')}, 'type': 'fill'}),
            ('save', {
                'locator': {"DEFAULT": self.page.locator(f'button:has-text("{self.locale.get("save")}")'),
                            'EAP600': self.page.locator(f'button:has-text("{self.locale.get("save")}")')},
                'type': 'button'}),
            ('reset', {
                'locator': {"DEFAULT": self.page.locator(f'button:has-text("{self.locale.get("reset")}")'),
                            'EAP600': self.page.locator(f'button:has-text("{self.locale.get("reset")}")')},
                'type': 'button'}),
        ]

    @property
    def lan_locator(self) -> list:
        return [
            ('lan_resource',
             {'table': [
                 ('add', {'locator': {'DEFAULT': self.page.locator('.anticon.anticon-plus').first,
                                      'EAP600': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'DEFAULT': self.pop_up.locator('#lan_modal_alias'),
                                       'EAP600': self.pop_up.locator('#lan_modal_alias')},
                           'type': 'fill'}),
                 ('ip_mode',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_l3_vlan').locator('.ant-radio-input').first,
                      'EAP600': self.pop_up.locator('#lan_modal_l3_vlan').locator('.ant-radio-input').first},
                      'type': 'check'}),
                 ('vlan_only_mode',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_l3_vlan').locator('.ant-radio-input').nth(1),
                      'EAP600': self.pop_up.locator('#lan_modal_l3_vlan').locator('.ant-radio-input').nth(1)},
                      'type': 'check'}),
                 ('standard',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_guest').locator('.ant-radio-input').nth(1),
                      'EAP600': self.pop_up.locator('#lan_modal_guest').locator('.ant-radio-input').nth(1)},
                      'type': 'check'}),
                 ('guest',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_guest').locator('.ant-radio-input').nth(1),
                      'EAP600': self.pop_up.locator('#lan_modal_guest').locator('.ant-radio-input').nth(1)},
                      'type': 'check', "relation": [('ip_mode', 'check')]}),
                 ('vlan',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_vlan'),
                      'EAP600': self.pop_up.locator('#lan_modal_vlan')},
                      'type': 'fill'}),
                 ('ip_address_mask',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_ipv4_ip'),
                      'EAP600': self.pop_up.locator('#lan_modal_ipv4_ip')},
                      'type': 'fill', "relation": [('ip_mode', 'check')]}),
                 ('dhcp_server',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_enabled'),
                      'EAP600': self.pop_up.locator('#lan_modal_enabled')},
                      'type': 'switch_button', "relation": [('ip_mode', 'check')]}),
                 ('dhcp_ip_range_start_ip',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_ip_pool_start_ip'),
                      'EAP600': self.pop_up.locator('#lan_modal_ip_pool_start_ip')},
                      'type': 'fill', "relation": [('ip_mode', 'check')]}),
                 ('dhcp_ip_range_end_ip',
                  {'locator': {
                      'DEFAULT': self.pop_up.locator('#lan_modal_ip_pool_end_ip'),
                      'EAP600': self.pop_up.locator('#lan_modal_ip_pool_end_ip')},
                      'type': 'fill', "relation": [('ip_mode', 'check')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'DEFAULT': self.pop_up, 'EAP600': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'DEFAULT': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                                                 'EAP600': self.page.locator('.ant-popover-inner-content').locator(
                                                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'DEFAULT': self.page.locator('.ant-table-container').nth(0),
                             'EAP600': self.page.locator('.ant-table-container').nth(0)},
                 'type': 'table_tr', })
        ]
