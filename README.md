# SoundSystem

## Available commands

Each command consists of three sections terminated by a $-sign.

    command;string_value;numeric_value$

The command is one of the below listed ones. The second section is reserved for string values. 
Either a string of max 50 characters or an _. This depends on the command.
The third section is reserved for numeric values. There will always be a number.
If the command doesn't need numeric values it accepts a 0.
 
    // Manipulate playback of the background music
    // Possible commands are PLAY_MUSIC, NEXT_SONG or PAUSE_SONG
    PLAY_MUSIC_REGEX =      "^(PLAY_MUSIC|NEXT_SONG|PAUSE_SONG);_;0$"
    
    // PLAY_SFX is followed by a string of max 50 chars and then a rotation
    // from -90 (left) to 90 (right)
    PLAY_SFX_REGEX =        "^PLAY_SFX;.{1,50};(-?[0-9]|[1-8][0-9]|90)$"
    
    // Last Parameter is 1 to 5 as we have defined that we wont have more
    PHASE_CHANGE_REGEX =    "^PHASE_CHANGE;_;([1-5])$"
    
    // Shutdown the program
    EXIT_REGEX =            "^EXIT;_;0$"

    // Explicitly start the Background music
    START_REGEX =           "^START;_;0$"

## Available SFX Sounds

    birds (0:12)