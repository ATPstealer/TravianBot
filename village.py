from auth import Request


class Village:
    def __init__(self, village_id):
        self.village_id = village_id
        self.get = Request()
        self.get_resources()
        self.get_buildings()

    def get_resources(self):
        resources_page = self.get.request("/dorf1.php?newdid=" + self.village_id)
        print(resources_page.text)

    def get_buildings(self):
        resources_page = self.get.request("/dorf2.php?newdid=" + self.village_id)
        print(resources_page.text)
