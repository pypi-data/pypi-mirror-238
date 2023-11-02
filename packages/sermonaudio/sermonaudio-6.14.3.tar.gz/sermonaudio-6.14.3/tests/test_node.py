from osis_book_tools import OSISBook

from sermonaudio.models import LiteContainedBroadcaster, SeriesSortOrder, SermonSortOption, SeriesFilter

from .helpers import (
    APITestCase,
    order_is_preach_date_descending,
    order_is_download_count_descending,
)

from sermonaudio import models
from sermonaudio.node.requests import NodeAPIError, Node


class SermonTests(APITestCase):
    def test_get_sermon(self):
        sermon_id = "261601260"
        sermon = Node.get_sermon(sermon_id)

        self.assertIsNotNone(sermon)
        self.assertEqual(sermon.sermon_id, sermon_id)

        sermon = Node.get_sermon(sermon_id, lite_broadcaster=True)
        self.assertIsNotNone(sermon)
        self.assertEqual(sermon.sermon_id, sermon_id)
        self.assertEqual(type(sermon.broadcaster), LiteContainedBroadcaster)

        sermon = Node.get_sermon(sermon_id, lite=True)
        self.assertIsNotNone(sermon)
        self.assertEqual(sermon.sermon_id, sermon_id)
        self.assertEqual(type(sermon), models.LiteSermon)

    def test_get_invalid_sermon(self):
        self.assertIsNone(Node.get_sermon("26160126sl;fkjsd0"))

    def test_sermons_by_broadcaster(self):
        broadcaster_id = "faith"
        response = Node.get_sermons(broadcaster_id=broadcaster_id)

        self.assertIsNotNone(response)
        self.assertGreater(response.total_count, len(response.results))

        for sermon in response.results:
            self.assertEqual(sermon.broadcaster.broadcaster_id, broadcaster_id)

    def test_sermons_lite_broadcaster(self):
        broadcaster_id = "faith"
        response = Node.get_sermons(broadcaster_id=broadcaster_id, lite_broadcaster=True)

        self.assertIsNotNone(response)
        self.assertGreater(response.total_count, len(response.results))

        for sermon in response.results:
            self.assertEqual(type(sermon.broadcaster), LiteContainedBroadcaster)

    def test_sermons_lite(self):
        broadcaster_id = "faith"
        response = Node.get_sermons(broadcaster_id=broadcaster_id, lite=True)

        self.assertIsNotNone(response)
        self.assertGreater(response.total_count, len(response.results))

        for sermon in response.results:
            self.assertEqual(type(sermon), models.LiteSermon)

    def test_sermons_sortby_update_date(self):
        broadcaster_id = "faith"
        response = Node.get_sermons(broadcaster_id=broadcaster_id, sort_by=SermonSortOption.UPDATED)

        last_update_date = None
        for r in response.results:
            if last_update_date is not None:
                self.assertGreaterEqual(last_update_date, r.update_date)
            last_update_date = r.update_date

    def test_sermons_by_book(self):
        # This test is not strictly necessary, but was added to test against regression after
        # switching to the osis_book_tools library
        book = OSISBook.Gen
        response = Node.get_sermons(book=book)

        self.assertIsNotNone(response)
        self.assertGreater(response.total_count, len(response.results))

        for sermon in response.results:
            self.assertTrue(book.chapter_descriptor("en") in sermon.bible_text)

    def test_sermon_video_and_document_count(self):
        # "Much Prayer Much Blessing, Little Prayer Little Blessing, No Prayer
        # No Blessing" is a Faith FPC power clip by Alan Cairns that has a lot
        # of video downloads and is likely not going to be removed. Happily, it
        # also has a transcript so it should always have a positive video and
        # document count.
        # https://www.sermonaudio.com/sermoninfo.asp?SID=10270420220
        sermon_id = "10270420220"
        sermon = Node.get_sermon(sermon_id)

        self.assertIsNotNone(sermon)
        self.assertGreater(sermon.download_count, 0)
        self.assertGreater(sermon.video_download_count, 0)
        self.assertGreater(sermon.document_download_count, 0)

        # This is a "Sunday School Lesson" with neither video nor transcript,
        # so these two counts should always be zero.
        # https://www.sermonaudio.com/sermoninfo.asp?SID=110418150222283
        sermon_id = "110418150222283"
        sermon = Node.get_sermon(sermon_id)

        self.assertIsNotNone(sermon)
        self.assertGreater(sermon.download_count, 0)
        self.assertEqual(sermon.video_download_count, 0)
        self.assertEqual(sermon.document_download_count, 0)

    def test_sermon_display_type(self):
        sermon_id = "261601260"  # event type is Sunday Service
        sermon = Node.get_sermon(sermon_id, preferred_language_override="es")

        self.assertIsNotNone(sermon)
        self.assertEqual(sermon.display_event_type, "Servicio Dominical")

    def test_last_feature_date(self):
        """Tests that featured sermons have a last feature date."""

        response = Node.get_sermons(featured=True, page_size=5)

        self.assertIsNotNone(response)

        for sermon in response.results:
            self.assertIsNotNone(sermon.last_feature_date)


