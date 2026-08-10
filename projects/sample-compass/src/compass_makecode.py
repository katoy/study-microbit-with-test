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
    # 8 方位判定の前に有効範囲を確認する
    if heading != heading or heading < 0 or heading >= 360:
        return "ERR"

    # 各方位は 45 度幅
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
    # ボタン A でログに時間と角度と方向名を出力
    global is_calibrated
    if not is_calibrated:
        calibrate_compass()
    else:
        heading = input.compass_heading()
        direction = get_direction_string(heading)
        console.log("Time: " + str(input.running_time()) + "ms, Heading: " + str(heading) + ", Dir: " + direction)
input.on_button_pressed(Button.A, on_button_pressed_a)

# 起動時の指示
basic.show_string("COMPASS")
basic.show_string("A:LOG")

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
            # 8方向の矢印で表示
            if direction == "N":
                basic.show_arrow(ArrowNames.NORTH)
            elif direction == "NE":
                basic.show_arrow(ArrowNames.NORTH_EAST)
            elif direction == "E":
                basic.show_arrow(ArrowNames.EAST)
            elif direction == "SE":
                basic.show_arrow(ArrowNames.SOUTH_EAST)
            elif direction == "S":
                basic.show_arrow(ArrowNames.SOUTH)
            elif direction == "SW":
                basic.show_arrow(ArrowNames.SOUTH_WEST)
            elif direction == "W":
                basic.show_arrow(ArrowNames.WEST)
            elif direction == "NW":
                basic.show_arrow(ArrowNames.NORTH_WEST)
            basic.pause(500)

basic.forever(on_forever)
