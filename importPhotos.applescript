#! /usr/bin/osascript

set file_count to 0

on to_alias(thePath)
	(*
	Converting a POSIX path to an HFS alias
	*)
	local importFolder
	log (thePath)
	set importFolder to POSIX file thePath as alias
	--log importFolder
	return importFolder
end to_alias

on import_images(theFiles)
	global file_count
	local theFiles
	log(number of items in theFiles)
	set file_count to file_count + number of items in theFiles
	set imageList to {}
	repeat with i from 1 to number of items in theFiles
		set this_item to item i of theFiles as alias
		set the end of imageList to this_item
	end repeat
	(*
	Run Photos App
	*)
	tell application "Photos"
		activate
		delay 5
		import imageList skip check duplicates no
	end tell
end import_images

set sourcePath to paragraphs of (read POSIX file "/Users/Shared/Photo Library/photoImportWorkflow/path_list.txt")
repeat with nextLine in sourcePath
    if length of nextLine is greater than 0 then
		set importFolder to to_alias(nextLine)
		tell application "Finder" to set theFiles to every file of importFolder
		import_images(theFiles)
    end if
end repeat

log ("Totla number of items added", file_count)

