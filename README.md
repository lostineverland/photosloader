# Taming My Photos

Photos and video have been the bane of my existence for the past few years. Once my kids were born, the gerth of the family photo library became quickly unmanegable. The early versions of iPhoto & Picasa were easily troubled once the library became big enough. This forced me to create multiple libraries in an effort to make it manageable, however, duplicates became a growing problem. At some point, one of those libraries became unusable and it was a death spiral after that. 

By the time iPhoto caught up with handling larger libraries, it would not load the entire library. This meant that I needed to break things into smaller more digestible chunks. This, of course, leads to a scripting solution, begging for applescript, which I never bothered to learn (it's just an awkward language).

I recently went on a fantastic family vacation to Puerto Rico, and upon our return, I could no longer postpone this task. I had a mountain of photo and videos that needed some serious attention. 

As you can imagine, collecting photos and videos for more than 15 years results in a scattering of files across multiple hard drives. To add to the complexity, as the family grew, there are now more contributors each with multiple devices. Some devices get read multiple times (accidentally, I've been assured).

The first task of course is to gather all the photos from all the sources and dedup them. This is a painful process, and while there are many software solutions out there, none of them are great. If a photo has been rotated, it can be missed as a duplicate, but it's usually better to err on the side of caution. I spent some money on a few solutions (I even considered using Amazon's mechanical turk), most I won't mention, but Decloner was the best of the lot. I actually spent a really long time on this process, many weekend late nights.

Once I gathered all the goods, and filtered all the junk, it was time to import all these files into a photo manager. This time I was considering Aperture and Light Room. I especially liked the fact that these would let you organize large libraries across multiple hard drives. But after some research I realized that my 500GB did not really constitute a large photo library, and that iPhoto should handle this quantity well (at least by this point in time). However, iPhoto still choked when it came time to import the files. It would complain that a photo or video was incompatible. At this point I was thinking that my 2007 iMac is probably under powered. But the iMac was the only desktop we had, the rest are laptops with much smaller HDDs

The use of a deduper was a necessity because applescript has a very limited support for events. That is, I could've used the Photos feature which queries you to omit importing duplicates, but I could not script this behavior. One can script omitting this check, which defeats the purpose. Better support of events would allow a program to react to such a prompt, then it could react using "System Events", but no such luck. But to be perfectly honest, this is actually simpler. I would've enjoyed diving into a more elegant and all-encompassing solution, but the complexity level rises. And this is a, hopefully, one-time problem. So instead, we run a de-dupping software (again I suggest decloner) prior to any import.

# Choose The Folders

```shell
> find . -type f | grep -iv jpg$ | grep -iv png$ | grep -iv avi$ | grep -iv mp4$ | grep -iv mov$ | grep -iv mpg
> find . -type f > file_list.txt
```

# Run Loader
```shell
> nohup ./importPhotos.applescript > import.log 2>&1 &
```
# Setting Up A Shared Folder
  • Set this up as a different post
  • How to share a family photo library