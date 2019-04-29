from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import warnings
import re
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu

# Session
fingerprint_drop = './fingerprint_drop/'
file_extension = '.mp3'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ############ Access Dejavu Database ##############
    os.system('cls||clear')
    config_path = os.path.abspath(os.path.join("../config.json"))
    config = json.load(open(config_path))
    database_query = (
                        "mysql+mysqlconnector://"
                        + str(config["database_username"])
                        + ":"
                        + str(config["database_password"])
                        + "@"\
                        + str(config["database_address"])
                        + "/"\
                        + str(config["database_name"])
                    )    
    dburl = os.getenv('DATABASE_URL', database_query)
    djv = Dejavu(dburl=dburl)


    ############ Build List of Audio to Fingerprint ##############
    print ("\n\nPlace all files to be added to fingerprint database into the ./dejavu/fingerprint_drop folder")
    print ("\n\nWARNING: This is a long process depending on processor speed and size of file(s). Be prepared for long wait periods.")
    selection = input("\nHit 'Enter' to find available file(s)...")

    folder_contents = ' '.join( os.listdir(fingerprint_drop) )      # Write all files in ./fingerprint_drop as string folder_contents
    pattern_regex = re.compile(r'\w+\.mp3')                         # Future: adapt .mp3 to other supportable file types.
    audio_files_list = pattern_regex.findall(folder_contents)       # Generate a list from the string with regex value

    print ("\n\nFound the following file(s) to attempt to fingerprint: ")
    print (audio_files_list)
    selection = input("\nHit 'Enter' to process audio file(s)...")

    ############ Fingerprint Audio Files ##############
    completed = []
    incomplete = []

    for audio_file in audio_files_list:
        songname, extension = os.path.splitext(os.path.basename(audio_file))
        input_file = fingerprint_drop + audio_file

        #try:
        djv.fingerprint_with_duration_check(input_file, song_name=songname)
        print ("\nFingerprinting Complete for " + str(audio_file))
        completed.append(audio_file)
        #except:
        #    print ("\nFingerprinting Failed for " + str(audio_file))
        #    incomplete.append(audio_file)

    print ("\n\nThe following files were successful and can be removed from the fingerprint_drop folder:")
    print (completed)
    print ("\n\nThe following files failed to fingerprint:")
    print (incomplete)