class BroadcasterNodeTests(APITestCase):
    def test_get_broadcaster(self):
        broadcaster_id = "faith"
        response = Node.get_broadcaster(broadcaster_id)

        self.assertIsNotNone(response)
        self.assertEqual(response.broadcaster_id, broadcaster_id)

        self.assertEqual(response.country_iso_code, "US")

        self.assertIsNone(Node.get_broadcaster("foobar123"))

    def test_broadcasters_near_location(self):
        response = Node.get_broadcasters_near_location(34.867_104, -82.330_768, 1000)

        self.assertIsNotNone(response)

        for loc in response:
            if loc.broadcaster.broadcaster_id == "faith":
                return  # Found a match

        self.fail("Expected to find broadcaster faith in Greenville, SC.")

    def test_broadcaster_series_list(self):
        response = Node.get_series_list("faith")

        self.assertIsNotNone(response)

        # Faith should have > the default page size; this tests the pagination
        # defaults on this endpoint (which should return 50 by default)
        self.assertEqual(len(response.results), 50)

    def test_get_sermon_event_types(self):
        response = Node.get_sermon_event_types("faith")

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 1)  # Faith should always have at least one ;)

        self.assertGreater(len(Node.get_sermon_event_types()), len(Node.get_sermon_event_types("hpbc")))

    def test_get_sermon_event_types_localized(self):
        """Tests localization of SermonEventTypeDetail objects."""
        response = Node.get_sermon_event_types("faith", preferred_language_override="ko")
        for detail in response:
            assert detail.description != detail.display_event_type

    def test_broadcaster_speaker_list(self):
        response = Node.get_speakers_for_broadcaster("faith")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 1)
        speaker_names = {s.display_name for s in response}
        self.assertTrue("Dr. Alan Cairns" in speaker_names)

    def test_broadcaster_sermon_count_for_speakers_list(self):
        response = Node.get_speaker_sermon_counts_for_broadcaster("faith")
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 1)
        speaker_names = {s.speaker_name for s in response}
        self.assertTrue("Dr. Alan Cairns" in speaker_names)

        for speaker in response:
            if speaker.speaker_name == "Dr. Alan Cairns":
                self.assertGreater(speaker.count, 1)


