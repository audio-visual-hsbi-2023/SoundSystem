# SoundSystem

## Available commands
 
    // Manipulate playback of the background music
    PLAY_MUSIC_REGEX =      "^(PLAY_MUSIC|NEXT_SONG|PAUSE_SONG);_;0"
    
    // PLAY_SFX is followed by a string of max 50 chars and then a rotation
    // from -90 (left) to 90 (right)
    PLAY_SFX_REGEX =        "^PLAY_SFX;.{1,50};(-?[0-9]|[1-8][0-9]|90)"
    
    // Last Parameter is 1 to 5 as we have defined that we wont have more
    PHASE_CHANGE_REGEX =    "^PHASE_CHANGE;_;([1-5])"
    
    // Shutdown the program
    EXIT_REGEX =            "^EXIT;_;0"

    // Explicitly start the Background music
    START_REGEX =           "^START;_;0"

## Available SFX Sounds

    birds (0:12)