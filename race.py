import aiohttp
import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Race:
    def __init__(self):
        self.loop = None
        self.requests_list = []

    def add_request(self, http_request, throttle_ms, proxy, verify, print_response):
        if verify:
            verify = None

        self.requests_list.append({'request': {'method': http_request.get_method(),
                                               'url': http_request.get_full_url(),
                                               'headers': http_request.get_headers(),
                                               'data': http_request.get_body(),
                                               'proxy': proxy,
                                               'ssl': verify},
                                   'throttle_ms': throttle_ms,
                                   'print_response': print_response})

    def go(self, threads=100):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.run_funcs(threads))
        self.loop.close()

    async def run_funcs(self, threads):
        jar = aiohttp.DummyCookieJar()
        connector = aiohttp.TCPConnector(limit=threads)
        async with aiohttp.ClientSession(connector=connector, cookie_jar=jar) as session:
            tasks = []
            for req in self.requests_list:
                tasks.append(self.loop.create_task(self.run_func(session, req['request'], req['throttle_ms'],
                                                                 req['print_response']))),

            await asyncio.wait(tasks)

    async def run_func(self, session, request_params, throttle_ms, print_response):
        await asyncio.sleep(throttle_ms / 1000)
        async with session.request(**request_params, allow_redirects=False) as resp:
            await self.result(resp, print_response)

    async def result(self, response, print_response):
        print('{} {} | {}'.format(response.method, response.url, response.status))
        if print_response:
            print(await response.text())
