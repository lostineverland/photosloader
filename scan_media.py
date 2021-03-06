import os, sys, hashlib, json, toolz
import argparse, datetime
from collections import Counter

media_types = [
    'jpg',
    'jpeg',
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

    def add_media(self, fullpath):
        self.counter += 1
        if self.counter % 1000 == 0:
            now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            print "{0}  {1} files scanned".format(now, self.counter)
        hash = hash_file(fullpath)
        self.media.setdefault(hash, []).append(fullpath)

    @classmethod
    def load(cls, input_file):
        if input_file[-5:].lower() != '.json':
            input_file += '.json'
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

    @property
    def unique(self):
        return len(self.media.keys())

    def __add__(self, B):
        counter = self.counter + B.counter
        media = {}
        photos = self.media.items() + B.media.items()
        combine = lambda (key, val): media.setdefault(key, []).extend(val)
        map(combine, photos)
        return mediaStruct(media, counter)

    def intersection(self, B):
        a = set(self.media.keys())
        b = set(B.media.keys())
        keys = a.intersection(b)
        media = toolz.keyfilter(lambda key: key in keys, self.media)
        return mediaStruct(media)

    def duplicates(self):
        hasDup = lambda val: len(val) > 1
        dups = toolz.valfilter(hasDup, self.media)
        return mediaStruct(dups)

    def delete_all(self):
        if raw_input('are you sure? (y/n) ') == 'y':
            files = toolz.concatv(*self.media.values())
            for i in files:
                os.remove(i)
                print 'deleted:', i

    def __sub__(self, B):
        a = set(self.media.keys())
        b = set(B.media.keys())
        keys = a - b
        media = toolz.keyfilter(lambda key: key in keys, self.media)
        return mediaStruct(media)

    def _make_links(self, dest_path, i, paths, symlink):
        'create hard links in dest_path with all the contents, for easy comparison'
        dest = '{0}/{1}'.format(dest_path, i)
        if symlink:
            linker = lambda src, dest: os.symlink('../' + src, dest)
        else:
            linker = os.link
        for j, path in enumerate(paths):
            linker(path, '{0}_img_{1}.{2}'.format(dest, j, path.rsplit('.', 1)[-1]))

    def explore_media(self, symlink=True):
        if self.source:
            dest = self.source[:-4] + 'files'
            os.mkdir(dest)
            for i, paths in enumerate(self.media.values()):
                self._make_links(dest, i, paths, symlink)
        else:
            print 'you must save before exploring this media\n'

    def export_paths(self, output_file):
        files = toolz.concatv(*self.media.values())
        dirs = set()
        map(lambda file: dirs.add(file.rsplit('/', 1)[0]), files)
        with open(output_file, 'w') as f:
            f.write('\n'.join(sorted(dirs)))

    def get_media_size(self):
        size_tuple = lambda (key, val): (key, os.path.getsize(val[0]) / 1024.0)
        self.media_size = dict(map(size_tuple, self.media.iteritems()))

    def pick_media(self, keys):
        white_list = lambda key: key in keys
        selected = toolz.keyfilter(white_list, self.media)
        return mediaStruct(selected)

def parse_cli():
    parser = argparse.ArgumentParser(usage="usage: %(prog)s")
    parser.add_argument(dest="base_path", default="./", help="The root path for searcing")
    parser.add_argument('-o', '--output-file', dest="output_file", default="image_scan.json", help="file name for the hashing results")
    parser.add_argument('-i', '--input-file', dest="input_file", default=None, help="file name for the hashing results")
    args = parser.parse_args()
    return args

def main():
    args = parse_cli()
    not_media = Counter()
    getType = lambda x: x.rsplit('.', 1)[-1] 
    notMedia = lambda path: not_media.update([getType(path)])
    isMedia = lambda x: getType(x).lower() in media_types
    buildFullPath = toolz.curry(lambda path, file: '/'.join([path, file]) if isMedia(file) else notMedia(file))
    iterFiles = lambda (path, dirs, files): map(buildFullPath(path), files)
    file_list = filter(None, toolz.mapcat(iterFiles, os.walk(args.base_path)))
    print '{0} total files'.format(len(file_list))

    image_scan = mediaStruct()
    for media in file_list:
        image_scan.add_media(media)
    image_scan.save(args.output_file)
    print 'file types not imported', not_media

if __name__ == '__main__':
    main()

