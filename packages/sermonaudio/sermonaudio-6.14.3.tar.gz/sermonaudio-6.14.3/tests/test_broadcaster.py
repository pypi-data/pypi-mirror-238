import secrets
from time import sleep

from .helpers import APITestCase

from sermonaudio import models
from sermonaudio.node.requests import Node
from sermonaudio.broadcaster.requests import BroadcasterAPIError, Broadcaster


class BroadcasterRequestTests(APITestCase):
    def test_deleting_missing_series(self):
        """Tests deleting a series which doesn't exist raises an exception."""
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.delete_series(id_or_title=f"Invalid {secrets.randbits(16)}", broadcaster_id="misc")

    def test_highlighted_sermons_bad_input(self):
        # Both sermon_id and event_type can't be supplied together.
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.set_highlighted_audio_sermon(
                audio_type=models.HighlightedAudioInputTypes.SERMON_ID,
                sermon_id="yerp",
                event_type=models.SermonEventType.SUNDAY_SERVICE,
                broadcaster_id="misc",
            )

        # Omitting sermon_id with SERMON_ID is not allowed.
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.set_highlighted_audio_sermon(
                audio_type=models.HighlightedAudioInputTypes.SERMON_ID, broadcaster_id="misc"
            )

        # Omitting event_type with EVENT_TYPE is not allowed.
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.set_highlighted_audio_sermon(
                audio_type=models.HighlightedAudioInputTypes.EVENT_TYPE, broadcaster_id="misc"
            )

    def test_welcome_video(self):
        """Tests clearing and setting the welcome video for misc.

        This test is idemponent, settin the welcome video back to its
        original value. But if the test fails, the welcome video may be
        erased. The sermon at development time was 92515832503.
        """
        # Get the value of the video and stash it...
        misc = Node.get_broadcaster("misc")
        welcome_video_id = misc.welcome_video_id

        # ... erase the video...
        success = Broadcaster.set_welcome_video(sermon_id=None, broadcaster_id="misc")
        assert success

        # ... wait out the endpoint cache...
        sleep(2)

        # ... and assert that the video has been cleared.
        misc = Node.get_broadcaster("misc")
        assert misc.welcome_video_id is None

        # Next, put the video back...
        success = Broadcaster.set_welcome_video(sermon_id=welcome_video_id, broadcaster_id="misc")
        assert success

        # ... wait out the endpoint cache again...
        sleep(2)

        # ... and make sure the value is the original value.
        misc = Node.get_broadcaster("misc")
        assert misc.welcome_video_id == welcome_video_id

    def test_welcome_video_invalid_sermon_id(self):
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.set_welcome_video(sermon_id="yerp", broadcaster_id="misc")

    def test_welcome_video_sermon_has_no_video(self):
        with self.assertRaises(BroadcasterAPIError):
            Broadcaster.set_welcome_video(
                sermon_id="117021689", broadcaster_id="misc"  # William Booth's "Short Excerpt"
            )
