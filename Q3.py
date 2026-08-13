"""Q3: Recipe Scaler (Functions)"""

def scale_recipe(name, servings, *ingredients, unit="g", **options):
    if servings < 1:
        print(f"ERROR: '{name}' needs servings >= 1, got {servings}")
        return 0

    print(f"\n=== {name.upper()} (servings: {servings}) ===")
    print("Shopping list:")
    scaled = {}
    for ingredient, amount_per_serving in ingredients:
        amount = amount_per_serving * servings
        scaled[ingredient] = amount
        print(f"  {ingredient}: {amount} {unit}")

    if options:
        print("Cooking notes:")
        for key, value in options.items():
            print(f"  {key}: {value}")

    return scaled


if __name__ == "__main__":
    scale_recipe("Pasta", 4, ("pasta", 100), ("tomato sauce", 200), ("cheese", 50))
    scale_recipe("Smoothie", 2, ("milk", 250), ("yogurt", 100), unit="ml")
    scale_recipe("Cake", 6, ("flour", 200), ("sugar", 150), oven="180C", time="45min")
    scale_recipe("Pizza", 0, ("dough", 250))