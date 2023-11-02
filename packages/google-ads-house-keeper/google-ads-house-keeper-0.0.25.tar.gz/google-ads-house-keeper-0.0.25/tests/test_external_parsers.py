from unittest import mock
import pytest
import requests
from googleads_housekeeper.services.external_parsers import website_parser
from googleads_housekeeper.services.external_parsers import youtube_data_parser


class TestWebSiteParser:

    @pytest.mark.parametrize("input_url,formatted_url",
                             [("example.com", "https://example.com"),
                              ("http://example.com", "http://example.com"),
                              ("https://example.com", "https://example.com")])
    def test_convert_url(self, input_url, formatted_url):
        url = website_parser.WebSiteParser()._convert_placement_to_url(
            input_url)
        assert url == formatted_url

    @pytest.mark.parametrize("attribute,expected_value",
                             [("is_processed", True),
                              ("title", "example title"),
                              ("description", "example description"),
                              ("keywords", "example keywords")])
    def test_parse_website_success(self, mocker, attribute, expected_value):
        mocker.patch(
            "googleads_housekeeper.services.external_parsers.website_parser.WebSiteParser.parse",
            return_value=website_parser.WebsiteInfo(
                placement="example.com",
                title="example title",
                description="example description",
                keywords="example keywords",
                is_processed=True))

        parser = website_parser.WebSiteParser()
        website_info = parser.parse("example.com")
        assert getattr(website_info, attribute) == expected_value
        parser.parse.assert_called_once_with("example.com")

    @pytest.mark.parametrize("attribute,expected_value",
                             [("is_processed", False), ("title", ""),
                              ("description", ""), ("keywords", "")])
    def test_parse_website_raise_error_empty_result(self, mocker, attribute,
                                                    expected_value):
        mocker.patch("requests.get",
                     side_effect=requests.exceptions.ConnectionError)
        website_info = website_parser.WebSiteParser().parse("non-example")
        assert getattr(website_info, attribute) == expected_value


class TestYouTubeChannelParser:

    @pytest.mark.parametrize("attribute,expected_value",
                             [("title", "example title"),
                              ("description", "example description"),
                              ("country", "US"), ("subscriberCount", 1),
                              ("videoCount", 1),
                              ("topicCategories", ("Film", "Game")),
                              ("country", "US"), ("viewCount", 10)])
    def test_parse_youtube_channel_success(self, mocker, attribute,
                                           expected_value):
        mocker.patch(
            "googleads_housekeeper.services.external_parsers.youtube_data_parser.ChannelInfoParser.parse",
            return_value=youtube_data_parser.ChannelInfo(
                placement="example_channel_id",
                title="example title",
                description="example description",
                country="US",
                subscriberCount=1,
                videoCount=1,
                viewCount=10,
                topicCategories=("Film", "Game")))

        parser = youtube_data_parser.ChannelInfoParser()
        channel_info = parser.parse("example_channel_id")
        assert getattr(channel_info, attribute) == expected_value
        parser.parse.assert_called_once_with("example_channel_id")


class TestYouTubeVideoParser:

    @pytest.mark.parametrize("attribute,expected_value",
                             [("title", "example title"),
                              ("description", "example description"),
                              ("defaultAudioLanguage", "EN"),
                              ("defaultLanguage", "EN"), ("likeCount", 10),
                              ("commentCount", 10), ("favouriteCount", 10),
                              ("topicCategories", ("Film", "Game")),
                              ("madeForKids", False),
                              ("tags", ("tag1", "tag2")), ("viewCount", 10)])
    def test_parse_youtube_video_success(self, mocker, attribute,
                                         expected_value):
        mocker.patch(
            "googleads_housekeeper.services.external_parsers.youtube_data_parser.VideoInfoParser.parse",
            return_value=youtube_data_parser.VideoInfo(
                placement="example_video_id",
                title="example title",
                description="example description",
                defaultLanguage="EN",
                defaultAudioLanguage="EN",
                viewCount=10,
                commentCount=10,
                likeCount=10,
                favouriteCount=10,
                madeForKids=False,
                tags=("tag1", "tag2"),
                topicCategories=("Film", "Game")))

        parser = youtube_data_parser.VideoInfoParser()
        video_info = parser.parse("example_video_id")
        assert getattr(video_info, attribute) == expected_value
        parser.parse.assert_called_once_with("example_video_id")
