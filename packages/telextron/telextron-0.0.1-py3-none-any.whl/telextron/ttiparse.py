# Color
COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
]
# Mode
MODE_ALPHABETIC = "ALPHABETIC"
MODE_MOSAIC = "MOSAIC"
# Size
SIZE_NORMAL = "NORMAL"
SIZE_DOUBLE_HEIGHT = "DOUBLE_HEIGHT"
SIZE_DOUBLE_WIDTH = "DOUBLE_WIDTH"
SIZE_DOUBLE_SIZE = "DOUBLE_SIZE"

MOSAICS = '                ' + \
    '                ' + \
    ' 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎' + \
    '🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝' + \
    '@ABCDEFGHIJKLMNO' + \
    'PQRSTUVWXYZ←½→↑⌗' + \
    '🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬' + \
    '🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█'

class Attributes:
    def __init__(self):
        self.mode = MODE_ALPHABETIC
        self.foreground = 7
        self.background = 0
        self.flashing = False
        self.lining = False
        self.size = SIZE_NORMAL

def output_lines(file):
    next_n = 0
    for line in file:
        def chomp():
            nonlocal line
            i = line.find(',')
            prefix = line[:i]
            line = line[i+1:]
            return prefix

        command = chomp()
        if command == 'OL':
            n = int(chomp())
            while next_n < n:
                attr = Attributes()
                yield ((' ', attr),) * 40
                next_n += 1
            yield characters(line)
            next_n = n + 1

def characters(line):
    def chomp():
        nonlocal line
        prefix = line[0]
        line = line[1:]
        return prefix

    attr = Attributes()

    while True:
        character = chomp()
        if character == '\n':
            return
        elif character == '\x1b':
            escape = ord(chomp())
            if escape == 0x48:
                attr.flashing = True
            elif escape == 0x49:
                attr.flashing = False
            elif escape == 0x4a:
                pass # TODO: end box
            elif escape == 0x4b:
                pass # TODO: start box
            elif escape == 0x4c:
                attr.size = SIZE_NORMAL
            elif escape == 0x4d:
                attr.size = SIZE_DOUBLE_HEIGHT
            elif escape == 0x4e:
                attr.size = SIZE_DOUBLE_WIDTH
            elif escape == 0x4f:
                attr.size = SIZE_DOUBLE_SIZE
            elif escape == 0x58:
                pass # TODO: conceal
            elif escape == 0x59:
                attr.lining = False
            elif escape == 0x5a:
                attr.lining = True
            elif escape == 0x5b:
                pass # TODO: Control Sequence Introducer
            elif escape == 0x5c:
                attr.background = 0
            elif escape == 0x5d:
                attr.background = attr.foreground
            elif escape >= 0x40 and escape <= 0x47:
                attr.mode = MODE_ALPHABETIC
                attr.foreground = escape - 0x40
            elif escape >= 0x50 and escape <= 0x57:
                attr.mode = MODE_MOSAIC
                attr.foreground = escape - 0x50
            else:
                raise NotImplementedError(hex(escape))
            yield (' ', attr)
        else:
            if attr.mode == MODE_MOSAIC:
                mosaic = ord(character)
                character = MOSAICS[mosaic]
            yield (character, attr)
