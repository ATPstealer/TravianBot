from bs4 import BeautifulSoup


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
        self.show_resources()
        self.get_buildings()
        self.show_buildings()

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
