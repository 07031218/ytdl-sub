import pytest
from expected_download import assert_expected_downloads
from expected_transaction_log import assert_transaction_log_matches
from mergedeep import mergedeep

from ytdl_sub.subscriptions.subscription import Subscription


@pytest.fixture
def preset_dict(output_directory):
    return {
        "preset": "music_video",
        "download": {"url": "https://www.youtube.com/watch?v=2zYF9JLHDmA"},
        "output_options": {"output_directory": output_directory},
        # download the worst format so it is fast
        "ytdl_options": {
            "postprocessor_args": {"ffmpeg": ["-bitexact"]},  # Must add this for reproducibility
        },
        "file_convert": {"convert_to": "mp4"},
    }


class TestFileConvert:
    @pytest.mark.parametrize("dry_run", [True, False])
    def test_file_convert(
        self,
        music_video_config,
        preset_dict,
        output_directory,
        dry_run,
    ):
        subscription = Subscription.from_dict(
            config=music_video_config,
            preset_name="file_convert_test",
            preset_dict=preset_dict,
        )

        transaction_log = subscription.download(dry_run=dry_run)
        assert_transaction_log_matches(
            output_directory=output_directory,
            transaction_log=transaction_log,
            transaction_log_summary_file_name="plugins/file_convert/output.txt",
        )
        assert_expected_downloads(
            output_directory=output_directory,
            dry_run=dry_run,
            expected_download_summary_file_name="plugins/file_convert/output.json",
        )

    @pytest.mark.parametrize("dry_run", [True, False])
    def test_file_convert_custom_ffmpeg(
        self,
        music_video_config,
        preset_dict,
        output_directory,
        dry_run,
    ):
        mergedeep.merge(
            preset_dict,
            {
                "file_convert": {
                    "convert_to": "mkv",
                    "convert_with": "ffmpeg",
                    "ffmpeg_post_process_args": "-bitexact -vcodec copy -acodec copy -scodec mov_text",
                }
            },
        )
        subscription = Subscription.from_dict(
            config=music_video_config,
            preset_name="file_convert_test",
            preset_dict=preset_dict,
        )

        transaction_log = subscription.download(dry_run=dry_run)
        assert_transaction_log_matches(
            output_directory=output_directory,
            transaction_log=transaction_log,
            transaction_log_summary_file_name="plugins/file_convert/output_custom_ffmpeg.txt",
        )
        assert_expected_downloads(
            output_directory=output_directory,
            dry_run=dry_run,
            expected_download_summary_file_name="plugins/file_convert/output_custom_ffmpeg.json",
        )
