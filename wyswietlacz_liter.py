#!/usr/bin/env python3
import time

import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FONT_SIZE = 220
LETTER_INTERVAL = 1.0
BREAK_DURATION = 1.0
LOG_FILENAME = "letter_log.txt"
BG_COLOR = (0, 0, 0)
FG_COLOR = (255, 255, 255)

# fmt: off
letters = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "Y", "Z"
]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SUPER FAJNY PROJEKT LITERKOWO")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, FONT_SIZE)

log_file = open(LOG_FILENAME, "a")

state = "show_letter"
next_switch = time.perf_counter()

index = 0
pending_letter = None
pending_start_unix = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    now_perf = time.perf_counter()
    if now_perf >= next_switch:
        if state == "show_letter":
            start_unix = time.time()
            letter = letters[index]

            screen.fill(BG_COLOR)
            surf = FONT.render(letter, True, FG_COLOR)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(surf, rect)
            pygame.display.flip()

            pending_letter = letter
            pending_start_unix = start_unix

            next_switch = now_perf + LETTER_INTERVAL
            state = "breaktime"

            index = (index + 1) % len(letters)

        elif state == "breaktime":
            end_unix = time.time()
            if pending_letter is not None:
                log_file.write(
                    f"{pending_letter}\t{pending_start_unix:.9f}\t{end_unix:.9f}\n"
                )
                log_file.flush()

            pending_letter = None
            pending_start_unix = None

            screen.fill(BG_COLOR)
            pygame.display.flip()

            next_switch = now_perf + BREAK_DURATION
            state = "show_letter"

    clock.tick(60)

if pending_letter is not None:
    exit_unix = time.time()
    log_file.write(f"{pending_letter}\t{pending_start_unix:.9f}\t{exit_unix:.9f}\n")
    log_file.flush()

log_file.close()
pygame.quit()
