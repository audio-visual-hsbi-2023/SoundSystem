# SoundSystem 🎼

## Start System 🚀

As of now there isn't a good way to start the system from command line or script.
The best way is to simply start intelliJ and run the ```SoundSystem.oy``` file.

## Connect to System 💻

The Server communicates through the OCP protocol.

A simple UDP Client that sends OSC messages is enough to connect to the server.

Only a localhost connection is needed, but can configured to actually communicate over network.

    PORT: 8999
    URL: 127.0.0.1

These values can be configured in the ```src/server/SoundSystemServer.py``` file.

## Available commands 💬

Each command consists of three sections terminated by a $-sign.

    command;string_value;numeric_value$

The command is one of the below listed ones. The second section is reserved for string values. 
Either a string of max 50 characters or an _. This depends on the command.
The third section is reserved for numeric values. There will always be a number.
If the command doesn't need numeric values it accepts a 0.

### Next Song

There are no values specified here. Parameters shall be _ and 0. A String
satisfying the REGEX will suffice.

    NEXT_SONG_REGEX = r"^NEXT_SONG;_;0$"

### Play SFX

As string value give the name of the sfx you want to play. Availalbe SFX are listed below.

The numeric value shall be a Number ranging from -90 to 90. It represents the direction
of the sound. -90 is hard left and 90 is hard right.

    SFX_REGEX = r"^PLAY_SFX;.{1,50};(-?[0-9]|[1-8][0-9]|90)$"

### Change Phase

No string value shall be given.

As a numeric value give a value ranging from 1-5 which represent the Phases.

    PHASE_CHANGE_REGEX = r"^PHASE_CHANGE;_;([1-5])$"

### Start/Stop

Use the REGEX below to either start or stop the Music.

    START_REGEX = r"^START;_;0$"
    EXIT_REGEX = r"^EXIT;_;0$"

## Available SFX Sounds 🎶

    a_calm_ambient
    bells_soft
    bell_ambient
    birds
    cymbal_impact
    dreaming_forest
    enchanted
    forest
    it_s_morning
    journey_through_space
    keys_of_relaxation
    lifting_guitar
    metal_grinding
    metal_whoosh_ambient
    piano_ambient
    ping_contact
    sharp
    short_logo
    sisters_voices
    soft_rain_umbrella
