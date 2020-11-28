from music_theory import *

scale_sharps = ['B#', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B']
scale_flats = ['C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'Cb']
diatonic_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
flavor_dict = ['d', 'p', 'a', 'n', 'j']  # diminished perfect augmented minor major
flavor_readable = ['diminished', 'perfect', 'augmented', 'minor', 'major']

interval_dict = {
    4: [4, 5, 6, 0, 0],
    5: [6, 7, 8, 0, 0],
    3: [2, 0, 5, 3, 4],
    6: [7, 0, 10, 8, 9],
    2: [0, 0, 3, 1, 2],
    7: [9, 0, 12, 10, 11]
}


# get diatonic difference between note [ignore sharp/flat]
def get_diff(start, proposed):
    table = diatonic_scale + diatonic_scale
    start_idx = table.index(start[0])
    proposed_idx = table.index(proposed[0], start_idx + 1)
    return proposed_idx - start_idx


def get_next(start_note, interval):
    data_bank = [scale_flats, scale_sharps]
    if start_note in scale_flats:
        data_idx = 0
    else:
        data_idx = 1
    raw = data_bank[data_idx] + data_bank[data_idx]

    start_idx = raw.index(start_note)
    amount = interval_dict[int(interval[1])][flavor_dict.index(interval[0])]

    end_idx = start_idx + amount

    proposed_next = raw[end_idx]

    diff = get_diff(start_note, proposed_next)

    if diff < int(interval[1]) - 1 or diff > int(interval[1]) - 1:
        # need to change expression
        candidate_output = '[need: {}] {} (diff: {}) '.format(interval[1], proposed_next, diff + 1)

        data_idx = int(not bool(data_idx))
        raw = data_bank[data_idx] + data_bank[data_idx]
        proposed_next = raw[end_idx]


        diff = get_diff(start_note, proposed_next)
        if diff < int(interval[1]) - 1 or diff > int(interval[1]) - 1:
            # even replacement doesn't work
            candidate_output += '{} (diff: {}) '.format(proposed_next, diff + 1)
            return "ERROR, UNABLE PRODUCE [{}]".format(candidate_output)

    return proposed_next


# given start note and interval calculate next note
def next_interactive():
    while True:
        note_input = input('Note: ')
        interval_input = input('Interval: ')

        if not note_input or not interval_input:
            break

        if note_input[0] == 'k' and len(note_input) == 2:
            print('{}: {}'.format(note_input[1:], get_next(note_input[1:], interval_input)))
            print('{}: {}'.format(note_input[1:] + '#', get_next(note_input[1:] + '#', interval_input)))
            print('{}: {}'.format(note_input[1:] + 'b', get_next(note_input[1:] + 'b', interval_input)))
        else:
            print(get_next(note_input, interval_input))
        print('')


def seventh_interactive():
    dominant_dict = ['j3', 'p5', 'n7']  # last one is based on root
    diminished_dict = ['n3', 'd5', 'd7']
    dicts = [dominant_dict, diminished_dict]
    mode = 0
    mode_readable = ['Dominant', 'Diminished']
    main_dict = dicts[mode]
    while True:
        note_input = input('Note: ')

        if not note_input:
            break

        if note_input[0] == 'm':
            mode = int(note_input[1])
            main_dict = dicts[mode]
            print("Mode changed to {}".format(mode_readable[mode]))
            continue

        print(note_input)

        for i in range(len(main_dict)):
            print(get_next(note_input, main_dict[i]))

        print('')


# given two notes, return the interval between them
def guess_diff(note1, note2):
    for k, v in interval_dict.items():
        for flavor in flavor_dict:
            f_idx = flavor_dict.index(flavor)
            if v[f_idx] == 0:
                continue    # skip unavailable
            if get_next(note1, flavor + str(k)) == note2:
                return flavor_readable[f_idx] + ' ' + str(k)
    return 'UNAVAILABLE'


# Given a note and a scale, if note is not sharped or flatted, then try to adjust it so it fits into the scale
def adjust(note, scale):
    if note not in scale and len(note) == 1:
        for n in scale:
            if n[0] == note[0]:
                print('Adjusted {} to {}'.format(note, n))
                return n
    else:
        return note


# given two note, and the scale they are in, try to guess what is the interval
# note: the reason we need to specify scale is because we want to automatically adjust the note to add sharps/flats
# so we dont need to look it up in the sheet
# another note: the way to specify scale is to put how many flats/sharps in the scale
#   ex. 3 # maj [try to look up a major scale with 3 sharps]
#       4 b min [try to look up a minor scale with 4 flats]
def diff_interactive(key_support):
    while True:
        if key_support:
            scale = build_scale_sub_interactive()

        note1_input = input('Note1: ')
        note2_input = input('Note2: ')

        if not note1_input or not note2_input:
            break

        # only adjust when not specified
        if key_support:
            note1_input = adjust(note1_input, scale)
            note2_input = adjust(note2_input, scale)

        # try all possible intervals
        print(guess_diff(note1_input, note2_input))


# input key (optional) and four notes, try to guess the seventh chord formed by these four notes and the inversion
def seventh_inversion_interactive(key_support):
    # guess the seventh chord based on ordered notes (i.e. root position(no inversion))
    def guess(ordered_data):
        result_dict = {
            'major-major': ['major 3', 'perfect 5', 'major 7'],
            'minor-minor': ['minor 3', 'perfect 5', 'minor 7'],
            'major-minor': ['major 3', 'perfect 5', 'minor 7'],
            'half-diminished': ['minor 3', 'diminished 5', 'minor 7'],
            'fully-diminished': ['minor 3', 'diminished 5', 'diminished 7']
        }
        guessed_result = []
        for i in range(1, len(ordered_data)):
            # diff between root, i
            guessed_result.append(guess_diff(ordered_data[0], ordered_data[i]))
        for k, v in result_dict.items():
            if guessed_result == v:
                return k
        return "NO MATCH"

    def counter_rotate(n):
        return n[-1:] + n[:-1]

    while True:
        if key_support:
            scale = build_scale_sub_interactive()

        data = []
        for i in range(4):
            note = input("Note {}: ".format(i + 1))
            note = adjust(note, scale)
            data.append(note)

        inversion_list = [[3, 5, 7], [3, 5, 6], [3, 4, 6], [2, 4, 6], [3, 5, 7]]
        inversion_readable = ['7', '6/5', '4/3', '4/2']
        interval_list = []

        for i in range(1, len(data)):
            interval_list.append(int(guess_diff(data[0], data[i]).split()[1]))  # only numbers
        inverted = inversion_list.index(interval_list)
        print("{} inversion ({})".format(inverted, inversion_readable[inverted]))
        for i in range(inverted):
            data = counter_rotate(data)  # reverse inversion
        print(guess(data))

if __name__ == '__main__':
    # given key (optional to adjust notes) and four notes, try to guess the seventh chord formed by these four notes and the inversion
    # seventh_inversion_interactive(True)

    # given root note, build a diminished or dominant seventh chord on the root note
    # seventh_interactive()

    # given key (optional to adjust notes) and two notes, return the interval between them
    # diff_interactive(True)

    # given a note and an interval, calculate the next note
    # if note starts with k and has no sharp/flat (ex. kC)
    #   it will calculate note + interval, note# + interval and noteb + interval
    next_interactive()
