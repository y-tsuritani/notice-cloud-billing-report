import os
import datetime

import requests
import flask.Request
from google.cloud import storage


def generate_dashboard_pdf(request: flask.Request) -> str:
    """
    Generates a PDF of a Looker dashboard and uploads it to Google Cloud Storage.

    Args:
        request (flask.Request): The request object.

    Returns:
        str: The response text.
    """

    # Looker APIのエンドポイントを設定する
    looker_api_endpoint = "https://your-looker-instance.com:19999/api/3.1"

    # ダッシュボードのIDを設定する
    dashboard_id = "123"

    # PDFを生成するためのLooker APIのエンドポイントを設定する
    pdf_url = f"{looker_api_endpoint}/dashboards/{dashboard_id}/pdf"

    # pdfを保存するバケット名を設定する
    bucket_name = "your-bucket-name"
    # 保存日時の文字列を接頭辞にもつpdfを保存するファイル名を設定する（yyyymmddhhmmss-dashboard.pdf）
    destination_blob_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-dashboard.pdf"

    # PDFを生成するためのHTTPリクエストを送信する
    response = requests.get(
        pdf_url,
        auth=(credentials._service_account_email, credentials._service_account_key),
    )

    # レスポンスからPDFファイルを取得する
    pdf_data = response.content

    # PDFファイルを一時的にローカルファイルに保存する
    with open("/tmp/dashboard.pdf", "wb") as f:
        f.write(pdf_data)

    # Google Cloud Storageにアップロードする
    gcs_client = storage.Client()
    bucket = gcs_client.bucket("your-bucket-name")
    blob = bucket.blob("dashboard.pdf")
    blob.upload_from_filename("/tmp/dashboard.pdf")

    # 一時的に保存したPDFファイルを削除する
    os.remove("/tmp/dashboard.pdf")


def upload_file_to_gcs(
    gcs_client: file_path: str, bucket_name: str, destination_blob_name: str
) -> None:
    """
    Uploads a file to Google Cloud Storage.

    Args:
        file_path (str): The path to the file to upload.
        bucket_name (str): The name of the bucket to upload the file to.
        destination_blob_name (str): The name to give the uploaded file in the bucket.

    Returns:
        None
    """

    # Google Cloud Storageにアップロードする
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
