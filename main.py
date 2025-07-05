import asyncio
import aiohttp
import colorama

FILENAME = 'proxies.txt'

class ProxyChecker():
    def __init__(self):
        self.proxies = self.load_proxies()

    def load_proxies(self):
        with open(FILENAME, 'r') as file:
            proxies = [proxy.strip() for proxy in file if proxy.strip()]

        return proxies

    async def check_proxy(self, proxy):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://httpbin.org/ip', proxy=f'http://{proxy}', timeout=5) as response:
                    if response.status == 200:
                        return {'status': 'ok', 'proxy': proxy}
                    else:
                        return {'status': 'not ok', 'proxy': proxy}
        except:
            return {'status': 'not ok', 'proxy': proxy}

    async def run(self):
        tasks = [self.check_proxy(proxy) for proxy in self.proxies]
        response = await asyncio.gather(*tasks)

        for result in response:
            status = result['status']
            proxy = result['proxy']

            if status == 'ok':
                print(colorama.Fore.GREEN + f'[+] Прокси {proxy} работает' + colorama.Fore.RESET)
            else:
                print(colorama.Fore.RED + f'[-] Прокси {proxy} не работает' + colorama.Fore.RESET)

if __name__ == '__main__':
    proxy_checker = ProxyChecker()
    asyncio.run(proxy_checker.run())