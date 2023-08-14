import time
import signal
import pygame
import caffeine
import subprocess
from ctypes import CDLL
from datetime import datetime, timedelta
import os

# Configuration constants
CONF_background_image = "screen1.png"
CONF_width, CONF_height = 5120, 2880
CONF_window_flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE
CONF_exit_passwd = "vxt6"
CONF_max_lock_time = 20 # 60 seconds
CONF_max_stay_time = 18000

pygame.init()
screen = pygame.display.set_mode((CONF_width, CONF_height), flags=CONF_window_flags)
running = True
lock_screen = pygame.image.load(CONF_background_image)
lock_screen = pygame.transform.scale(lock_screen, screen.get_size())
locked = False
lock_time = 0
caffeine.on()
passwd_buffer = ""
# start_time = datetime.now()
start_time = datetime.now().timestamp()
def sad():
    pygame.mouse.set_pos((20, 20))
    pygame.quit()


def signal_handler(signal, frame):
    sad()
    print("OK BB\n")

# Register the signal handler function for SIGINT signal
signal.signal(signal.SIGQUIT, signal_handler)

while running:
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
    pygame.mouse.set_visible(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not locked:
                # Lock the screen if any key is pressed
                locked = True
                lock_time = time.time()
                passwd_buffer = ""
            else:
                # Store password characters if the screen is already locked
                if event.unicode.isalnum():
                    passwd_buffer += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    passwd_buffer = passwd_buffer[:-1]
                elif event.key == pygame.K_RETURN:
                    if CONF_exit_passwd in passwd_buffer:
                        # Unlock the screen if the correct password is entered
                        locked = False
                        running = False
                        # exit(1)
                        lock_time = 0
                        passwd_buffer = ""
                        break
                # elif event.key == pygame.K_ESCAPE:
                #     # loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
                #     # result = loginPF.SACLockScreenImmediate()
                #     # Exit the program if the user presses ESC
                #     running = False
    if locked:
        # Show the lock screen image for a minute
        screen.blit(lock_screen, (0, 0))
        elapsed_time = time.time() - lock_time
        if elapsed_time > CONF_max_lock_time:
            locked = False
            lock_time = 0
            passwd_buffer = ""
    else:
        # Show a black screen
        screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

    elapsed_time = time.time() - start_time
    if elapsed_time > CONF_max_stay_time:
        # sad()
        running = False
        break
sad()

