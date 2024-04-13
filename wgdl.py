import bs4
import os
import requests
import sys

USAGE = """Usage: wgdl </wg thread code>
This downloads all images from 4chan.org/wg/thread/<code>"""

IMAGE_TYPE = ("png", "jpg", "jpeg", "webp")

# TODO: write a terminal interface that lets user select a thread directly from terminal, without the need to use a browser


def draw_progress(actual: int, total: int):
    sys.stdout.write("\r")
    sys.stdout.write("Progress: [" + str(actual) + " of " + str(total) + "]")
    sys.stdout.flush()


# exit if no code was provided
if len(sys.argv) < 2:
    sys.exit(USAGE)

link = "https://boards.4chan.org/wg/thread/" + sys.argv[1]

res = requests.get(link)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html.parser")

title = soup.select(".subject")[0].getText()

images = set()
anchors = soup.select("a")
for a in anchors:
    href = a.get("href")
    if "http" not in href:
        href = "https:" + href
    for it in IMAGE_TYPE:
        if it in href:
            images.add(href)
            break

total = len(images)
dirname = (title if title != '' else 'wg')
os.mkdir(dirname)
draw_progress(0, total)
for num, img in enumerate(images):
    res = requests.get(img)
    with open(dirname + "/img" + str(num), "wb") as fp:
        for chunk in res.iter_content(10000):
            fp.write(chunk)
    draw_progress(num+1, total)

sys.stdout.write("\n")
