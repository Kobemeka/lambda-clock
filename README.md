# lambda-clock
A digital terminal clock

To run the clock, go to the folder where `lambda-clock.py` is located and type `python lambda-clock.py` into the terminal.

## Command Line Arguments

You can also do `python lambda-clock.py -h` to list the all command line arguments.

### Format

Command line argument: `-m` or `--format`

_**The format of the clock.**_

1. m (Hour:Minute)
2. s (Hour:Minute:Second) (Default)
3. ms (Hour:Minute:Second:Microsecond)
4. ds (Day:Month:Year Hour:Minute:Second)

### Position

Command line argument: `-p` or `--position`

_**Position of the clock.**_

You can choose one of the 9 positions: 1 to 9.

Think of it as a grid starts from the top left corner and ends at the bottom right corner.

Default position is 5.

`1 2 3`

`4 5 6`

`7 8 9`

### Coloring

Command line argument: `-c` or `--coloring`

_**How to color the clock.**_

1. Default
2. Gradient (Default)

### Spacing Character

Command line argument: `-s` or `--spacing`

_**The character that fills the space between characters in the clock.**_

Default character is *empty*

You can choose one of the character in the fonts.

### Empty Cell Character

Command line argument: `-e` or `--echar`

_**The empty cell character.**_

Default character is *empty*

You can choose one of the character in the fonts.


### Full Cell Character

Command line argument: `-f` or `--fchar`

_**The non-empty cell character.**_

Default character is *full-block*

You can choose one of the character in the fonts.

### Gradient Style

Command line argument: `--gstyle`

_**Style of the gradient.**_

Applied only if coloring option is selected as gradient.

1. horizontal (Default)
2. vertical
3. diagonal
4. reverse-diagonal

### Gradient Colors

For gradient HSV is used and program needs start and spread values for both hue (H) and saturation (S).

Accepts only floats between 0.0 and 1.0 (both included)

Note: value (V) is constant and equal to 1.

For example, if start value of hue is 0.0 and spread is 0.5, the hue of gradient starts from 0.0 and ends at 0.0 + 0.5 = 0.5. It is same for saturation. 

#### Hue Start

Command line argument: `--hstart`

_**Start value of hue.**_

Default value is 0.0

#### Hue Spread

Command line argument: `--hspread`

_**Spread value of hue.**_

Default value is 0.1

#### Saturation Start

Command line argument: `--sstart`

_**Start value of saturation.**_

Default value is 1.0

#### Saturation Spread

Command line argument: `--sspread`

_**Spread value of saturation.**_

Default value is 0.0
