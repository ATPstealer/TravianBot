from auth import Request
from village import Village
from bs4 import BeautifulSoup

get = Request()


def get_villages(get):
    soup = BeautifulSoup(get.request("/dorf1.php").text, "html.parser")
    divs = soup.find_all(class_="listEntry")
    return [div['data-did'] for div in divs]


village_ids = get_villages(get)
for village_id in village_ids:
    village = Village(village_id, get)




