#!/usr/bin/env python3

import sys
import os
import shutil

def main(argv):
    if len(argv) < 4:
        usage = "Usage: {} <csv-path> <music-path> <card-path> [character]"
        print(usage.format(argv[0]))
        return 1

    csv_path = str(argv[1])
    if not os.path.isdir(csv_path):
        return 1

    music_path = str(argv[2])
    if not os.path.isdir(music_path):
        return 1

    common_music_path = os.path.join(music_path, "_COMMON")
    if not os.path.isdir(common_music_path):
        return 1

    card_path = str(argv[3])

    if len(argv) > 4:
        characters = [argv[4]]
    else:
        characters = os.listdir(csv_path)

    for character in characters:
        if character[0] == "_":
            continue

        character_csv_path = os.path.join(csv_path, character)
        if not os.path.isdir(character_csv_path):
            continue

        character_music_path = os.path.join(music_path, character)
        if not os.path.isdir(character_music_path):
            continue

        while True:
            answer = input("Process {}? <y/n> ".format(character))
            if len(answer) == 0:
                continue
            if answer[0] == "n":
                break
            if answer[0] != "y":
                continue

            input("Insert {} card and press any key...".format(character))

            if not os.path.isdir(card_path):
                print("Unable to open card!")
                continue

            for element in os.listdir(character_csv_path):
                element_path = os.path.join(character_csv_path, element)
                if os.path.isfile(element_path):
                    shutil.copy2(element_path, card_path)
                elif os.path.isdir(element_path):
                    new_element_path = os.path.join(card_path, element)
                    shutil.copytree(element_path, new_element_path)

            for emotion in os.listdir(common_music_path):
                if emotion[0] == "_":
                    continue

                emotion_path = os.path.join(character_music_path, emotion)
                if not os.path.isdir(emotion_path):
                    emotion_path = os.path.join(common_music_path, emotion)
                    if not os.path.isdir(emotion_path):
                        continue

                new_emotion_path = os.path.join(card_path, emotion)
                shutil.copytree(emotion_path, new_emotion_path)

            print("{} processed!".format(character))
            break

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
