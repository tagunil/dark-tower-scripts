#!/usr/bin/env python3

import sys
import os

import ffmpeg_normalize

LEVELS = {
    "_ROAD": 9,
    "_FATE": 9,
    "_CRIMSON_VOICE": 9,
    "DOOR": 9,
    "CRIMSON": 12,
    "CRIMSONISH": 12,
    "NEUTRAL": 12,
    "WHITISH": 12,
    "WHITE": 12,
    "CORRUPT": 12,
    "HYPNOSIS": 12,
    "WHITE_BELIEVE": 12,
    "CRIMSON_ANGER": 12,
    "FORM_KATET": 9,
    "DESTROY_KATET": 12,
    "ARRIVING": 12,
    "HEART": 6,
    "WHITE_GLORY": 9,
    "ROSE": 12,
    "CRIMSON_KING_SONG": 9,
    "HOPE": 12,
    "CRIMSON_SERVANT": 12,
    "EAGLE": 12,
    "LION": 12,
    "BEAM_CLOSE": 6,
    "BEAM": 12,
    "CURSE": 12,
    "HEAL": 6,
    "HEAL_LONG": 6,
    "CRIMSON_BROADCAST1": 12,
    "CRIMSON_BROADCAST2": 12,
    "CRIMSON_BROADCAST3": 12,
    "CRIMSON_BROADCAST4": 12,
    "TIMELINE_GATHERING": 12,
    "TIMELINE_TRAIN_ARRIVING": 12,
    "TIMELINE_TRAIN": 6,
    "CRIMSON_SERVANT_FEELING": 6,
    "GUNSLINGER_FEELING": 6,
    "CRIMSON_LAUGH": 12,
    "WHITE_SORROW": 12,
    "WHITE_JOY": 12,
    "CRIMSON_GRIEVE": 12,
    "DOOR_NEAR": 12,
    "DOOR_FAR": 9,
    "DAEMON": 12,
    "THINNY": 9,
    "BLESS": 6,
    "FEAR": 9,
    "CRIMSON_PLACE": 0,
    "INN": 0,
    "MANNI": 0,
    "GERRARO": 0,
    "MORANO": 0,
    "MASTERKA": 0,
    "DEATH": 6,
    "BOOT": 6,
    "TISHINA": 0
}


def convert_file(level, path, original_name, index):
    initial_path = os.getcwd()
    os.chdir(path)

    index_string = "{:04d}".format(index)

    final_name = index_string + ".wav"

    normalizer = ffmpeg_normalize.FFmpegNormalize(
        normalization_type="ebu",
        target_level=float(level),
        loudness_range_target=17.0,
        true_peak=0.0,
        sample_rate=44100,
        output_format="wav",
        print_stats=True
    )

    normalizer.add_media_file(original_name, final_name)

    print("Converting {}...".format(os.path.join(path, original_name)))
    normalizer.run_normalization()
    print("Success!")

    os.remove(original_name)

    os.chdir(initial_path)


def main(argv):
    if len(argv) < 2:
        print("Usage: {} <data-path> [base-level]".format(argv[0]))
        return 1

    base_level = -26
    if len(argv) > 2:
        base_level = int(argv[2])

    data_path = str(argv[1])
    if not os.path.isdir(data_path):
        return 1

    for character in os.listdir(data_path):
        character_path = os.path.join(data_path, character)
        if not os.path.isdir(character_path):
            continue

        for emotion in os.listdir(character_path):
            emotion_path = os.path.join(character_path, emotion)
            if not os.path.isdir(emotion_path):
                continue

            tracks = []

            for track in os.listdir(emotion_path):
                track_path = os.path.join(emotion_path, track)
                if not os.path.isfile(track_path):
                    continue

                tracks.append(track)

            tracks.sort()

            level = base_level
            if emotion in LEVELS:
                level += LEVELS[emotion]

            for (index, track) in enumerate(tracks):
                convert_file(level, emotion_path, track, index)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
