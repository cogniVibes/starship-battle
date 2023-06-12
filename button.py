import pygame.font

class Play_Button:


    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 225, 60
        self.button_colour = (244,180,27)
        self.text_colour = (255,255,255)
        self.font = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 56)
        
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.screen_rect.width / 2 - 90
        self.rect.y = self.screen_rect.height / 2 - 120

        # Thr button message needs to be prepped only once
        self._prep_msg(msg)


    def _prep_msg(self, msg) -> None:
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                        self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self) -> None:
        # Draw blank button and then draw message.
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Easy_Button:
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 225, 60
        self.button_colour = (244,180,27)
        self.text_colour = (255,255,255)
        self.font = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 56)
            
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.screen_rect.width / 2 - 360
        self.rect.y = self.screen_rect.height / 2

        self._prep_msg(msg)

    def _prep_msg(self, msg) -> None:
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                        self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self) -> None:
        # Draw blank button and then draw message.
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self._prep_msg("EASY")


class Medium_Button:
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 225, 60
        self.button_colour = (244,180,27)
        self.text_colour = (255,255,255)
        self.font = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 56)
            
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.screen_rect.width / 2 - 90
        self.rect.y = self.screen_rect.height / 2

        self._prep_msg(msg)

    def _prep_msg(self, msg) -> None:
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                        self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self) -> None:
        # Draw blank button and then draw message.
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self._prep_msg("MEDIUM")


class Hard_Button:
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 225, 60
        self.button_colour = (244,180,27)
        self.text_colour = (255,255,255)
        self.font = pygame.font.Font("assets/font/3D-Thirteen-Pixel-Fonts.ttf", 56)
            
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = self.screen_rect.width / 2 + 180
        self.rect.y = self.screen_rect.height / 2

        self._prep_msg(msg)

    def _prep_msg(self, msg) -> None:
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour,
                        self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self) -> None:
        # Draw blank button and then draw message.
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self._prep_msg("HARD")
        