class SeriesTests(APITestCase):
    broadcaster_id = "faith"

    def test_valid_single_series(self):
        valid_series_name = "Studies in Romans"
        response = Node.get_series(broadcaster_id=self.broadcaster_id, series_name=valid_series_name)
        self.assertIsNotNone(response)
        self.assertEqual(response.title, valid_series_name)

    def test_invalid_single_series(self):
        invalid_series_name = "9999999999999999"
        response = Node.get_series(broadcaster_id=self.broadcaster_id, series_name=invalid_series_name)
        self.assertIsNone(response)

    def test_series_list(self):
        page_size = 10  # smaller page to speed up tests

        # Get the first page.
        response = Node.get_series_list(broadcaster_id=self.broadcaster_id, page=1, page_size=page_size)
        self.assertIsNotNone(response)
        self.assertEqual(len(response.results), page_size)
        page1_titles = {r.title for r in response.results}

        # Get the next page...
        response = Node.get_series_list(broadcaster_id=self.broadcaster_id, page=2, page_size=page_size)
        self.assertIsNotNone(response)
        self.assertEqual(len(response.results), page_size)
        page2_titles = {r.title for r in response.results}

        # ... and titles for page 2 should not overlap page 1 except for one or
        # two titles that could be bumped onto the next page between the time
        # the first and second calls are made.
        self.assertLessEqual(len(page1_titles.intersection(page2_titles)), 2)

        # Now make sure sort orders work.
        response = Node.get_series_list(
            broadcaster_id=self.broadcaster_id, page=1, page_size=page_size, sort_by=SeriesSortOrder.LAST_UPDATED
        )
        last_updated = None
        for r in response.results:
            if last_updated is not None:
                self.assertLessEqual(r.updated, last_updated)
            last_updated = r.updated

        last_count = None
        response = Node.get_series_list(
            broadcaster_id=self.broadcaster_id,
            page=1,
            page_size=page_size,
            sort_by=SeriesSortOrder.SERMON_COUNT_HIGHEST,
        )
        for r in response.results:
            if last_count is not None:
                self.assertGreaterEqual(last_count, r.count)
            last_count = r.count

    def test_series_list_filters(self):
        """Tests that filters work.

        This test is half-baked, but better than nothing. We do not know
        if any series are even flagged as podcasts. But at least we
        prove that we can make the call properly with a filter
        specified, and that if we do get results, they are sane.
        """

        page_size = 10

        response = Node.get_series_list(
            broadcaster_id=self.broadcaster_id, page=1, page_size=page_size, filter_by=SeriesFilter.PODCAST_ENABLED
        )
        self.assertIsNotNone(response)
        flags = {r.podcast_enabled for r in response.results}

        # All items in the response should have the podcast flag set to True.
        assert all(f for f in flags)

        response = Node.get_series_list(
            broadcaster_id=self.broadcaster_id, page=1, page_size=page_size, filter_by=SeriesFilter.PODCAST_DISABLED
        )
        self.assertIsNotNone(response)
        flags = {r.podcast_enabled for r in response.results}

        # All items in the response should have the podcast flag set to
        # False. Since Python doesn't have notall() we have to reverse the
        # logic to say we want it to be true that all flags are false.
        assert all(not f for f in flags)


