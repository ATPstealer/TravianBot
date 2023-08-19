from bs4 import BeautifulSoup
from build_list import build_list


class Resource:
    def __init__(self, land_type, level, slot, gid):
        self.land_type = land_type
        self.level = level
        self.slot = slot
        self.gid = gid


class Building:
    def __init__(self, building_type, level, slot, gid):
        self.building_type = building_type
        self.level = level
        self.slot = slot
        self.gid = gid


class Village:
    def __init__(self, village_id, get):
        print(village_id)
        self.village_id = village_id
        self.get = get
        self.resources = []
        self.buildings = []
        self.get_resources()
        # self.show_resources()
        self.get_buildings()
        # self.show_buildings()
        self.check_list()

    def get_resources(self):
        soup = BeautifulSoup(self.get.request("/dorf1.php?newdid=" + self.village_id).text, "html.parser")
        resource_fields = soup.find(id="resourceFieldContainer")
        for resource_field in resource_fields.find_all(class_="level"):
            classes = resource_field['class']
            if "gid1" in classes:
                land_type = "Woodcutter"
            elif "gid2" in classes:
                land_type = "Clay Pit"
            elif "gid3" in classes:
                land_type = "Iron Mine"
            elif "gid4" in classes:
                land_type = "Cropland"
            level_str = next(c for c in classes if c.startswith('level') and c != 'level')
            level = int(''.join(filter(str.isdigit, level_str)))
            slot_str = next(c for c in classes if c.startswith('buildingSlot'))
            slot = int(''.join(filter(str.isdigit, slot_str)))
            gid_str = next(c for c in classes if c.startswith('gid'))
            gid = int(''.join(filter(str.isdigit, gid_str)))
            self.resources.append(Resource(land_type, level, slot, gid))

    def get_buildings(self):
        soup = BeautifulSoup(self.get.request("/dorf2.php?newdid=" + self.village_id).text, "html.parser")
        buildings_divs = soup.find(id="villageContent")
        for div in buildings_divs.find_all(class_="buildingSlot"):
            level = div.find("a")['data-level'] if div['data-gid'] != "0" else 0
            self.buildings.append(Building(div['data-name'], int(level), int(div['data-aid']), int(div['data-gid'])))

    def show_resources(self):
        for res in self.resources:
            print(res.land_type, res.level, res.slot, res.gid)

    def show_buildings(self):
        for building in self.buildings:
            print(building.building_type, building.level, building.slot, building.gid)

    def check_list(self):
        for build_task in build_list:
            if build_task["type"] == "resource":
                for res in self.resources:
                    if res.land_type == build_task["land_type"] and res.level < build_task["level"]:
                        print(build_task)
                        if not self.upgrade(res):
                            return
            if build_task["type"] == "building":
                for building in self.buildings:
                    if building.building_type == build_task["building_type"] and building.level < build_task["level"]:
                        print(build_task)
                        if not self.upgrade(building):
                            return

    def upgrade(self, construction):
        soup = BeautifulSoup(self.get.request("/build.php?newdid=" + self.village_id + "&id=" + str(construction.slot)).text, "html.parser")
        button = soup.find("button", class_="textButtonV1 green build")
        if button:
            start = button['onclick'].find("'") + 1
            end = button['onclick'].find("'", start)
            url = button['onclick'][start:end]
            self.get.request(url + "&newdid=" + self.village_id)
            if construction.land_type:
                print("Start build " + construction.land_type + " level " + str(construction.level) + " on slot " +
                      str(construction.slot))
            else:
                print("Start build " + construction.building_type + " level " + str(construction.level) + " on slot " +
                      str(construction.slot))
            return True
        else:
            print("Workers busy")
            return False
