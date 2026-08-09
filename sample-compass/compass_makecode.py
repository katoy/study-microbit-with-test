# micro:bit 用方位磁石（MakeCode Python / Static Python 互換実装）
#
# このファイルは Microsoft MakeCode エディタの Python モードに
# 直接コピー＆ペーストしてブロック表示・書き込みができる互換コードです。
# （標準の MicroPython ライブラリである `from microbit import *` は使用しません）

is_calibrated = False

def calibrate_compass():
    global is_calibrated
    basic.clear_screen()
    # 矢印で校正中であることを示す
    basic.show_leds("""
        . . # . .
        . # # # .
        # # # # #
        . # # # .
        . . # . .
    """)
    input.calibrate_compass()
    basic.clear_screen()
    basic.show_string("OK")
    is_calibrated = True

def get_direction_string(heading: number) -> str:
    # 8方位判定（各方位は45度幅）
    if heading < 22.5 or heading >= 337.5:
        return "N"
    elif heading < 67.5:
        return "NE"
    elif heading < 112.5:
        return "E"
    elif heading < 157.5:
        return "SE"
    elif heading < 202.5:
        return "S"
    elif heading < 247.5:
        return "SW"
    elif heading < 292.5:
        return "W"
    else:
        return "NW"

def on_button_pressed_a():
    calibrate_compass()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    # ボタンBを押して現在の角度と方位を表示
    global is_calibrated
    if not is_calibrated:
        basic.show_string("CAL?")
    else:
        heading = input.compass_heading()
        if heading < 0:
            basic.show_string("ERR")
        else:
            direction = get_direction_string(heading)
            basic.show_string(direction)
            basic.show_number(heading)
input.on_button_pressed(Button.B, on_button_pressed_b)

# 起動時の指示
basic.show_string("COMPASS")
basic.show_string("A:CAL B:CHK")

def on_forever():
    global is_calibrated
    if not is_calibrated:
        # キャリブレーション未完了時は 'CAL' を表示して促す
        basic.show_string("CAL")
        basic.pause(1000)
    else:
        heading = input.compass_heading()
        if heading < 0:
            basic.show_string("ERR")
            basic.pause(1000)
        else:
            direction = get_direction_string(heading)
            # LED スクリーンに主要方角の簡易マークを表示
            if direction == "N":
                basic.show_leds("""
                    . . # . .
                    . # # # .
                    # . # . #
                    . . . . .
                    . . . . .
                """)
            elif direction == "E":
                basic.show_leds("""
                    . . # . .
                    . . # # .
                    . . # . .
                    . . # # .
                    . . # . .
                """)
            elif direction == "S":
                basic.show_leds("""
                    . . # . .
                    . . . . .
                    # . # . #
                    . # # # .
                    . . # . .
                """)
            elif direction == "W":
                basic.show_leds("""
                    . . # . .
                    . # # . .
                    . . # . .
                    . # # . .
                    . . # . .
                """)
            else:
                basic.show_string(direction)
            basic.pause(500)

basic.forever(on_forever)
