#! /usr/bin/python

import argparse
import plistlib

def findDuplicates(filename):
    """
    Find duplicate tracks
    """
    print('Finding duplicate tracks in %s...' % filename)
    # Create a dictionary to keep track of duplicates
    track_names = {}

    # read the playlist file
    playlist = plistlib.readPlist(filename)

    # Get the tracks from the dictionary
    tracks = playlist['Tracks']

    # Iterate through the Tracks dictionary
    for trackId, track in tracks.items():
        try:

            # retrieve the name and duration of each track
            name = track['Name']
            duration = track['Total Time']

            # Does the track already exist in our dictionary?
            if name in track_names and duration//100 == track_names[name][0]//1000:

                # increment the duplicates count
                count = track_names[name][1]
                track_names[name] = (duration, count + 1)

            else:
                # add a new dictionary entry
                track_names[name] = (duration, 1)

        except:
            # Don't raise any exception, just go on
            pass

    # store duplicates as (name, count) tuples
    dups = []
    for k,v in track_names.items():
        if v[1] > 1:
            dups.append((v[1], k))
            
    # save the duplicates list to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names and counts saved to dups.txt" % len(dups))
        #write to file
        f = open("dups.txt","w")
        for val in dups:
            f.write("[%d] %s\n" % (val[0],val[1]))
        f.close()
    else:
        print("No duplicates found! No output file has been created.")


# command line handler
def main():
    descr = """
    This program analyzes playlist files (.xml) exported from iTunes
    """

    parser = argparse.ArgumentParser(description=descr)

    # Add argument parser groups
    cli_group = parser.add_mutually_exclusive_group()

    # expected arguments within the group
    cli_group.add_argument('--dup', required=False)
    cli_group.add_argument('--common',required=False)
    
    # parse the provided arguments
    args = parser.parse_args()

    print vars(args)

    if vars(args).get('dup'):
        findDuplicates(args.dup)
        

# main method
if __name__ == "__main__":
    main()
