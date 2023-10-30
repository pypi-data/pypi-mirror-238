# object_store
from datetime import datetime
import logging
import os
from pathlib import Path
from tqdm import tqdm

from mathtext.constants import DATA_DIR, OBJECT_STORAGE_PROVIDER
from mathtext.constants import CURRENT_MODEL_LINK as MODEL_KEY
from mathtext.constants import OBJECT_STORAGE_CLIENT as client
from mathtext.constants import OBJECT_STORAGE_NAME as MODEL_BUCKET


MODEL_BUCKET, MODEL_KEY = Path(MODEL_BUCKET), Path(MODEL_KEY)

log = logging.getLogger(__name__)


def get_stat(path, follow_symlinks=False):
    """Python equivalent to unix `stat` command.

    Returns dict of file/dir statistics

    SEE os.get_stat()

    Create `class Stat` like os.stat_result object but with
       - .__dict__
       - .__getitem__
       - .keys()
       - .items()
    """
    p = Path(path)
    if follow_symlinks:
        p = p.resolve()
    stat = p.stat()
    # TODO:
    # dict([(k[3:], getattr(stat, k))
    #     for k in dir(stat)
    #     if k.startswith('st_')])
    status = dict(
        size=stat.st_size,
        uid=stat.st_uid,
        gid=stat.st_gid,
        mode=stat.st_mode,
        ino=stat.st_ino,  # inode number/id
        dev=stat.st_dev,
        nlink=stat.st_nlink,
        atime=stat.st_atime,
        mtime=stat.st_mtime,
        ctime=stat.st_ctime,
    )
    # aliases:
    status.update(
        dict(
            device=status.get("dev"),
            inode=status.get("ino"),
            num_links=status.get("nlink"),
            accessed=datetime.fromtimestamp(status.get("atime")),
            modified=datetime.fromtimestamp(status.get("mtime")),
            changed_any=datetime.fromtimestamp(status.get("ctime")),
            changed=datetime.fromtimestamp(status.get("ctime")),
        )
    )
    return status


def get_obj_head(path):
    path = Path(path)
    bucket = path.parts[0]
    key = Path(*path.parts[1:])  # s3.Key

    head = {}
    try:
        head = client.head_object(
            Bucket=str(bucket),
            Key=str(key),
        )
    except Exception as e:
        log.error(
            f"Unable to retrieve headers for object:"
            + f"\n  path: {path}\n  bucket: {bucket}\n  key: {key}"
        )
        log.error(str(e))
    return head


def split_bucket_key(path, data_dir=DATA_DIR):
    path = Path(path)
    # FIXME: use path.absolute() and data_dir.absolute() rather than skipping path.root
    path_parts = path.parts[bool(path.root) :]
    data_dir = Path(data_dir)
    data_dir_parts = data_dir.parts[bool(data_dir.root) :]
    obj_parts = list(path_parts)
    for d, p in zip(data_dir_parts, path_parts):
        if d != p:
            break
        obj_parts.pop(0)
    if not obj_parts:
        raise ValueError(f"Invalid path ({path})")
    bucket = obj_parts[0]
    key = None
    if len(obj_parts) > 1:
        key = Path(*obj_parts[1:])  # s3.Key
    return bucket, key


def get_obj_size(path):
    return (get_obj_head(path) or {}).get("ContentLength")


def get_file_size(path):
    return get_stat(path)["size"]


