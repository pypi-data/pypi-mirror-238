# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from bs4 import BeautifulSoup
from datetime import datetime
import requests

from .base_parser import BaseParser


@dataclass
class WebsiteInfo:
    placement: str
    title: str = ""
    description: str = ""
    keywords: str = ""
    is_processed: bool = False
    last_processed_time: datetime = datetime.now()


class WebSiteParser(BaseParser):

    def parse(self, placement: str) -> WebsiteInfo:
        url = self._convert_placement_to_url(placement)
        try:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            description = soup.find('meta', attrs={'name': 'description'})
            return WebsiteInfo(
                placement=placement,
                title=soup.title.string if soup.title else None,
                keywords=keywords.get("content") if keywords else None,
                description=description.get("content")
                if description else None,
                is_processed=True)
        except Exception as e:
            print(e)
            return WebsiteInfo(placement=placement)

    def _convert_placement_to_url(self, placement: str) -> str:
        if "http" not in placement:
            https = "https://"
            url = f"https://{placement}"
        else:
            url = placement
        return url
