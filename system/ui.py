import pygame


# =========================================================
# SCREEN / TIMING
# =========================================================
SCREEN_WIDTH = 1180
SCREEN_HEIGHT = 820
FPS = 60


# =========================================================
# COLORS
# =========================================================
BACKGROUND = (18, 18, 24)

PANEL = (32, 34, 44)
PANEL_ALT = (40, 44, 58)
PANEL_BORDER = (92, 98, 122)

TITLE = (242, 243, 248)
TEXT = (225, 227, 235)
MUTED = (170, 176, 194)

ACCENT = (120, 170, 255)
SUCCESS = (110, 200, 140)
DANGER = (210, 90, 90)
GOLD = (220, 190, 110)

BUTTON = (58, 64, 84)
BUTTON_HOVER = (78, 88, 116)
BUTTON_PRESSED = (48, 54, 72)
BUTTON_BORDER = (132, 144, 184)
BUTTON_TEXT = (245, 246, 250)

INPUT_BG = (28, 30, 40)
INPUT_ACTIVE = (50, 58, 78)


# =========================================================
# SPACING / LAYOUT
# =========================================================
PADDING_SMALL = 10
PADDING = 20
PADDING_LARGE = 30

LINE_SPACING = 6
PARAGRAPH_SPACING = 12

PANEL_RADIUS = 14
BUTTON_RADIUS = 12


# =========================================================
# BACKGROUNDS
# =========================================================
MENU_BACKGROUND = None
NODE_BACKGROUND = None


def set_menu_background(surface):
    global MENU_BACKGROUND
    MENU_BACKGROUND = surface


def set_node_background(surface):
    global NODE_BACKGROUND
    NODE_BACKGROUND = surface


def draw_background(screen, mode="node"):
    if mode == "menu" and MENU_BACKGROUND:
        scaled = pygame.transform.smoothscale(
            MENU_BACKGROUND,
            (screen.get_width(), screen.get_height())
        )
        screen.blit(scaled, (0, 0))
        return

    if mode == "node" and NODE_BACKGROUND:
        scaled = pygame.transform.smoothscale(
            NODE_BACKGROUND,
            (screen.get_width(), screen.get_height())
        )
        screen.blit(scaled, (0, 0))
        return

    screen.fill(BACKGROUND)


# =========================================================
# FONTS
# =========================================================
pygame.font.init()
# later if you add a font file:
# FONT_PATH = "assets/fonts/your_font.ttf"
TITLE_FONT = pygame.font.SysFont("segoe ui", 58, bold=True)
HEADING_FONT = pygame.font.SysFont("segoe ui", 36, bold=True)
BODY_FONT = pygame.font.SysFont("segoe ui", 28)
BUTTON_FONT = pygame.font.SysFont("segoe ui", 28)
SMALL_FONT = pygame.font.SysFont("segoe ui", 22)

CHOICE_FONT = pygame.font.SysFont("segoe ui", 24)

# =========================================================
# PANEL DRAWING
# =========================================================
def draw_panel(
    screen,
    rect,
    fill_color=PANEL,
    border_color=PANEL_BORDER,
    border_width=2,
    radius=PANEL_RADIUS
):
    pygame.draw.rect(screen, fill_color, rect, border_radius=radius)
    pygame.draw.rect(
        screen,
        border_color,
        rect,
        width=border_width,
        border_radius=radius
    )


def draw_text(
    screen,
    text,
    font,
    color,
    x,
    y,
    center=False
):
    surface = font.render(str(text), True, color)
    rect = surface.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(surface, rect)
    return rect


# =========================================================
# WRAPPED TEXT
# =========================================================
def wrap_text_lines(text, font, max_width):
    lines = []
    paragraphs = str(text).split("\n")

    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append("")
            continue

        words = paragraph.split(" ")
        current_line = ""

        for word in words:
            test_line = word if not current_line else current_line + " " + word

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        lines.append("")  # paragraph gap marker

    # remove trailing empty line if it exists
    if lines and lines[-1] == "":
        lines.pop()

    return lines


def get_wrapped_text_height(
    text,
    font,
    max_width,
    line_spacing=LINE_SPACING,
    paragraph_spacing=PARAGRAPH_SPACING
):
    lines = wrap_text_lines(text, font, max_width)
    height = 0

    for line in lines:
        if line == "":
            height += paragraph_spacing
        else:
            height += font.get_height() + line_spacing

    return height


def draw_text_wrapped(
    screen,
    text,
    font,
    color,
    rect,
    line_spacing=LINE_SPACING,
    paragraph_spacing=PARAGRAPH_SPACING,
    scroll_y=0
):
    x, y, width, height = rect
    lines = wrap_text_lines(text, font, width)

    current_y = y + scroll_y

    for line in lines:
        if line == "":
            current_y += paragraph_spacing
            continue

        surface = font.render(line, True, color)
        screen.blit(surface, (x, current_y))
        current_y += font.get_height() + line_spacing

    return current_y


