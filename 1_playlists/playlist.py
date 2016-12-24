#! /usr/bin/python

import argparse
import plistlib


# Helper class to format arguments for the command line
# From here:
#    http://stackoverflow.com/a/22157136
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


def findDuplicates(filename):
    """
    Find duplicate tracks
    """
    try:
        # read the playlist file
        playlist = plistlib.readPlist(filename)

        print('Finding duplicate tracks in %s...' % filename)
        # Create a dictionary to keep track of duplicates
        track_names = {}

        # Get the tracks from the dictionary
        tracks = playlist['Tracks']

        # Iterate through the Tracks dictionary
        for trackId, track in tracks.items():
            try:

                # retrieve the name and duration of each track
                name = track['Name']
                duration = track['Total Time']

                # Does the track already exist in our dictionary?
                if name in track_names:
                    if duration//100 == track_names[name][0]//1000:
                        # increment the duplicates count
                        count = track_names[name][1]
                        track_names[name] = (duration, count + 1)

                    else:
                        # add a new dictionary entry
                        track_names[name] = (duration, 1)

            except:
                # Don't raise any exception, just go on
                pass

            dups = []

            for k, v in track_names.items():
                if v[1] > 1:
                    dups.append((v[1], k))

                    # save the duplicates list to a file
                    if len(dups) > 0:
                        print("Found %d duplicates")
                        print("Track names and counts saved to dups.txt" % len(dups))
                        # write to file
                        f = open("dups.txt", "w")
                        for val in dups:
                            f.write("[%d] %s\n" % (val[0], val[1]))
                            f.close()
                        else:
                            print("No duplicates found! No output file has been created.")
    except:
        print "Something went wrong. Did you specify the correct filename?"


def findCommonTracks(filenames):
    """
    This function finds common tracks across playlists
    """
    # a list containing sets of track names
    trackname_sets = []

    # traverse through the filenames to extract a list of track names in each
    for filename in filenames:
        # init a new set of names
        tracknames_in_file = set()

        # read the playlist
        playlist = plistlib.readPlist(filename)
        # extract the tracks from the playlist
        tracks_in_playlist = playlist['Tracks']

        # Iterate through the tracks
        for track_id, track in tracks_in_playlist.items():
            try:
                tracknames_in_file.add(track['Name'])
            except:
                pass  # ignore

        # add all collected track names to the list
        trackname_sets.append(tracknames_in_file)

    # extract the set of common tracks using set intersection
    common_tracks = set.intersection(*trackname_sets)

    # write the common tracks to file, if we find any
    if len(common_tracks) > 0:
        to_file = open("common_tracks.txt", "w")

        for track in common_tracks:
            track_info = "%s\n" % track
            to_file.write(track_info.encode("UTF-8"))

        to_file.close()

        print "%d tracks written to common_tracks.txt" % len(common_tracks)
    else:
        print "Couldn't find any common tracks. No file written."


# command line handler
def main():
    descr = """
    This program analyzes playlist files (.xml) exported from iTunes
    """
    f = SmartFormatter
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=f)

    # Add argument parser groups
    cli_group = parser.add_mutually_exclusive_group()

    # expected arguments within the group
    cli_group.add_argument('-d',
                           '--dup',
                           dest='filename',
                           required=False,
                           help="extract names of duplicate tracks")

    cli_group.add_argument('-c',
                           '--common',
                           required=False,
                           dest='filenames',
                           nargs = 2,
                           help="extract common tracks from multiple files")

    # parse the provided arguments
    args = parser.parse_args()

    if vars(args).get('filename'):
        findDuplicates(args.filename)

    if vars(args).get('filenames'):
        findCommonTracks(args.filenames)


# main method
if __name__ == "__main__":
    main()
