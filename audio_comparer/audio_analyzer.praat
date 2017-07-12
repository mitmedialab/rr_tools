# The input is a single wav file to be analyzed

form Counting Syllables in Sound Utterances
    sentence target_file sample2.wav
endform

# Got files:
printline Target file: 'target_file$'

# Pitch range to consider (children generally 200-400 Hz).
floor = 100
ceiling = 500

# Read target file and detect features.
if fileReadable(target_file$)
    # Detect speech rate.
    printline Detecting target speech rate...
    @detectSpeechRate: target_file$
    target_speech_rate = speakingrate
    target_sound_id = soundid
    printline
    printline Speaking rate: 'speakingrate'

    # Get mean pitch of target.
    select 'target_sound_id'
    To Pitch... 0 floor ceiling
    target_mean_pitch = Get mean... 0 0 Hertz
    printline Mean pitch: 'target_mean_pitch'

    # Get mean intensity of target.
    select 'target_sound_id'
    To Intensity... 100 0
    mean_intensity = Get mean... 0 0 dB
    printline Mean intensity: 'mean_intensity'
else
    printline Cannot read target file
    exit
endif

# Done!
printline Done!

####################################################
####### Speech rate detection - DO NOT TOUCH #######
####################################################

# counts syllables of all sound utterances in a directory
# NB unstressed syllables are sometimes overlooked
# NB filter sounds that are quite noisy beforehand
# NB use Silence threshold (dB) = -25 (or -20?)
# NB use Minimum dip between peaks (dB) = between 2-4 (you can first try;
#                                         For clean and filtered: 4)
procedure detectSpeechRate: .wav_file$

    # Silence threshold in dB, default -25.
    silencedb = -25
    # Minimum dip between peaks in dB, default 2.
    mindip = 2
    # Minimum pause duration in s, default 0.3.
    minpause = 0.3
    # Keep soundfiles and textgrids, default false.
    showtext = 0

    # Read in wav file.
    Read from file... '.wav_file$'

    # use object ID
    soundname$ = selected$("Sound")
    soundid = selected("Sound")

    originaldur = Get total duration
    # allow non-zero starting time
    bt = Get starting time

    # Use intensity to get threshold
    To Intensity... 50 0 yes
    intid = selected("Intensity")
    start = Get time from frame number... 1
    nframes = Get number of frames
    end = Get time from frame number... 'nframes'

    # estimate noise floor
    minint = Get minimum... 0 0 Parabolic
    # estimate noise max
    maxint = Get maximum... 0 0 Parabolic
    #get .99 quantile to get maximum (without influence of non-speech sound bursts)
    max99int = Get quantile... 0 0 0.99

    # estimate Intensity threshold
    threshold = max99int + silencedb
    threshold2 = maxint - max99int
    threshold3 = silencedb - threshold2
    if threshold < minint
        threshold = minint
    endif

    # get pauses (silences) and speakingtime
    # This also trims extra silence from the start and end of the file.
    To TextGrid (silences)... threshold3 minpause 0.1 silent sounding
    textgridid = selected("TextGrid")
    silencetierid = Extract tier... 1
    silencetableid = Down to TableOfReal... sounding
    nsounding = Get number of rows
    npauses = 'nsounding'
    speakingtot = 0
    for ipause from 1 to npauses
        beginsound = Get value... 'ipause' 1
        endsound = Get value... 'ipause' 2
        speakingdur = 'endsound' - 'beginsound'
        speakingtot = 'speakingdur' + 'speakingtot'
    endfor

    select 'intid'
    Down to Matrix
    matid = selected("Matrix")
    # Convert intensity to sound
    To Sound (slice)... 1
    sndintid = selected("Sound")

    # use total duration, not end time, to find out duration of intdur
    # in order to allow nonzero starting times.
    intdur = Get total duration
    intmax = Get maximum... 0 0 Parabolic

    # estimate peak positions (all peaks)
    To PointProcess (extrema)... Left yes no Sinc70
    ppid = selected("PointProcess")

    numpeaks = Get number of points

    # fill array with time points
    for i from 1 to numpeaks
        t'i' = Get time from index... 'i'
    endfor


    # fill array with intensity values
    select 'sndintid'
    peakcount = 0
    for i from 1 to numpeaks
        value = Get value at time... t'i' Cubic
        if value > threshold
              peakcount += 1
              int'peakcount' = value
              timepeaks'peakcount' = t'i'
        endif
    endfor


    # fill array with valid peaks: only intensity values if preceding
    # dip in intensity is greater than mindip
    select 'intid'
    validpeakcount = 0
    currenttime = timepeaks1
    currentint = int1

    for p to peakcount-1
        following = p + 1
        followingtime = timepeaks'following'
        dip = Get minimum... 'currenttime' 'followingtime' None
        diffint = abs(currentint - dip)

        if diffint > mindip
            validpeakcount += 1
            validtime'validpeakcount' = timepeaks'p'
        endif
        currenttime = timepeaks'following'
        currentint = Get value at time... timepeaks'following' Cubic
    endfor


    # Look for only voiced parts
    select 'soundid'
    To Pitch (ac)... 0.02 30 4 no 0.03 0.25 0.01 0.35 0.25 450
    # keep track of id of Pitch
    pitchid = selected("Pitch")

    voicedcount = 0
    for i from 1 to validpeakcount
        querytime = validtime'i'

        select 'textgridid'
        whichinterval = Get interval at time... 1 'querytime'
        whichlabel$ = Get label of interval... 1 'whichinterval'

        select 'pitchid'
        value = Get value at time... 'querytime' Hertz Linear

        if value <> undefined
            if whichlabel$ = "sounding"
                 voicedcount = voicedcount + 1
                 voicedpeak'voicedcount' = validtime'i'
            endif
        endif
    endfor


    # calculate time correction due to shift in time for Sound object versus
    # intensity object
    timecorrection = originaldur/intdur

    # Insert voiced peaks in TextGrid
    if showtext > 0
        select 'textgridid'
        Insert point tier... 1 syllables

        for i from 1 to voicedcount
            position = voicedpeak'i' * timecorrection
            Insert point... 1 position 'i'
        endfor
    endif

    # clean up before next sound file is opened
    select 'intid'
    plus 'matid'
    plus 'sndintid'
    plus 'ppid'
    plus 'pitchid'
    plus 'silencetierid'
    plus 'silencetableid'
    Remove

    # summarize results in Info window
    if originaldur <> 0
        speakingrate = 'voicedcount'/'originaldur'
    else
        speakingrate = 0
    endif
    if speakingtot <> 0
        articulationrate = 'voicedcount'/'speakingtot'
    else
        articulationrate = 0
    endif
    npause = 'npauses'-1
    if voicedcount <> 0
        asd = 'speakingtot'/'voicedcount'
    else
        asd = 0
    endif

    # print a single header line with column names and units
    printline soundname, nsyll, npause, dur (s), phonationtime (s), speechrate (nsyll/dur), articulation rate (nsyll / phonationtime), ASD (speakingtime/nsyll)

    printline 'soundname$', 'voicedcount', 'npause', 'originaldur:2', 'speakingtot:2', 'speakingrate:2', 'articulationrate:2', 'asd:3'

endproc
