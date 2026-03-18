import pygame, sys
from game import button, states, utils, constants, theme


def options_menu(screen):
    pygame.display.set_caption("Menu")
    options_background = pygame.image.load(theme.get_asset("options_background"))
    options_background = pygame.transform.scale(options_background, screen.get_size()).convert()

    options_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("OPTIONS MENU", True, theme.get_color("text_accent"))
    options_text_rect = options_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    set_keybinds_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(250)), 
                             text_input="SET KEYBINDS", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color=theme.get_color("button_base"), hovering_color=theme.get_color("button_hover"))
    set_resolution_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(400)), 
                             text_input="SET RESOLUTION", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color=theme.get_color("button_base"), hovering_color=theme.get_color("button_hover"))
    audio_settings_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(550)), 
                             text_input="AUDIO SETTINGS", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color=theme.get_color("button_base"), hovering_color=theme.get_color("button_hover"))
        
    back_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color=theme.get_color("button_base"), hovering_color=theme.get_color("button_hover"))

    while True:
        
        screen.blit(options_background, (0, 0))

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(theme.get_color("overlay_soft"))
        screen.blit(overlay, (0, 0))

        options_mouse_pos = pygame.mouse.get_pos()

       
        screen.blit(options_text, options_text_rect)

        for b in [set_keybinds_button, back_button, set_resolution_button, audio_settings_button]:
            b.change_color(options_mouse_pos)
            b.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if set_keybinds_button.check_for_input(options_mouse_pos):
                    return states.SET_KEYBINDS
                elif set_resolution_button.check_for_input(options_mouse_pos):
                    return states.SET_RESOLUTION
                elif audio_settings_button.check_for_input(options_mouse_pos):
                    return states.AUDIO_SETTINGS
                elif back_button.check_for_input(options_mouse_pos):
                    return states.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MENU

        pygame.display.flip()

                    


