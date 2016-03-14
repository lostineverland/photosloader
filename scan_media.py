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
    mem['media'].setdefault(hash, []).append(fullpath)
    return mem

def load(input_file):
    with open(input_file) as f:
        data = json.loads(f.read())
    return data

def save(data, output_file):
    with open(output_file, 'w') as f:
        f.write(json.dumps(data))

def merge(a, b):
    c = {'counter': a['counter'] + b['counter']}
    photos = filter(lambda (key, val): key != counter, a.items() + b.items())
    combine = lambda (key, val): c.setdefault(key, []).append(val)
    map(combine, photos)
    return c

def duplicates(data):
    hasDup = lambda val: len(val) > 1
    dups = toolz.valfilter(hasDup, data['media'])
    return {'counter': sum(map(len, dups.values())), 'media': dups}

def make_links(dest_path, i, paths):
    'create hard links in dest_path with all the contents, for easy comparison'
    dest = '{0}/{1}'.format(dest_path, i)
    map(lambda (j, path): os.link(path, '{0}_img_{1}.{2}'.format(dest, j, path[-3:])), enumerate(paths))
    with open('{0}/files.txt'.format(dest_path), 'a') as f:
        f.write('\n'.join(paths) + '\n')

def explore_media(data, dest):
    os.mkdir(dest)
    for i, paths in enumerate(data['media'].values()):
        make_links(dest, i, paths)


def parse_cli():
    parser = argparse.ArgumentParser(usage="usage: %(prog)s")
    parser.add_argument(dest="base_path", default="./", help="The root path for searcing")
    parser.add_argument('-o', '--output-file', dest="output_file", default="image_scan.json", help="file name for the hashing results")
    parser.add_argument('-i', '--input-file', dest="input_file", default=None, help="file name for the hashing results")
    args = parser.parse_args()
    return args

def main():
    args = parse_cli()
    isMedia = lambda x: x[-3:].lower() in media_types
    buildFullPath = toolz.curry(lambda path, file: '/'.join([path, file]) if isMedia(file) else None)
    iterFiles = lambda (path, dirs, files): map(buildFullPath(path), files)
    file_list = filter(None, toolz.mapcat(iterFiles, os.walk(args.base_path)))
    print '{0} total files'.format(len(file_list))

    image_scan = reduce(add_media, file_list, {'counter': 0, 'media': {}})
    save(image_scan, args.output_file)

if __name__ == '__main__':
    main()

