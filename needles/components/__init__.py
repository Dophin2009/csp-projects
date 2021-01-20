"""
Truly awful try at something of a UI toolkit with horrible user ergonomics and
probably terrible performance.

Update: The ergonomics of this are so awful, I regret this.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Dict, Generator, List, Optional, Set

import pygame
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock

from .properties import Box, Dimensions, OverflowMode, Padding, Point


class ComponentBoxes:
    def __init__(self, active: Box, full: Box):
        self.active = active
        self.full = full


class Container:
    def __init__(self, screen: Surface,
                 rg: Register,
                 box: Box,
                 padding=Padding.zero(),
                 overflow=OverflowMode.Ignore()):
        self.screen = screen
        self.rg = rg
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
                rg.register_root(self.child)
                child_boxes = self.child.draw(ctx)

                rg.set_box(self.child.id(), child_boxes, False)

            # Handle events
            for event in pygame.event.get():
                if self._check_quit(event):
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Pass click event to descendants if within the active box.
                    for descendant_entry in rg.yield_for(event.pos):
                        descendant_entry.component.on_click(event)

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
        # Quick-access dictionary of components and their index in
        # nested_follows
        self.components: Dict[str, RegisterEntry] = {}

        # List where each element contains the indexes of that element's
        # children
        self.nested_follows: List[Set[FollowEntry]] = []

        self.overflows: List[str] = []

        self.root = None

    def yield_for(self, p: Point) -> Generator[RegisterEntry, None, None]:
        if self.root is not None:
            root_id = self.root
            root = self.components[root_id]
            if root.boxes.active.contains(p):
                yield root

            queue = Queue()
            queue.put(root.idx)

            # Breadth-first traversal
            while not queue.empty():
                current_idx = queue.get()

                # Yield child component entries
                for child_follow_entry in self.nested_follows[current_idx]:
                    child = self.components[child_follow_entry.id]

                    # Only yield if the point is within the active box of the
                    # component.
                    if child.boxes.active.contains(p):
                        yield child
                        queue.put(child.idx)

            # Yield overflow boxes
            for child_id in self.overflows:
                child = self.components[child_id]
                if child.boxes.active.contains(p):
                    yield child

    def set_box(self, id: str, boxes: ComponentBoxes, overflow: bool):
        self.components[id].boxes = boxes
        if overflow:
            self.overflows.append(id)

    def register_child(self, parent: Component, child: Component,
                       pass_events: bool):
        id = child.id()
        if id in self.components:
            return

        child_idx = self._insert_component(child, pass_events)

        # Find parent idx in nested_follows
        parent_entry = self.components[parent.id()]

        # Push child index to list for parent
        self.nested_follows[parent_entry.idx].add(
            FollowEntry(child_idx, child.id()))

    def register_root(self, child: Component):
        id = child.id()
        if id in self.components:
            return

        self._insert_component(child, True)
        self.root = child.id()

    def _insert_component(self, child: Component, pass_events: bool) -> int:
        id = child.id()

        # Push empty list to nested_follows for children of child
        self.nested_follows.append(set())
        child_idx = len(self.nested_follows) - 1

        # Store in components for quick access by id
        self.components[id] = RegisterEntry(child, child_idx, pass_events)

        return child_idx

    def get_id(self, id: str) -> Optional[RegisterEntry]:
        return self.components[id]


class RegisterEntry:
    def __init__(self, component: Component, idx: int, pass_events: bool):
        self.component = component
        self.idx = idx
        self.boxes: Optional[ComponentBoxes] = None
        self.pass_events = pass_events


class FollowEntry:
    def __init__(self, idx: int, id: str):
        self.idx = idx
        self.id = id
