#!/usr/bin/env python3

import sys
import os

def merge_emotions(target_path, source_paths):
    if not os.path.isdir(target_path):
        os.mkdir(target_path)

    default_name = "0000.wav"

    merged_name = "merged.wav"
    merged_path = os.path.join(target_path, merged_name)

    filter_string = ""
    for i in range(len(source_paths)):
        filter_string += "[{:d}:0]".format(i)
    filter_string += "concat=n={:d}:v=0:a=1".format(len(source_paths))
    filter_string += "[out]"

    command = "ffmpeg"
    for i in range(len(source_paths)):
        original_path = os.path.join(source_paths[i], default_name)
        command += " -i \"{}\"".format(original_path)
    command += " -filter_complex \"{}\"".format(filter_string)
    command += " -map \"[out]\""
    command += " \"{}\"".format(merged_path)

    print("Executing {}...".format(command))
    if os.system(command) == 0:
        print("Success!")
    else:
        print("Error!")
        return

    final_path = os.path.join(target_path, default_name)

    print("Renaming...")
    os.replace(merged_path, final_path)
    print("Success!")


def main(argv):
    if len(argv) < 2:
        print("Usage: {} <data-path>".format(argv[0]))
        return 1

    data_path = str(argv[1])
    if not os.path.isdir(data_path):
        return 1

    common_path = os.path.join(data_path, "_COMMON")
    if not os.path.isdir(common_path):
        return 1

    for character in os.listdir(data_path):
        if character[0] == "_":
            continue

        character_path = os.path.join(data_path, character)
        if not os.path.isdir(character_path):
            continue

        new_thinny_path = os.path.join(character_path, "THINNY")
        thinny_path = new_thinny_path
        if not os.path.isdir(thinny_path):
            thinny_path = os.path.join(common_path, "THINNY")
            if not os.path.isdir(thinny_path):
                continue

        new_door_path = os.path.join(character_path, "DOOR")
        door_path = new_door_path
        if not os.path.isdir(door_path):
            door_path = os.path.join(common_path, "DOOR")
            if not os.path.isdir(door_path):
                continue

        new_form_katet_path = os.path.join(character_path, "FORM_KATET")
        form_katet_path = new_form_katet_path
        if not os.path.isdir(form_katet_path):
            form_katet_path = os.path.join(common_path, "FORM_KATET")
            if not os.path.isdir(form_katet_path):
                continue

        new_crimson_voice_path = os.path.join(character_path, "_CRIMSON_VOICE")
        crimson_voice_path = new_crimson_voice_path
        if not os.path.isdir(crimson_voice_path):
            crimson_voice_path = os.path.join(common_path, "_CRIMSON_VOICE")
            if not os.path.isdir(crimson_voice_path):
                continue

        new_road_path = os.path.join(character_path, "_ROAD")
        road_path = new_road_path
        if not os.path.isdir(road_path):
            road_path = os.path.join(common_path, "_ROAD")
            if not os.path.isdir(road_path):
                continue

        new_fate_path = os.path.join(character_path, "_FATE")
        fate_path = new_fate_path
        if not os.path.isdir(fate_path):
            fate_path = os.path.join(common_path, "_FATE")
            if not os.path.isdir(fate_path):
                continue

        merge_emotions(new_thinny_path,
                       [thinny_path, crimson_voice_path])

        merge_emotions(new_door_path,
                       [door_path, road_path, crimson_voice_path])

        merge_emotions(new_form_katet_path,
                       [form_katet_path, fate_path])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
