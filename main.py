import argparse
from BackGroundColorChanger.background_color_changer import check_svg_directory


def main():
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

    check_svg_directory(args.dir_path_in, args.fontsize, args.color)


if __name__ == "__main__":
    main()
