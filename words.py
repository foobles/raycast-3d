import pygame as pg

pg.font.init()


def get_word_list(file):
    with open(file) as words:
        return words.readlines()


def render_words(surface, font, words, color):
    x, y = 0, 0
    max_width = 0
    for word in words:
        text = font.render(word, False, color)
        max_width = max(max_width, text.get_width())
        if y > surface.get_height():
            y = 0
            x += max_width
            max_width = 0
        surface.blit(text, (x, y))
        y += text.get_height()
