import boto3
import os


class S3Interface:
    def __init__(self, client: boto3.client, bucket_name: str, folder_name: str):
        # クライアントとバケット名の情報を初期化
        self.client = client
        self.bucket_name = bucket_name
        self.folder_name = folder_name

    def upload_svg_to_s3(self, svg_file_path):
        """
        処理されたsvgファイルをS3バケットにアップロードします。
        :param svg_file_path: アップロードするSVGファイルのパス
        """
        try:
            # ファイルパスからキーを生成
            object_key = os.path.relpath(svg_file_path)
            object_key = object_key.replace("\\", "/")
            object_key = self.folder_name + "/" + object_key
            # SVGファイルをアップロード

            self.client.upload_file(
                svg_file_path, Bucket=self.bucket_name, Key=object_key
            )

            print(
                f"SVG file uploaded to S3 bucket '{self.bucket_name}' with key '{object_key}'"
            )
        except Exception as e:
            print(f"Error uploading SVG file to S3: {str(e)}")
