from auth import Request
from village import Village
from bs4 import BeautifulSoup


def get_villages():
    get = Request()
    soup = BeautifulSoup(get.request("/dorf1.php").text, "html.parser")
    divs = soup.find_all(class_="listEntry")
    return [div['data-did'] for div in divs]


village_ids = get_villages()
print(village_ids)



# village = Village("17901")

