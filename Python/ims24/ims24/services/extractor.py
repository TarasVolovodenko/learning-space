#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# extractor.py
# @Author : Gustavo F (gustavo@gmf-tech.com)
# @Link   : https://github.com/sharkguto
# @Date   : 17/02/2019 11:38:47


from ims24.contrators.requester import RequesterCrawler
import html5lib
import re


class Extractor(RequesterCrawler):
    """
    implement RequesterCrawler class to do multiple requests async 
    using Future 
        :param RequesterCrawler: RequesterCrawler object
    """

    _endpoints = {}

    _endpoints_dive = {}

    def __init__(self, base_url: str = ""):
        """
        pass base_url or get from env variable
            :param self: itself
            :param base_url:str="": base_url
        """
        super().__init__(base_url)
        self.load_endpoints()
        self.regex_link = re.compile('data-go-to-expose-id="([0-9]+)"')

    def load_endpoints(self):
        """
        load endpoints dict 
            :param self: itself
        """
        for i in range(4000):

            self._endpoints[f"{i}"] = self._requester_url.format(pagination=i)

    def return_data(self):
        """
        run crawler and return a list of haus results
            :param self: itself
        """

        self.get_list(tuple(self._endpoints.keys()))

        return self._endpoints_dive

    def html_parser(self, text: str):
        """
        convert html to json
            :param self: itself
            :param text:str: html text to be parsed
        """
        list_ids_haus = self.regex_link.findall(text)

        self._endpoints_dive = {
            **self._endpoints_dive,
            **{
                f"{id_haus}": f"https://www.immobilienscout24.de/expose/{id_haus}"
                for id_haus in list_ids_haus
            },
        }

        print(self._endpoints_dive)


# /html/body/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/div/div/ul/li[1]/div/article/div/div[2]/div/div[3]/div/div[1]
# result-109925272 > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1)

