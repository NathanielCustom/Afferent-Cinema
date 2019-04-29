import json
import time
import os

from dejavu import Dejavu
from dejavu.recognize import MicrophoneRecognizer


if __name__ == '__main__':
    ############ Access Dejavu Database ##############
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

    
    ############ Run Through Audio Related Warnings and Clear Screen ##############
    void = djv.recognize(MicrophoneRecognizer, 0.01)    
    os.system('clear')
   
        
    ############ Audio Recognition Test ##############    
    print ("\n\nMicrophone Test:")
    print ("Ensure you microphone is configured. Help can be found in the readme document for Afferent Cinema")

    timestamp_current = 0
    timestamp_previous = 0
    time_start = time.time()
    id_specific = None


    while True:
        print ("\nTimestamp: " + str(time.time() - time_start))

        time_recognize_start = time.time()
        try:
            movie = djv.recognize(MicrophoneRecognizer, 3)
        except:
            print ("Dejavu Failed...")
            movie = None

        processing_time = time.time() - time_recognize_start # Amount of time it took to process the audio sample; compensates.
        print ("Process Time: " + str(processing_time))
        
        if movie is None:
            print ("\nNothing Recognized")
        else:
            print ("\n%s recognized" % (movie["song_name"]))
            print ("Confidence: " + str(movie["confidence"]))

            ## ID stored if confident enough and not already identified ##
            if ( movie['confidence'] > 5 ) and id_specific == None:
                id_specific = movie['song_id']
                print ("Movie ID'd as " + str(movie['song_name']))
                timestamp_current = movie["offset_seconds"] + processing_time
                prev_timestamp = time.time() - time_start
                m, s = divmod(timestamp_current, 60)
                h, m = divmod(m, 60)
                print ("Current Movie Time adjusted to %d (%d:%d:%d) from %d (Changed: %d)" % (timestamp_current, h, m, s, prev_timestamp, (timestamp_current-prev_timestamp)))
                time_start = time.time() - timestamp_current
            
            ## Recalculate Current Marker Time; Greater Confidence expected to change time. ##
            elif movie['confidence'] > 10:
                timestamp_current = movie["offset_seconds"] + processing_time
                prev_timestamp = time.time() - time_start
                m, s = divmod(timestamp_current, 60)
                h, m = divmod(m, 60)
                print ("Current Movie Time adjusted to %d (%d:%d:%d) from %d (Changed: %d)" % (timestamp_current, h, m, s, prev_timestamp, (timestamp_current-prev_timestamp)))
                time_start = time.time() - timestamp_current
            
            ## Not enough Confidence to Adjust Time.
            else:
                print ("Not enough Confidence.") 
                timestamp = time.time() - time_start
                m, s = divmod(timestamp, 60)
                h, m = divmod(m, 60)
                print ("Current time is %d (%d:%d:%d)" % (timestamp, h, m, s))
