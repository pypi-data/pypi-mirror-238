# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:38
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : locators.py
@IDE     : PyCharm
------------------------------------
"""
from playwright.sync_api import Page, Locator

from inhandtest.pages.er_device.config.config_locators import ConfigLocators


class ErLocators:
    def __init__(self, page: Page, locale):
        self.page = page
        self.locale = locale
        self.config_locators = ConfigLocators(page, self.locale)

    @property
    def interface(self) -> dict:
        return {'er805_interface': {'default': 'Default', 'wan1': 'WAN1', 'wan2': 'WAN2', 'cellular': 'Cellular',
                                    'wifi-sta': 'Wi-Fi(STA)', 'any': 'Any'},
                'er605_interface': {'default': 'Default', 'wan1': 'WAN1', 'wan2': 'WAN2', 'cellular': 'Cellular',
                                    'wifi-sta': 'Wi-Fi(STA)', 'any': 'Any'},
                'odu2002_interface': {'any': 'Any', 'wan1': 'WAN', 'cellular': 'Cellular', 'default': 'Default'},
                'fwa02_interface': {'any': 'Any', 'wan1': 'WAN', 'cellular': 'Cellular', 'default': 'Default'}}

