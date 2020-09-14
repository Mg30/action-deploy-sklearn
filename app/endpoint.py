from dataclasses import dataclass
import re
import sys


@dataclass
class Sls(object):
    regex: str = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    def find_endpoint(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf8") as f:
            content = f.read()
            urls = re.findall(self.regex, content)
            urls = [url[0] for url in urls]
            endpoint = urls[0]
        return endpoint

if __name__ == "__main__":
    file_path = sys.argv[-1]
    sls = Sls()
    endpoint = sls.find_endpoint(file_path)
    with open("/endpoint.txt", "w") as f:
        f.write(endpoint)