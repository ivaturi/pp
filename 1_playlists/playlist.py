import plistlib

def findDuplicates(filename):
    """
    Find duplicate tracks
    """
    print('Finding duplicate tracks in %s...' % filename)
    # read the playlist file
    playlist = plistlib.readPlist(filename)
    # Create a dictionary to keep track of duplicates
    track_names = {}
    # Get the tracks from the dictionary
    tracks = plist['Tracks']
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
