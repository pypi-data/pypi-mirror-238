"""Test esoteric data model features"""

from .helpers import APITestCase

from sermonaudio import models


class ModelTests(APITestCase):
    def test_model_override(self):
        @models.override_model(models.MediaSet)
        class NewMediaSet(models.MediaSet):
            def __init__(self, obj: dict):
                super().__init__(obj)

                # Note: this is a get because this actually affects all other tests given the way
                # pytest works lol
                self.foo = obj.get("foo")

        try:

            @models.override_model(models.MediaSet)
            class OtherMediaSet(models.MediaSet):
                pass

        except models.MultipleOverrideError:
            pass
        else:
            self.assertTrue(False, "This should have failed due to overriding the same model twice.")

        data = {"audio": [], "video": [], "text": [], "foo": 42}

        parsed = models.MediaSet.parse(data)

        self.assertEqual(parsed.foo, NewMediaSet(data).foo)
        self.assertEqual(parsed.foo, 42)

    def test_generic_speakers(self):
        speaker_data = {
            "displayName": "Foo Bar",
            "sortName": "Bar, Foo",
            "bio": "I am an anthropomorphic metasyntactic entity with a split personality.",
            "portraitURL": "http://example.com/image.png",
            "albumArtURL": "http://example.com/{size}/{size}/image.png",
            "roundedThumbnailImageURL": "http://example.com/image_round.png",
        }

        # This is not one of the known generic speaker names
        self.assertFalse(models.Speaker(speaker_data).is_generic)

        for generic_name in models._generic_speaker_names:
            speaker_data["displayName"] = generic_name
            self.assertTrue(models.Speaker(speaker_data).is_generic)

    def test_sort_orders(self):
        """Minimally tests sort order parameters are sane."""
        for order in models.HighlightedSortOrders:
            assert type(order.sermon_parameters) == dict

    def test_highlighted_sermons_with_nones(self):
        """Test the highlighted sermons object handles None values."""
        params = {"sortOrder": None, "sortTitle": None, "audioTitle": None, "audioSermon": None}

        h = models.HighlightedSermons.parse(params)
        self.assertIsNone(h.sort_order)
        self.assertIsNone(h.sort_title)
        self.assertIsNone(h.audio_title)
        self.assertIsNone(h.audio_sermon)
