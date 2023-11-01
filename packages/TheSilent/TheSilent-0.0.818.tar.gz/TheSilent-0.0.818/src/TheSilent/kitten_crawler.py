import re
import time
import urllib.parse
from TheSilent.clear import clear
import TheSilent.puppy_requests as puppy

CYAN = "\033[1;36m"

def kitten_crawler(host,delay=0,crawl=1):
    clear()
    hits = [host]
    total = []
    for depth in range(crawl):
        hits = list(dict.fromkeys(hits[:]))
        try:
            if urllib.parse.urlparse(host).netloc in hits[depth] or "js" in hits[depth]:
                time.sleep(delay)
                print(CYAN + hits[depth])
                data = puppy.text(hits[depth])
        except IndexError:
            break
        except:
            continue

        try:
            links = re.findall("content\s*=\s*[\"\'](\S+)[\"\']|href\s*=\s*[\"\'](\S+)[\"\']|src\s*=\s*[\"\'](\S+)[\"\']",data.lower())
            for link in links:
                for _ in link:
                    if _ != "" and "script" not in _ and "base64" not in _:
                        _ = _.split('"')[0]
                        _ = _.split("'")[0]
                        if _.startswith("/") and not _.startswith("//"):
                            hits.append(f"{host}{_}")
                            total.append(f"{host}{_}")
                        elif not _.startswith("/") and not _.startswith("http://") and not _.startswith("https://"):
                            hits.append(f"{host}/{_}")
                            total.append(f"{host}/{_}")
                        elif _.startswith("http://") or _.startswith("https://"):
                            hits.append(_)
                            total.append(_)
        except:
            pass

    hits = list(dict.fromkeys(hits[:]))
    hits.sort()
    results = []
    for hit in hits:
        if urllib.parse.urlparse(host).netloc in hit:
            results.append(hit)
    clear()
    return results