# =========================================================
# BUTTON
# =========================================================
class Button:
    def __init__(
        self,
        rect,
        text,
        style="menu",
        enabled=True
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.style = style
        self.enabled = enabled

        self.hovered = False
        self.pressed = False

        self._apply_style()

    def _apply_style(self):
        if self.style == "menu":
            self.font = BUTTON_FONT
            self.fill_color = BUTTON
            self.hover_color = BUTTON_HOVER
            self.pressed_color = BUTTON_PRESSED
            self.border_color = BUTTON_BORDER
            self.text_color = BUTTON_TEXT
            self.border_width = 2
            self.radius = 14

        elif self.style == "choice":
            self.font = CHOICE_FONT
            self.fill_color = PANEL_ALT
            self.hover_color = BUTTON_HOVER
            self.pressed_color = BUTTON_PRESSED
            self.border_color = BUTTON_BORDER
            self.text_color = BUTTON_TEXT
            self.border_width = 2
            self.radius = 12

        elif self.style == "small":
            self.font = SMALL_FONT
            self.fill_color = BUTTON
            self.hover_color = BUTTON_HOVER
            self.pressed_color = BUTTON_PRESSED
            self.border_color = BUTTON_BORDER
            self.text_color = BUTTON_TEXT
            self.border_width = 2
            self.radius = 10

        else:
            self.font = BUTTON_FONT
            self.fill_color = BUTTON
            self.hover_color = BUTTON_HOVER
            self.pressed_color = BUTTON_PRESSED
            self.border_color = BUTTON_BORDER
            self.text_color = BUTTON_TEXT
            self.border_width = 2
            self.radius = 12

    def update(self, mouse_pos):
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicked = self.pressed and self.rect.collidepoint(event.pos)
            self.pressed = False
            return clicked

        return False


    def draw(self, screen):
        if not self.enabled:
            fill = (50, 52, 60)
            border = (90, 92, 100)
            text_color = (140, 145, 155)
        elif self.pressed:
            fill = self.pressed_color
            border = self.border_color
            text_color = self.text_color
        elif self.hovered:
            fill = self.hover_color
            border = self.border_color
            text_color = self.text_color
        else:
            fill = self.fill_color
            border = self.border_color
            text_color = self.text_color

        pygame.draw.rect(
            screen,
            fill,
            self.rect,
            border_radius=self.radius
        )

        pygame.draw.rect(
            screen,
            border,
            self.rect,
            width=self.border_width,
            border_radius=self.radius
        )

        if self.style == "choice":
            text_rect = pygame.Rect(
                self.rect.x + 14,
                self.rect.y + 9,
                self.rect.width - 28,
                self.rect.height - 18
            )

            ui_lines = wrap_text_lines(self.text, self.font, text_rect.width)

            line_height = self.font.get_height()
            total_text_height = 0
            for line in ui_lines:
                if line == "":
                    total_text_height += 4
                else:
                    total_text_height += line_height + 4

            current_y = text_rect.y + max(0, (text_rect.height - total_text_height) // 2)

            for line in ui_lines:
                if line == "":
                    current_y += 4
                    continue

                surface = self.font.render(line, True, text_color)
                screen.blit(surface, (text_rect.x, current_y))
                current_y += line_height + 4

        else:
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


# =========================================================
# OPTIONAL HELPER: DRAW A SIMPLE STAT BAR
# =========================================================
def draw_game_stat_bar(screen, player, rect):
    draw_panel(
        screen,
        rect,
        fill_color=PANEL_ALT,
        border_color=PANEL_BORDER
    )

    name_text = player.get("name", "Unknown")
    left_text = f"{name_text}"

    right_text = (
        f"K: {player['knowledge']}    "
        f"T: {player['trust']}    "
        f"I: {player['influence']}    "
        f"S: {player['skill']}    "
        f"HP: {player['current_hp']}/{player['max_hp']}"
    )

    draw_text(
        screen,
        left_text,
        SMALL_FONT,
        TITLE,
        rect.x + 16,
        rect.y + 12
    )

    right_surface = SMALL_FONT.render(right_text, True, TEXT)
    right_rect = right_surface.get_rect(
        midright=(rect.right - 16, rect.y + rect.height // 2)
    )
    screen.blit(right_surface, right_rect) 

def center_rect(width, height, screen):
    return pygame.Rect(
        (screen.get_width() - width) // 2,
        (screen.get_height() - height) // 2,
        width,
        height
    )

def draw_separator(screen, rect, y_offset):
    pygame.draw.line(
        screen,
        PANEL_BORDER,
        (rect.x + 24, rect.y + y_offset),
        (rect.right - 24, rect.y + y_offset),
        2
    ) 