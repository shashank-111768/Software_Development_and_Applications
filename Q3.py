

def scale_recipe(name, servings, *ingredients, unit="g", **options):

    if servings < 1:
        print("ERROR:", name, "needs at least 1 serving")
        return {}

    scaled = {}

    for ingredient, amount in ingredients:
        scaled[ingredient] = amount * servings

    print("\n" + name)
    print("Servings:", servings)

    for ingredient in scaled:
        print(
            ingredient + ":",
            scaled[ingredient],
            unit
        )

    if options:
        print("Notes:")

        for key in options:
            print(key + ":", options[key])

    return scaled


if __name__ == "__main__":

    print("Q3: RECIPE SCALER")

    scale_recipe(
        "Pasta",
        4,
        ("pasta", 100),
        ("tomato sauce", 200),
        ("cheese", 50)
    )

    scale_recipe(
        "Smoothie",
        2,
        ("milk", 250),
        ("yogurt", 100),
        unit="ml"
    )

    scale_recipe(
        "Cake",
        6,
        ("flour", 200),
        ("sugar", 150),
        oven="180C",
        time="45min"
    )

    # Invalid serving test
    scale_recipe(
        "Pizza",
        0,
        ("dough", 250)
    )