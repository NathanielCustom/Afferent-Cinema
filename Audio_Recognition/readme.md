Fingerprinting Movies

The provided version of Dejavu includes modifications for automatically splitting large audio files into smaller managaeble chunks and sending them off to the processor, taking advantage of multiple cores.

Basic testing found that for a 1 Hour 40 Minute movie a ~120MB audio file is created and takes ~2 hours to fingerprint on a Raspberry Pi 3.


Procedure:
Setup Afferent Cinema
1. Dejavu and its dependents installed.
2. Install and create a MYSQL database.
3. Edit config.json in root Afferent Cinema folder with the proper database settings.

Extract Movie Audio
Note: Testing a song track (~3-5 Minutes) would be an ideal test before committing to fingerprinting a full movie. To test an audio track skip down to 'Fingerprint Audio' and substitute the movie audio file with the song.
4. Install WinFF
5. 'Add' the movie file to fingerprint.
6. 'Convert to:' 'Audio'. Select 'Preset' "MP3".
7. Select and 'Output Folder'.
8. Convert

Fingerprint Audio
9. Place the newly created audio file into the '..\Audio_Recognition\fingerprint_drop' folder
10. Run fingerprint_audio.py and wait...

Test Audio Recognition
11. Run test_audio_recognition.py
12. Playback movie with microphone in range while program is running.
