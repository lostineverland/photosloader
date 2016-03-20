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

class mediaStruct(object):
    """the data structure for the media being operated on"""
    def __init__(self, media={}, counter=None, source=''):
        if counter:
            self.counter = counter
        else:
            self.counter = sum(map(len, media.values()))
        self.media = media
        self.source = source

    def add_media(fullpath):
        self.counter += 1
        if self.counter % 1000 == 0:
            print "{0} files scanned".format(self.counter)
        hash = hash_file(fullpath)
        self.media.setdefault(hash, []).append(fullpath)

    @classmethod
    def load(cls, input_file):
        with open(input_file) as f:
            data = json.loads(f.read())
        return cls(data['media'], data['counter'], source=input_file)

    def save(self, output_file):
        if output_file[-5:].lower() != '.json':
            output_file += '.json'
        with open(output_file, 'w') as f:
            f.write(json.dumps({
                'counter': self.counter,
                'media': self.media
                }))
        self.source = output_file

    def merge(self, b):
        counter = self.counter + b.counter
        media = {}
        photos = self.media.items() + b.media.items()
        combine = lambda (key, val): media.setdefault(key, []).append(val)
        map(combine, photos)
        return mediaStruct(media, counter)

    def duplicates(self):
        hasDup = lambda val: len(val) > 1
        dups = toolz.valfilter(hasDup, self.media)
        return mediaStruct(dups)

    def delete_all(self):
        if raw_input('are you sure? (y/n) ') == 'y':
            files = toolz.concatv(self.media.values())
            for i in files:
                os.remove(i)
                print 'deleted:', i

    def __sub__(self, B):
        a = set(self.media.keys())
        b = set(B.media.keys())
        keys = a - b
        media = toolz.keyfilter(lambda key: key in keys, self.media)
        return mediaStruct(media)

    def _make_links(self, dest_path, i, paths):
        'create hard links in dest_path with all the contents, for easy comparison'
        dest = '{0}/{1}'.format(dest_path, i)
        for j, path in enumerate(paths):
            os.link(path, '{0}_img_{1}.{2}'.format(dest, j, path[-3:]))

    def explore_media(self):
        if self.source:
            dest = self.source[:-4] + 'files'
            os.mkdir(dest)
            for i, paths in enumerate(data.media.values()):
                make_links(dest, i, paths)
        else:
            print 'you must save before exploring this media\n'

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

    image_scan = mediaStruct()
    for media in file_list:
        image_scan.add_media(media)
    image_scan.save(args.output_file)

if __name__ == '__main__':
    main()