def download_with_progressbar(
    s3_bucket, s3_object_key, dest, data_dir=DATA_DIR, s3_client=client
):
    s3_object_key = os.path.normpath(s3_object_key).replace("\\", "/")
    if OBJECT_STORAGE_PROVIDER == "gcs":
        bucket = client.bucket(s3_bucket)
        meta_data = bucket.get_blob(s3_object_key)
        blob = bucket.blob(s3_object_key)
        total_length = int(meta_data.size)
    else:
        meta_data = s3_client.head_object(Bucket=s3_bucket, Key=s3_object_key)
        total_length = int(meta_data.get("ContentLength", 0))
    with tqdm(
        total=total_length,
        desc=f"source: s3://{s3_bucket}/{s3_object_key}",
        bar_format="{percentage:.1f}%|{bar:25} | {rate_fmt} | {desc}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        with dest.open("wb") as f:
            if OBJECT_STORAGE_PROVIDER == "gcs":
                blob.download_to_filename(str(DATA_DIR / s3_bucket / s3_object_key))
            else:
                s3_client.download_fileobj(
                    s3_bucket, s3_object_key, f, Callback=pbar.update
                )


def download(source=MODEL_BUCKET / MODEL_KEY, dest=DATA_DIR, force=False):
    """Download object from an s3 bucket to a dest path within dest dir or DATA_DIR

    Inputs:
      source (Path|str): bucket / key for remote object to download
      dest (Path|str): local file path or directory path (default: DATA_DIR)
    """
    source = Path(source)
    source_size = get_obj_size(source)
    source_bucket, source_key = split_bucket_key(source)

    log.error(f"source: {source}\nsource_size: {source_size}")
    if source.is_file():
        return source
    if dest.is_dir():
        log.debug(f"isdir: {dest}")
        dest = dest / source_bucket / source_key
        log.debug(f"isfile?: {dest.is_file()} {dest}")
    if dest.is_file() and not force:
        log.debug(f"isfile: {dest}")
        stat = get_stat(dest)
        dest_size = stat["size"]
        if dest_size == source_size:
            log.warning(
                f"File exists and is the same size ({source_size}) and force={force}."
            )
            return dest
        raise FileExistsError(
            f"The dest_file ({dest}) exists\nand is not the same size\n  dest_size: {dest_size}"
            + f"\n  source_size: {source_size}\n  force={force}."
        )
    resp = download_with_progressbar(
        s3_bucket=source_bucket, s3_object_key=source_key, dest=dest, data_dir=None
    )
    log.info(str(resp))
    return dest


def download_model(
    path=MODEL_BUCKET / MODEL_KEY,
    # provider=OBJECT_STORAGE_PROVIDER,
    data_dir=DATA_DIR,
    force=False,
):
    # FIXED: never define a new path within the code
    #   Always reuse a previously defined path (DATA_DIR), preferably from constants.py
    #   And try to avoid using Path('') or Path.cwd() so that code can run anywhere
    dest_path = data_dir / path

    if not dest_path.parent.is_dir():
        log.warning(f"Creating new directory to store file {dest_path.parent}.mkdir()")
        dest_path.parent.mkdir(exist_ok=True, parents=True)
    log.debug(f"dest_path: {dest_path}")
    split_bucket_key(dest_path, data_dir=data_dir)
    if force or not dest_path.is_file() or not get_file_size(dest_path):
        download(source=path, dest=dest_path, force=force)
    return dest_path


def upload(
    source=MODEL_BUCKET / MODEL_KEY,
    dest=None,
    data_dir=None,
    force=False,
    acl="public-read",
):
    """Uploads local file to object storage (s3 bucket on GCP, AWS, or DO)
    Path(source) can be relative to DATA_DIR, CWD, or absolute file Path"""
    source = Path(source)
    if not source.root:
        data_dir = Path(data_dir or DATA_DIR)
    if not source.is_file():
        if source.root:
            raise FileNotFoundError(f"Invalid source file path: {source}")
        log.error(
            f"Invalid source file path: {source}, prepending with {MODEL_BUCKET}/"
        )
        source = Path(MODEL_BUCKET) / source

    if not source.is_file():
        log.error(f"Invalid source file path: {source}, prepending with {data_dir}/")
        source = data_dir / source
    if not source.is_file():
        raise FileNotFoundError(f"Invalid source file path: {source}")

    dest = Path(dest or source)  # .absolute()
    dest_bucket, dest_key = split_bucket_key(dest)
    log.info(f"\n  dest_bucket: {dest_bucket}\n  dest_key: {dest_key}")
    if not dest_key:
        log.warning(f"No dest filename found, dest: {dest}, dest_key: {dest_key}")

    head = get_obj_size(Path(dest_bucket) / dest_key)
    if force or not head:
        log.debug(f"Uploading to bucket: {dest_bucket}, key: {dest_key}")
        response = client.upload_file(Filename=source, Bucket=dest_bucket, Key=dest_key)
    log.info(f"client.upload_file() response: {response}")

    # acl = acl or 'private' or 'public-read'
    if acl:
        response = client.put_object_acl(ACL=acl, Bucket=dest_bucket, Key=dest_key)
    return response
