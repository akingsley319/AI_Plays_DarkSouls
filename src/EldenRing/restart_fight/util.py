import vgamepad as vg


def press_and_release(gamepad, button):
    gamepad.press_button(button=button)
    gamepad.update()
    gamepad.release_button(button=button)
    gamepad.update()
