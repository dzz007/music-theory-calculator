# by dzz007, 2020/10/22
# this program can calculate the harmonic of a given pitch in a given scale
# the scale is defined by how many sharps or flats in the signature.
# for example (under major mode):
#   3 b
#   Ab
# would return the harmonic function of A-flat in the major that has signature of 3 flats in it

scale_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
scale_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'Cb']

jumptable = [[
    # for major
    2, 2, 1, 2, 2, 2, 0
], [
    # for minor
    2, 1, 2, 2, 1, 2, 0
]]

personalities = [
    # major
    ['tonic', 'supertonic', 'mediant', 'subdominant', 'dominant', 'submediant', 'leading-tone'],
    # minor
    ['tonic', 'supertonic', 'mediant', 'subdominant', 'dominant', 'submediant', 'subtonic']
]

traid_types = [
    # major
    ['major', 'minor', 'minor', 'major', 'major', 'minor', 'diminished'],
    # minor
    ['minor', 'diminished', 'major', 'minor', 'minor', 'major', 'major']
]

cycle_of_fifths = [
    # sharps
    [
        ('C', 'A'), ('G', 'E'), ('D', 'B'), ('A', 'F#'), ('E', 'C#'), ('B', 'G#'), ('F#', 'D#'), ('C#', 'A#')
    ],
    # flats
    [
        ('C', 'A'), ('F', 'D'), ('Bb', 'G'), ('Eb', 'C'), ('Ab', 'F'), ('Db', 'Bb'), ('Gb', 'Eb'), ('Cb', 'Ab')
    ]
]


def decrease(x):
    if x[0] == 'A':
        base = 'G'
    else:
        base = chr(ord(x[0]) - 1)
    return base + '#'


def increase(x):
    if x[0] == 'G':
        base = 'A'
    else:
        base = chr(ord(x[0]) + 1)
    return base + 'b'


# given a key, return a whole scale, ex. build_scale('Ab', 1) return A-flat minor
# type 0 major, 1 minor
def build_scale(key, type):
    if len(key) >= 2 and key[1] == 'b':
        raw = scale_flats + scale_flats
    else:
        raw = scale_sharps + scale_sharps

    raw_pt = raw.index(key)
    chosen = 0
    result = list()

    prev = None

    while chosen < 7:
        tmp = raw[raw_pt]
        if prev:
            if ord(tmp[0]) - ord(prev[0]) > 1:
                # we need to decrease tmp by 1
                tmp = decrease(tmp)
            elif ord(tmp[0]) - ord(prev[0]) == 0:
                # we need to increase tmp by 1
                tmp = increase(tmp)

        result.append(tmp)
        prev = tmp
        raw_pt += jumptable[type][chosen]
        chosen += 1
    return result


def get_personality(key_input, pitch):
    opts = key_input.split()
    type = 0 if opts[2] == 'maj' else 1

    scale = build_scale_sub_interactive(key_input)

    if pitch not in scale:
        return 'dont exist'

    return 'P: ' + personalities[type][scale.index(pitch)] + ' Triad: ' + traid_types[type][scale.index(pitch)]


# prompt for user to input a key signature and return a scale
def build_scale_sub_interactive(key_input=None):
    if key_input is None:
        key_input = input("Key: ")
    opts = key_input.split()
    amount = opts[0]
    accent = opts[1]
    type = 0 if opts[2] == 'maj' else 1

    key = cycle_of_fifths[0 if accent == '#' else 1][int(amount)][type]

    print(key + ' ' + ('major' if type == 0 else 'minor'))
    scale = build_scale(key, type)
    print(scale)
    return scale


def interactive():
    # 0 major mode, 1 minor mode, can be changed at run time through typing 0 or 1 in 'Key: ' with non-empty Pitch input
    mode = 0
    while True:
        print('Mode: ' + ('major' if mode == 0 else 'minor'))
        key_input = input('Key: ')
        pitch_input = input('Pitch: ')

        if not key_input or not pitch_input:
            break

        if key_input == '0':
            mode = 0
            print('Changed mode')
            continue
        elif key_input == '1':
            mode = 1
            print('Changed mode')
            continue

        print(get_personality(key_input + (' maj' if mode == 0 else ' min'), pitch_input))
        print('')


if __name__ == '__main__':
    # given key signature and a note, calculate it's harmonic function as well as triad type built on this note in this key
    interactive()
