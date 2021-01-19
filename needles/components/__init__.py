from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock

from .properties import Box, Dimensions, OverflowMode, Padding


class Container:
    def __init__(self, screen: Surface, box: Box,
                 padding=Padding.zero(),
                 overflow=OverflowMode.Ignore()):
        self.screen = screen
        self.box = box

        if padding is not None:
            self.padding = padding
        else:
            self.padding = Padding.zero()

        if overflow is not None:
            self.overflow = overflow
        else:
            self.overflow = OverflowMode.Ignore()

    def content_box(self) -> Box:
        return self.box.shrink(self.padding)


class Component(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def draw(self, ctx: Container):
        """
        Implementations should draw the component on the given screen and at
        the given delta. The screen and modified delta should be passed to any
        nested components.
        """
        pass

    def on_click(self, event: Event) -> None:
        pass


class Window:
    def __init__(self, title: str, dimensions: Dimensions,
                 padding=Padding.zero(),
                 overflow=OverflowMode.Ignore(),
                 child: Optional[Component] = None):
        self.dimensions = dimensions
        self.padding = padding
        self.overflow = overflow

        self.screen = pygame.display.set_mode([600, 600])
        pygame.display.set_caption(title)
        self.clock = Clock()

        self.child = child

    def render(self):
        pygame.init()

        ctx = Container(self.screen, self.content_box(),
                        self.padding, self.overflow)

        exit = False
        while not exit:
            # Draw the child if it is given
            if self.child is not None:
                self.child.draw(ctx)

            # Handle events
            for event in pygame.event.get():
                if self._check_quit(event):
                    exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Pass click event to descendants if within the active box.
                    if self.child is not None \
                            and self.content_box().contains(event.pos):
                        self.child.on_click(event)

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    def box(self) -> Box:
        return Box(0, 0, self.dimensions.w, self.dimensions.h)

    def content_box(self) -> Box:
        return self.box().shrink(self.padding)

    def _check_quit(self, event: Event) -> bool:
        """
        Check if window should stop rendering; returns true if X button clicked
        or <esc> key is pressed.
        """
        return event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
