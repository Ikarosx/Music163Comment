from scrapy import cmdline
import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
cmdline.execute("scrapy crawl Music163".split())