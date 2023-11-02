# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import re
import os

from headless.ext.picqer import DefaultClient
from headless.ext.picqer.v1 import Comment

os.environ['GOOGLE_DATASTORE_NAMESPACE'] = 'drt.molanouplink.com'
os.environ['GOOGLE_SERVICE_PROJECT'] = 'molano-i9v754'


async def main():
    pattern: re.Pattern[str] = re.compile('[0-9]{15}')
    async with DefaultClient() as picqer:
        async for comment in picqer.listall(Comment):
            if not comment.source_type == 'order':
                continue
            imei = pattern.findall(comment.body)
            if not imei:
                continue
            print(comment.document_number, ', '.join(imei))

if __name__ == '__main__':
    asyncio.run(main())