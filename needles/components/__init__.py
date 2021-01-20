from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock

from .properties import Box, Dimensions, OverflowMode, Padding


class ComponentBoxes:
    def __init__(self, active: Box, full: Box):
        self.active = active
        self.full = full


class Container:
    def __init__(self, screen: Surface,
                 register: Register,
                 box: Box,
                 padding=Padding.zero(),
                 overflow=OverflowMode.Ignore()):
        self.screen = screen
        self.register = register
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
    def id(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    @abstractmethod
    def draw(self, ctx: Container) -> ComponentBoxes:
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

    def render(self) -> None:
        pygame.init()
        self.loop()
        pygame.quit()

    def loop(self) -> None:
        rg = Register()
        ctx = Container(self.screen, rg, self.content_box(),
                        self.padding, self.overflow)
        while True:
            # Draw the child if it is given
            if self.child is not None:
                self.child.draw(ctx)

            # Handle events
            for event in pygame.event.get():
                if self._check_quit(event):
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Pass click event to descendants if within the active box.
                    if self.child is not None \
                            and self.content_box().contains(event.pos):
                        self.child.on_click(event)
            pygame.display.update()
            self.clock.tick(30)

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
        return event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)


class Register:
    def __init__(self):
        self.components = {}
        self.nested_follows = []
        self.overflown_boxes = []

    def register(self, parent_id: str, child: Component):
        self.nested_follows.append()

        # Store in components dict for quick access
        id = component.id()
        self.components[id] = (component, 0)

    def get_id(self, id: str) -> Optional[Component]:
        return self.components[id]


class Node:
    def __init__(self, children: Optional[List[Node]] = None):
        if children is not None:
            self.children = children
        else:
            self.children = []
            self.children = []