class MiscTests(APITestCase):
    def test_single_speaker(self):
        response = Node.get_speaker("Dr. Alan Cairns")  # valid
        self.assertIsNotNone(response)
        self.assertEqual(response.display_name, "Dr. Alan Cairns")

        response = Node.get_speaker("Rev Allan Murray")  # valid
        self.assertIsNotNone(response)
        self.assertEqual(response.display_name, "Rev Allan Murray")

        response = Node.get_speaker("Allan Murray")  # not SA speaker name
        self.assertIsNone(response)

        response = Node.get_speaker("Mister Mxyzptlk")  # not real name
        self.assertIsNone(response)

    def test_speakers(self):
        response = Node.get_speakers("faith", page_size=None)

        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        self.assertNotEqual([speaker for speaker in response if speaker.display_name == "Dr. Alan Cairns"], [])

        response = Node.get_speakers("faith", page_size=20)
        unfiltered_response = Node.get_speakers(page_size=len(response) + 10)
        self.assertIsNotNone(unfiltered_response)
        self.assertGreater(len(unfiltered_response), 0)
        self.assertGreater(len(unfiltered_response), len(response))

        query_response = Node.get_speakers(query="Cairns")
        self.assertGreater(len(query_response), 0)
        self.assertNotEqual([speaker for speaker in query_response if speaker.display_name == "Dr. Alan Cairns"], [])

    def test_speakers_for_series(self):
        series_tests = (
            # tuples with (series, speaker we expect to find)
            ("Studies in Romans", "Dr. Alan Cairns"),
            # The following are commented out due to a caching issue somewhere in the current stack
            # We are removing these additional tests during the FastAPI port and may revisit in the
            # future
            # ("Studies in Job", "Dr. Michael Barrett"),
            # ("Reformation Month 2000", "Dr. Edward Panosian"),
        )

        for series_name, expected_speaker in series_tests:
            speakers = Node.get_speakers_for_series(broadcaster_id="faith", series_name=series_name)
            self.assertTrue(expected_speaker in [sp.display_name for sp in speakers])

    def test_webcasts_in_progress(self):
        response = Node.get_webcasts_in_progress()

        # Sadly we can't do a lot more here since webcasts aren't running 24/7
        self.assertIsNotNone(response)

    def test_spurgeon_devotional(self):
        kind = models.SpurgeonDevotionalType.AM
        month = 5
        day = 21
        response = Node.get_spurgeon_devotional(kind, month, day)

        self.assertIsNotNone(response)
        self.assertEqual(response.type, kind)
        self.assertEqual(response.month, month)
        self.assertEqual(response.day, day)
        self.assertEqual(response.audio.broadcaster.broadcaster_id, "pop")  # pop = prince of preachers

        self.assertRaises(NodeAPIError, Node.get_spurgeon_devotional, models.SpurgeonDevotionalType.AM, 7, 32)

    def test_get_filter_options(self):
        broadcaster_id = "faith"
        response = Node.get_filter_options(broadcaster_id)

        self.assertIsNotNone(response)

        # Faith should have some stuff ;)
        self.assertGreater(len(response.books), 0)
        self.assertGreater(len(response.series), 0)
        self.assertGreater(len(response.languages), 0)
        self.assertGreater(len(response.sermon_counts_for_speakers), 0)
        self.assertGreater(len(response.sermon_event_types), 0)
        self.assertGreater(len(response.speakers), 0)
        self.assertGreater(len(response.years), 0)

        # Series is the only one with uniquely identifying data we can assert
        for series in response.series:
            self.assertEqual(series.broadcaster_id, broadcaster_id)

    def test_get_filter_options_localized(self):
        """Tests we get different localized strings for another language."""
        response = Node.get_filter_options("faith", preferred_language_override="ko")
        for b in response.books:
            self.assertNotEqual(b.name, b.display_name)

    def test_get_all_languages(self):
        response = Node.get_all_languages()

        self.assertGreater(len(response), 0)

    def test_get_all_sermon_event_types(self):
        response = Node.get_all_sermon_event_types()

        self.assertGreater(len(response), 0)

    def test_highlighted_sermon(self):
        response = Node.get_highlighted_sermons(broadcaster_id="faith")

        # Not much we can assert about the results, other than we got a result,
        # because we don't know what we are getting back.
        self.assertIsNotNone(response)
        self.assertEqual(response.audio_sermon.broadcaster.broadcaster_id, "faith")

    def test_highlighted_sermon_sort_order_clips(self):
        response = Node.get_sermons(broadcaster_id="faith", sort_by=models.HighlightedSortOrders.NEWEST_CLIPS)

        self.assertIsNotNone(response)

        for sermon in response.results:
            self.assertEqual(sermon.event_type, models.SermonEventType.SERMON_CLIP)

    def test_highlighted_sermon_sort_order_preached(self):
        response = Node.get_sermons(broadcaster_id="faith", sort_by=models.HighlightedSortOrders.PREACHED)

        self.assertIsNotNone(response)
        self.assertTrue(order_is_preach_date_descending(response.results))

    def test_highlighted_sermon_sort_order_popular(self):
        response = Node.get_sermons(broadcaster_id="faith", sort_by=models.HighlightedSortOrders.POPULAR)

        self.assertIsNotNone(response)
        self.assertTrue(order_is_download_count_descending(response.results))
