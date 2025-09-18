import RadiantCrystal
import pygame
import Inventory
import UIController as ui_controller


# Class for Shopkeeper
class Shopkeeper:
    def __init__(self):
        self.inventory = Inventory()

    def stock_shop(self):
        # Example items in the shop
        self.inventory.add_item("Health Potion", 5)
        self.inventory.add_item("Sword", 3)
        self.inventory.add_item("Armor", 2)

    def display_shop(self):
        print("Shop Inventory:")
        for item, quantity in self.inventory.items.items():
            print(f"{item}: {quantity}")

# Function to handle visiting the shop
def visit_shop(player, shopkeeper):
    ui_controller.draw_text("Welcome to the Shop!", 50, 300)
    shopkeeper.stock_shop()  # Stock the shop with items
    shopkeeper.display_shop()  # Display items for sale
    pygame.display.flip()
    pygame.time.delay(2000)

    ui_controller.draw_text("Select an item to buy:", 50, 350)
    for i, (item, quantity) in enumerate(shopkeeper.inventory.items.items(), start=1):
        ui_controller.draw_text(f"{i}. {item} - ${quantity * 10}", 50, 400 + i * 50)

    pygame.display.flip()

    purchase_choice = None
    while not (purchase_choice and 1 <= int(purchase_choice) <= len(shopkeeper.inventory.items)):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    purchase_choice = pygame.key.name(event.key)

    chosen_item = list(shopkeeper.inventory.items.keys())[int(purchase_choice) - 1]
    item_price = shopkeeper.inventory.items[chosen_item] * 10

    # Check if the player has enough money to make the purchase
    if player.money >= item_price:
        player.money -= item_price
        player.inventory.add_item(chosen_item)
        shopkeeper.inventory.remove_item(chosen_item)
        ui_controller.draw_text(f"You bought {chosen_item} for ${item_price}.", 50, 550)
    else:
        ui_controller.draw_text("You don't have enough money to make the purchase.", 50, 550)

    pygame.display.flip()
    pygame.time.delay(2000)