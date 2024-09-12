import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
 
async def check(domain, total_domains, current_domain):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
    }
 
    protocols = ["http://", "https://"]
    results = []
 
    print(f"\nChecking {domain}... ({current_domain}/{total_domains} domains left)\n" + "-" * 50)
 
    for protocol in protocols:
        url = f"{protocol}{domain}"
        try:
            async with httpx.AsyncClient(http2=True, verify=False) as client:
                response = await client.get(url, headers=headers, timeout=10)
            if response.http_version == "HTTP/2":
                results.append(colored(f"{url} supports HTTP/2", 'red'))
            else:
                results.append(f"{url} does not support (uses {response.http_version})")
        except httpx.RequestError:
            results.append(f"Connection error for {url}")
        except Exception as e:
            results.append(f"Error for {url}: {e}")
 
    for result in results:
        print(result)
 
def threaded_check(domain, total_domains, current_domain):
    return asyncio.run(check(domain, total_domains, current_domain))
 
def main():
    with open("domains.txt", "r") as temp:
        domains = temp.read().splitlines()
 
    total_domains = len(domains)
    current_domain = total_domains
 
    with ThreadPoolExecutor() as executor:
        list(executor.map(threaded_check, domains, [total_domains]*total_domains, range(total_domains, 0, -1)))
 
if __name__ == "__main__":
    main()