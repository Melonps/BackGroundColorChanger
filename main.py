import argparse
import os
import boto3
from dotenv import load_dotenv

from BackGroundColorChanger.S3Interface.s3_data_manipulation import S3Interface
from BackGroundColorChanger.background_color_changer import check_svg_directory


def main(args):
    load_dotenv()
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region_name = os.environ.get("AWS_DEFAULT_REGION")
    bucket_name = os.environ.get("AWS_BUCKET")
    folder_name = "ColorChangedSVG"

    client = boto3.client(
        "s3",
        endpoint_url=f"https://s3.{region_name}.wasabisys.com",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    s3_instance = S3Interface(
        client=client, bucket_name=bucket_name, folder_name=folder_name
    )
    check_svg_directory(args.dir_path_in, args.fontsize, args.color, s3_instance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process SVG files with background color based on font size."
    )
    parser.add_argument(
        "--fontsize", required=True, type=float, help="Minimum font size for processing"
    )
    parser.add_argument(
        "--color",
        type=str,
        help="Background color in hexadecimal format",
    )
    parser.add_argument(
        "--dir_path_in",
        required=True,
        nargs="?",
        default=None,
        help="Input directory path (optional)",
    )

    args = parser.parse_args()
    main(args)
