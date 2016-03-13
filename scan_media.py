import os, sys, hashlib, json, toolz
import argparse

media_types = [
    'jpg',
    'png',
    'avi',
    'mp4',
    'mov',
    'mpg',
    'tiff',
    'tif',
    'cr2',
    'bmp',
]

def hash_file(path):
    with open(path) as f:
        ss = f.read()
        sha1 = hashlib.sha1(ss).hexdigest()
        md5 = hashlib.md5(ss).hexdigest()
    return sha1 + md5

def add_media(mem, fullpath):
    mem['counter'] += 1
    if mem['counter'] % 1000 == 0:
        print "{0} files scanned".format(mem['counter'])
    hash = hash_file(fullpath)
    mem.setdefault(hash, []).append(fullpath)
    return mem

def parse_cli():
    parser = argparse.ArgumentParser(usage="usage: %(prog)s")
    parser.add_argument(dest="base_path", default="./", help="The root path for searcing")
    parser.add_argument('-o', '--output-file', dest="file_name", default="image_scan.json", help="file name for the hashing results")
    args = parser.parse_args()
    return args

def main():
    args = parse_cli()
    isMedia = lambda x: x[-3:].lower() in media_types
    buildFullPath = toolz.curry(lambda path, file: '/'.join([path, file]) if isMedia(file) else None)
    iterFiles = lambda (path, dirs, files): map(buildFullPath(path), files)
    file_list = filter(None, toolz.mapcat(iterFiles, os.walk(args.base_path)))
    print '{0} total files'.format(len(file_list))

    image_scan = reduce(add_media, file_list, {'counter': 0})
    with open(args.file_name, 'w') as f:
        f.write(json.dumps(image_scan))

if __name__ == '__main__':
    main()

