from test.base import ApiDBTestCase

from zou.app.project import asset_info

from zou.app.utils import events


class CreateAssetsTestCase(ApiDBTestCase):

    def setUp(self):
        super(CreateAssetsTestCase, self).setUp()

        self.generate_fixture_project_status()
        self.generate_fixture_project()
        self.generate_fixture_entity_type()

        self.is_event_fired = False
        events.unregister_all()

    def handle_event(self, data):
        self.is_event_fired = True
        self.assertEqual(
            data["asset"]["name"],
            self.asset_data["name"].capitalize()
        )
        self.assertEqual(
            data["asset_type"]["id"],
            str(self.entity_type.id)
        )
        self.assertEqual(
            data["project"]["id"],
            str(self.project.id)
        )

    def test_create_asset(self):
        events.register(
            "asset:new",
            "handle_event",
            self
        )
        self.asset_data = {
            "name": "car",
            "description": "Test description"
        }
        path = "data/projects/%s/asset-types/%s/assets/new" % (
            self.project.id,
            self.entity_type.id
        )
        asset = self.post(path, self.asset_data)
        assets = asset_info.get_assets()
        self.assertIsNotNone(asset.get("id", None))
        self.assertEquals(len(assets), 1)
        self.assertEquals(assets[0].name, self.asset_data["name"].capitalize())
        self.assertEquals(
            assets[0].description,
            self.asset_data["description"]
        )

    def test_remove_asset(self):
        self.generate_fixture_entity()
        path = "data/projects/%s/asset-types/%s/assets/%s" % (
            self.project.id,
            self.entity_type.id,
            self.entity.id
        )
        self.delete(path)
        assets = asset_info.get_assets()
        self.assertEquals(len(assets), 0)
