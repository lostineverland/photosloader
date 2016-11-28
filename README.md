
### TLDR;

The provided scripts:

* Identify simple duplicates
* Load images into Mac Photos.app
    - the photos must not be identified as duplicates by Photos.app (hence the dedupe step)
    - the photos are loaded in smaller, directory based, groups such that Photos.app doesn't hang on a large photo library

# Taming My Photos

Photos and video have been the bane of my existence for the past few years. Once my kids were born, the gerth of the family photo library became quickly unmanegable. The early versions of iPhoto & Picasa were easily troubled once the library became big enough. This forced me to create multiple libraries in an effort to make it manageable, however, duplicates became a growing problem. At some point, one of those libraries became unusable and it was a death spiral after that. 

By the time iPhoto caught up with handling larger libraries, it would not load the entire library. This meant that I needed to break things into smaller more digestible chunks. This, of course, leads to a scripting solution, begging for applescript, which I never bothered to learn (it's just an awkward language).

The first task of course is to gather all the photos from all the sources and dedup them. This is a painful process, and while there are many software solutions out there, none of them are great. If a photo has been rotated, it can be missed as a duplicate, but it's usually better to err on the side of caution. I spent some money on a few solutions (I even considered using Amazon's mechanical turk). I won't mention any of the ones I used, they were all useless, they all broke down on the simplest of comparisons.

## Duplicates
The use of a deduper was a necessity because applescript has a very limited support for events. That is, I could've used the Photos feature which queries you to omit importing duplicates, but I could not script this behavior. One can script omitting this check, which defeats the purpose. Better support of events would allow a program to react to such a prompt, then it could react using "System Events", but no such luck. But to be perfectly honest, this is actually simpler. I would've enjoyed diving into a more elegant and all-encompassing solution, but the complexity level rises. And this is a, hopefully, one-time problem. So instead, we dedupe, with the help of the script, prior to any import.

So I decided to write my own deduper. This wasn't a difficult problem, at this point I really only care to get rid of the photos that caused the automated process to hang, meaning I wasn't too picky. The approach was simple, use a hash funciton on each file and compare the files. Literally 27 lines of code (find_duplicates.py), python is great!

I proceeded to make a more full-featured module/script for handling and manipulating the image data, so that multiple sources could be compared and deduped.

### Example

Considering 3 sources of media

* src1
* src2
* src3

#### Scan the images:

```shell
$ python scan_media src1 -o src1.json
$ python scan_media src2 -o src2.json
$ python scan_media src3 -o src3.json
```

This will create the fingerprints for the images. For many cases this can be a lenghty process, in my case it took multiple hours to scan 400 GB worth of images and videos. So I opted to run in the background.

```shell
$ nohup python scan_media src1 -o src1.json > src1.out 2>&1 &
$ nohup python scan_media src2 -o src2.json > src2.out 2>&1 &
$ nohup python scan_media src3 -o src3.json > src3.out 2>&1 &
```

The std output produced gives some feedback on what it found:

```
878 total files
file types not imported Counter({'jpeg': 14})
```

For the case above, it did not reconized the file type `jpeg`, so I added it as an entry to `media_types` in the `scan_media.py` script.

#### Analyze the contents

```python
>>> import scan_media as scan
>>> src1 = scan.mediaStruct.load('src1.json')
>>> src2 = scan.mediaStruct.load('src2.json')
>>> src3 = scan.mediaStruct.load('src3.json')
```

##### Examine duplicates within a source:

```python
>>> dupes1 = src1.duplicates()
>>> dupes1.counter
0
>>> dupes2 = src2.duplicates()
>>> dupes2.counter
0
>>> dupes3 = src3.duplicates()
>>> dupes3.counter
4
```

It is clear that src3 has 4 duplicates which need to be addressed. You can see which files are duplicates with a simple pprint:

```python
>>> from pprint import pprint
>>> pprint(dupes3.media)
{
    u'004ca173daa1e9835007da78b52153c2b89dea429a3090f0c59169bd7834f547e30bbf8c':[
            u'path_to_image_0/duplicate_0/IMG_1697.JPG',
            u'path_to_image_0/duplicate_1/IMG_1819.JPG'],
    u'8c9fca790b060681f185485a3be9c7896f87ed1938b1835771bd0e4eafef4eec00fa0d9f': [
            u'path_to_image_1/duplicate_0/IMG_0992.JPG',
            u'path_to_image_1/duplicate_1/IMG_1005.JPG']
}
```

