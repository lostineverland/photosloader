import os, sys, hashlib, json, toolz

with open('data.json') as f:
    known_media = json.loads(f.read()).keys()

with open('unwanted_data.json') as f:
    known_media += json.loads(f.read()).keys()

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

isMedia = lambda x: x[-3:].lower() in media_types
buildFullPath = toolz.curry(lambda path, file: '/'.join([path, file]) if isMedia(file) else None)
iterFiles = lambda (path, dirs, files): map(buildFullPath(path), files)
base_path = sys.argv[1]
file_list = filter(None, toolz.mapcat(iterFiles, os.walk(base_path)))

def hash_file(path):
    with open(path) as f:
        ss = f.read()
        sha1 = hashlib.sha1(ss).hexdigest()
        md5 = hashlib.md5(ss).hexdigest()
    return sha1 + md5

def find_missing_media(mem, fullpath):
    mem['counter'] += 1
    if mem['counter'] % 1000 == 0:
        print "checking {0}  of {1} files".format(mem['counter'], len(file_list))
    hash = hash_file(fullpath)
    if hash not in known_media:
        print 'found new', fullpath
        mem.setdefault(hash, []).append(fullpath)
    return mem

missing_media = reduce(find_missing_media, file_list, {'counter': 0})

with open('missing_data.json', 'w') as f:
    f.write(json.dumps(missing_media))
