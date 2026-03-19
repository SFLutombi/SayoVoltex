import pygame
from game import theme


class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.source_image = image
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.is_hovered = False
		self.uses_generated_panel = self.source_image is None and self.text_input != ""
		self.text = None
		self.rect = None
		self.text_rect = None
		self._refresh_visuals()

	def _build_panel_surface(self):
		text_width = self.text.get_width()
		text_height = self.text.get_height()
		padding_x = max(20, text_height)
		padding_y = max(12, text_height // 2)
		width = text_width + padding_x * 2
		height = text_height + padding_y * 2

		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		shadow_color = theme.get_color("button_shadow")
		fill_color = theme.get_color("button_fill_hover") if self.is_hovered else theme.get_color("button_fill")
		border_color = theme.get_color("button_border_hover") if self.is_hovered else theme.get_color("button_border")

		shadow_rect = pygame.Rect(0, 4, width, height - 4)
		body_rect = pygame.Rect(0, 0, width, height - 4)
		accent_rect = pygame.Rect(0, 0, max(8, width // 18), height - 4)

		pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=18)
		pygame.draw.rect(surface, fill_color, body_rect, border_radius=18)
		pygame.draw.rect(surface, border_color, body_rect, width=2, border_radius=18)
		pygame.draw.rect(surface, border_color, accent_rect, border_radius=18)
		return surface

	def _refresh_visuals(self):
		text_color = self.hovering_color if self.is_hovered else self.base_color
		self.text = self.font.render(self.text_input, True, text_color)

		if self.uses_generated_panel:
			self.image = self._build_panel_surface()
		elif self.source_image is not None:
			self.image = self.source_image
		else:
			self.image = self.text

		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		screen.blit(self.image, self.rect)
		if self.text_input != "":
			screen.blit(self.text, self.text_rect)

	# Check if mouse is on the button
	def check_for_input(self, position):
		return self.rect.collidepoint(position)
	
	def change_color(self, position):
		new_hover_state = self.rect.collidepoint(position)
		if new_hover_state != self.is_hovered:
			self.is_hovered = new_hover_state
			self._refresh_visuals()
		elif self.uses_generated_panel is False and self.text_input != "":
			text_color = self.hovering_color if new_hover_state else self.base_color
			self.text = self.font.render(self.text_input, True, text_color)
			self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def change_image(self, new_image):
		self.source_image = new_image
		self.uses_generated_panel = self.source_image is None and self.text_input != ""
		self._refresh_visuals()

	def set_position(self, center):
		self.x_pos, self.y_pos = center
		self.rect.center = center
		self.text_rect.center = center
