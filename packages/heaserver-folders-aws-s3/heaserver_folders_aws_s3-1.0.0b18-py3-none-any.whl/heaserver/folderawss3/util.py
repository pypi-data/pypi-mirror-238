

import logging
from uuid import uuid4
from aiohttp import hdrs, web
from heaobject.awss3key import display_name, is_folder
from heaobject.user import NONE_USER
from heaserver.service import response
from heaserver.service.aiohttp import StreamResponseFileLikeWrapper
from heaserver.service.appproperty import HEA_BACKGROUND_TASKS
from heaserver.service.db import awsservicelib
from heaserver.service.oidcclaimhdrs import SUB
from mypy_boto3_s3 import S3Client


import asyncio
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


async def response_folder_as_zip(s3_client: S3Client, request: web.Request, bucket_name: str, folder_key: str) -> web.Response:
    """
    Creates a HTTP streaming response with the contents of all S3 objects with the given prefix packaged into a ZIP
    file. S3 allows folders to have no name (just a slash), and for maximum compatibility with operating systems like
    Windows that do not, such folders are replaced in the zip file with "No name <random string>". The resulting ZIP
    files are uncompressed, but this may change in the future.

    :param s3_client: the S3Client (required).
    :param request: the HTTP request (required).
    :param bucket_name: the bucket name (required).
    :param folder_key: the folder key (required).
    :return: the HTTP response.
    """
    folder_display_name = display_name(folder_key)
    if not folder_display_name:
        folder_display_name = 'archive'

    response_ = web.StreamResponse(status=200, reason='OK',
                                               headers={hdrs.CONTENT_DISPOSITION: f'attachment; filename={folder_display_name}.zip'})
    response_.content_type = 'application/zip'
    await response_.prepare(request)

    loop = asyncio.get_running_loop()

    async with StreamResponseFileLikeWrapper(response_) as fileobj:
        with ZipFile(fileobj, mode='w', compression=ZIP_DEFLATED) as zf:
            async for obj in awsservicelib.list_objects(s3_client, bucket_name, folder_key):
                folder = obj['Key'].removeprefix(folder_key)
                if not folder:
                    continue
                filename = _fill_in_folders_with_no_name(folder)
                zinfo = ZipInfo(filename=filename, date_time=obj['LastModified'].timetuple()[:6])
                #zinfo.compress_type = ZIP_DEFLATED  # Causes downloads to hang, possibly because something gets confused about file size.
                if zinfo.is_dir():  # Zip also denotes a folders as names ending with a slash.
                    await loop.run_in_executor(None, zf.writestr, zinfo, '')
                else:
                    with zf.open(zinfo, mode='w') as dest:
                        await loop.run_in_executor(None, s3_client.download_fileobj, bucket_name, obj['Key'], dest)
    return response_

async def get_async_status(request: web.Request) -> web.Response:
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    background_tasks = request.app[HEA_BACKGROUND_TASKS]
    logger.debug('background tasks: %s', background_tasks)
    task_name = f'{sub}^{request.url}'
    if not background_tasks.contains(task_name):
        return response.status_not_found()
    if not background_tasks.done(task_name):
        return response.status_accepted()
    error = background_tasks.error(task_name)
    if error:
        background_tasks.remove(task_name)
        # In case we get an exception other than an HTTPException, raise it so it gets wrapped in an internal server
        # error response.
        raise error
    else:
        resp = background_tasks.result(task_name)
        background_tasks.remove(task_name)
        return resp


def _fill_in_folders_with_no_name(filename: str) -> str:
    """
    S3 allows folders to have no name (just a slash). This function replaces those "empty" names with a randomly
    generated name.

    :param filename: the filename.
    :return: the filename with empty names replaced.
    """
    logger = logging.getLogger(__name__)
    def split_and_rejoin(fname_: str) -> str:
        return '/'.join(part if part else f'No name {str(uuid4())}' for part in fname_.split('/'))
    if is_folder(filename):
        filename = split_and_rejoin(filename.rstrip('/')) + '/'
    else:
        filename = split_and_rejoin(filename)
    logger.debug('filename to download %s', filename)
    return filename