The print out is a dict where the key is the hash which identifies the image, and the value is the list of images that are identified as identical. At this point it is up to you to decide which one is valid, delete or remove the duplicates and re-scan src3.

To make the evaluation easier, there's an `explore_media` method whih will generate sym-links (or hard links) of the file for easy access to all the duplicates.

```python
>>> dupes3.save('duplicates_of_src3.json')
>>> dupes3.explore_media(symlink=False)
```

This creates a directory called `duplicates_of_src3.files` with hard links to the files. The names of the files are `i_img_j.jpg`, where `i` is the image index, and `j` is the duplicate index (the extension will remain consitent with the media type). The save creates the same kind of data file that is created by the scan. 

Once `src3` has been cleaned of duplicates, re-scan it.

```shell
$ python scan_media src3 -o src3.json
```

And re-load

```python
>>> import scan_media as scan
>>> src1 = scan.mediaStruct.load('src1.json')
>>> src2 = scan.mediaStruct.load('src2.json')
>>> src3 = scan.mediaStruct.load('src3.json')
```

##### Examine duplicates between sources

```python
>>> src1_2 = src1 + src2
>>> dupes1_2 = src1_2.duplicates()
>>> dupes1_2.counter
1756
```

This means that in the collection of `src1` and `src2` there are 1756 files which were flagged as duplicates. 

Now let's look at the unique ones. To see if there is any media in `src1` which is not present in `src2`:

```python
>>> diff1 = src1 - src2
>>> diff1.counter
0
```

This means that everything (every media type) in `src1` is also present in `src2`. But the opposite is not true:


```python
>>> diff2 = src2 - src1
>>> diff2.counter
81
```

This means that there are 81 files in `src2` which are missing from `src1`

A bit more exploration of the groups.

```python
>>> src1.counter
878
>>> src2.counter
959
>>> (src1 + src2).counter
1837
>>> (src1 + src2).duplicates().counter
1756
>>> (src1 + src2).unique
959

```

The differene between `counter` and `unique` is just at it seems. One is the number of items in the group, and the latter is the number of unique items in the group.

##### Handling duplicates between sources

From the examples above `src1` is a subset of `src2`, what about src3?

```python
>>> src2.counter
959
>>> src3.counter
9704
>>> (src2 - src3).counter
909
>>> (src3 - src2).counter
9652
>>> (src2 + src3).duplicates().counter
100
>>> src2.intersection(src3).counter
50
```

The last statement shows the intersection of the 2 sets. But there's a difference beteen these statements:

```python
src2.intersection(src3).counter
src3.intersection(src2).counter
```

The first returns the set from `src2` and the second from `src3`. Let's say that you've decided that `src2` is more valid, or has higher priority, than `src3`. Then we could get rid of the duplicates from `src3` as follow:

```python
>>> src3_dupes = src3.intersection(src2)
>>> src3_dupes.counter
50
>>> src3_dupes.delete_all()
are you sure? (y/n) y
deleted: path_to_image_0/IMG_1613.JPG
deleted: path_to_image_1/IMG_1632.JPG
deleted: path_to_image_2/IMG_2210.JPG
deleted: path_to_image_3/IMG_1606.JPG
.
.
.
```

That command now means that `src3` is out of sync with the contents on the filesystem, thus we would have to re-scan `src3`. We could also use the knowledge of `src3_dupes` to update `src3`:

```python
>>> src3_updated = src3 - src3_dupes
>>> src3_updated.save(src3.source)
>>> src3 = src3_updated
```

The save command stores a JSON with the same structure as the original media scan, in this case it overwrites the contents of the src3 scan (it accomplishes the same thing as a re-scan).


##### Collecting the results

We now have a collection from `src2` & `src3` whic is ready to be loaded. So let's create the final collection.

```python
>>> all_photos = src2 + src3
>>> all_photos.save('all_photos')
```

## Import into Photos.app
### Export The Folder Names

Now that the photo library is free of duplicates, write the file paths so that the applescript loader can import them to the Photos.app.

```python
all_photos.export_paths('path_list.txt')
```

### Run Loader

The `path_list.txt` is hard-coded on the script (I know, lame). So you must edit the path to the file. Then let it run for hours on end.

```shell
$ ./importPhotos.applescript
```

### Cleanup

You now have a collection of JSON files which you may want to get rid of. If you ran the original scan with a `nohup` you'll also have some `*.out` files to get rid of.

Additionally if you made use of the `explore_media` method, you'll want to get rid of the `*.files` directory, especially if you used hard links because the `delete_all` method won't get rid of these files.