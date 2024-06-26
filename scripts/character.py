# Generate a random character
import random

# Expanded lists with over 100 items each
occupations = [
    "wizard", "detective", "scientist", "artist", "explorer", "teacher", "chef", "inventor", "warrior", "healer",
    "archaeologist", "pilot", "swordsman", "gardener", "engineer", "musician", "spy", "alchemist", "jeweler", "blacksmith",
    "carpenter", "philosopher", "surgeon", "astronomer", "magician", "hunter", "mechanic", "ranger", "herbalist", "sailor",
    "merchant", "smith", "monk", "knight", "druid", "ranger", "librarian", "scholar", "artificer", "chronicler",
    "beekeeper", "baker", "butcher", "tinker", "goldsmith", "mason", "cobbler", "merchant", "navigator", "cartographer",
    "puppeteer", "watchmaker", "potter", "bard", "illusionist", "shoemaker", "treasure hunter", "fisherman", "guide",
    "forester", "pathfinder", "bard", "jester", "trainer", "therapist", "visionary", "psychic", "illusionist", "bricklayer",
    "calligrapher", "cleric", "commander", "cryptographer", "diplomat", "diviner", "dreamer", "electro-mechanic", "enchanter",
    "gamekeeper", "harvester", "hearth-keeper", "illuminator", "locksmith", "logician", "mapmaker", "metallurgist", "miner",
    "minstrel", "navigator", "oracle", "pathologist", "peacemaker", "piper", "poet", "prophet", "purveyor", "scribe", "seer",
    "sentinel", "shaman", "soothsayer", "tactician", "tavern keeper", "taxidermist", "thaumaturge", "tinker", "tracker", "translator",
    "doctor", "nurse", "teacher", "lawyer", "programmer", "engineer",
    "police officer", " firefighter", "scientist", "writer", "artist", "musician",
    "athlete", "chef", "farmer", "retail worker", "construction worker", "accountant",
    "dentist", "veterinarian", "pilot", "flight attendant", "architect", " hairstylist",
    "jeweler", "carpenter", "electrician", "plumber", "mechanic", "web developer",
    "graphic designer", "data analyst", "marketing manager", "sales representative",
    "customer service representative", "social worker", "therapist", "researcher",
    "professor", "journalist", "photographer", "translator", "editor", "actor",
    "director", "singer", "dancer", "politician", "entrepreneur", "astronaut",
    "marine biologist", "paleontologist", "astrophysicist", "geologist", "forester",
    "veterinarian technician", "dental hygienist", "medical assistant", "paralegal",
    "administrative assistant", "executive assistant", "human resources specialist",
    "logistics coordinator", "inventory control specialist", "quality control inspector",
    "warehouse worker", "truck driver", "bus driver", "taxi driver", "delivery driver",
    "bartender", "waiter/waitress", "chef", " hairstylist", "cosmetologist", "massage therapist",
    "personal trainer", "yoga instructor", " childcare worker", "teacher's aide",
    "security guard", "lifeguard", "janitor", "landscaper", "housekeeper", "pet sitter",
    "dog walker", "crossing guard", "librarian", "museum curator", "park ranger",
    "forest ranger", "firefighter", "police officer", "soldier", "sailor", "marine",
    "airline pilot", "train conductor", "bus driver", "taxi driver", "delivery driver",
    "retail worker", "cashier", "stocker", "customer service representative", " barista"
]

settings = [
    "a bustling city", "a remote village", "a futuristic space station", "an enchanted forest", "a haunted mansion",
    "a serene seaside town", "a snowy mountain village", "a desert oasis", "a crowded medieval market", "a hidden underground city",
    "a high-tech metropolis", "a distant alien planet", "a magical academy", "a floating sky island", "a cursed battlefield",
    "a vibrant coral reef", "a bustling port town", "a serene forest glade", "a remote arctic research station", "a busy ancient port",
    "a mysterious abandoned temple", "a quaint cottage in the woods", "a grand royal palace", "a futuristic research lab", "a hidden waterfall",
    "a dense jungle", "a sunken city", "an ancient ruins", "a futuristic underwater base", "a massive spaceship", "a sprawling desert city",
    "a hidden mountain fortress", "a tranquil monastery", "a modern metropolis", "a bustling carnival", "a majestic castle",
    "a mysterious cave system", "a floating fortress", "a shadowy alleyway", "a rustic farmstead", "a futuristic megacity",
    "a mystical floating island", "a lost pirate ship", "a frozen tundra", "a busy spaceport", "a verdant rainforest", "a sunlit meadow",
    "a mystical enchanted castle", "a futuristic virtual reality world", "a windswept desert", "a magical labyrinth", "a high-tech floating city",
    "a serene lakeside cabin", "a haunted graveyard", "a bustling airship", "a foggy swamp", "a sparkling fairy tale castle",
    "a lively medieval tavern", "a futuristic hovercar garage", "a mystical library", "a mysterious observatory", "a towering mountain peak",
    "a haunted forest", "a futuristic orbital station", "a floating market", "a glittering crystal cavern", "a mysterious time-warped city",
    "a tranquil zen garden", "a bustling coastal resort", "a rugged frontier town", "a lush vineyard", "a high-tech robotics lab",
    "a sprawling underground city", "a serene beachside town", "a shadowy fortress", "a futuristic agricultural dome", "a mystical cave sanctuary",
    "a vibrant marketplace", "a remote island", "a moonlit forest", "a hidden castle", "a mysterious foggy moor", "a bright carnival",
    "a futuristic observation deck", "a shadowy ancient library", "a sun-dappled forest clearing", "a quaint harbor town", "a hidden sanctuary",
    "a grand bazaar", "a futuristic cargo ship", "a tranquil monastery", "a bustling cyber market", "a misty waterfall", "a vibrant coral reef",
    "a shadowy lair", "a mystical tower", "a sparkling ice palace", "a bustling urban street market", "a serene orchard", "a mysterious ancient crypt",
    "hospital", "clinic", "school", "courthouse", "office building", "factory",
    "police station", "fire station", "laboratory", "library", "art studio", "concert hall",
    "stadium", "restaurant", "farm", "grocery store", "construction site", "accounting firm",
    "dental office", "veterinarian clinic", "airplane", "airport terminal", "architectural firm",
    "hair salon", "jewelry store", "workshop", "power plant", "building site", "auto repair shop",
    "web development agency", "design studio", "data analysis firm", "marketing agency",
    "sales office", "call center", "social service agency", "therapy office", "university",
    "newspaper office", "photography studio", "translation agency", "publishing house",
    "movie set", "theater stage", "recording studio", "dance studio", "government building",
    "startup office", "spaceship", "underwater research station", "museum", "national park",
    "rainforest", "construction site", "dental office", "doctor's office", "law firm",
    "secretary's office", "manager's office", "human resources department", "warehouse",
    "shipping yard", "factory floor", "delivery truck", "restaurant kitchen", "bar",
    "dining room", "cafe", "hair salon", "spa", "gym", "yoga studio", "daycare center",
    "classroom", "security office", "beach", "pool", "office building", "residential home",
    "pet store", "park", "library", "museum exhibit", "forest", "mountain range",
    "fire station", "police station", "military base", "warship", "submarine", "cockpit",
    "train station", "bus terminal", "retail store", "coffee shop"
]

traits = [
    "brave", "curious", "mysterious", "gentle", "cunning", "friendly", "adventurous", "resourceful", "wise", "clever",
    "determined", "charismatic", "inventive", "tenacious", "compassionate", "bold", "patient", "loyal", "ambitious", "intuitive",
    "energetic", "meticulous", "thoughtful", "perceptive", "pragmatic", "dedicated", "charming", "resilient", "enthusiastic", "stoic",
    "courageous", "empathetic", "visionary", "idealistic", "methodical", "gregarious", "honest", "imaginative", "kind", "loyal",
    "dynamic", "practical", "altruistic", "sincere", "optimistic", "tactful", "humble", "forthright", "passionate", "innovative",
    "insightful", "analytical", "cheerful", "disciplined", "humorous", "open-minded", "versatile", "reliable", "strategic", "compassionate",
    "observant", "inquisitive", "courteous", "daring", "generous", "trustworthy", "considerate", "conscientious", "intellectual", "dedicated",
    "astute", "engaging", "diligent", "fearless", "modest", "quick-witted", "spontaneous", "spirited", "adaptable", "thoughtful",
    "vivacious", "benevolent", "determined", "dynamic", "elegant", "innovative", "vigilant", "brilliant", "tactful", "shrewd",
    "diplomatic", "amiable", "articulate", "enterprising", "genuine", "independent", "perceptive", "purposeful", "resolute", "studious",
    "sympathetic", "vivacious", "well-rounded", "zealous", "affable", "attentive", "bright", "capable", "devoted", "gracious"
]

items = [
    "a magical amulet", "an ancient book", "a futuristic gadget", "a mysterious map", "a legendary sword", "a powerful staff", "a sacred relic", 
    "an enchanted ring", "a mystical crystal", "a rare potion", "a high-tech device", "a hidden diary", "a glowing orb", "a protective shield",
    "a precious gemstone", "a secret scroll", "a mystical compass", "a unique artifact", "a cryptic manuscript", "a blessed charm", "a shimmering cloak",
    "an ornate dagger", "a mechanical watch", "an arcane tome", "a celestial telescope", "a futuristic visor", "a rare herb", "a magical mirror",
    "a mysterious key", "a divine artifact", "a legendary bow", "an ancient coin", "a futuristic communicator", "a mystical pendant", "a hidden chest",
    "a powerful elixir", "a celestial map", "an enchanted lantern", "a high-tech toolkit", "a protective talisman", "a mystical gemstone", "a legendary armor",
    "a sacred icon", "a futuristic hologram", "an ancient scroll", "a mystical sword", "a powerful artifact", "a unique potion", "a magical artifact",
    "a futuristic weapon", "a mysterious artifact", "a sacred text", "a high-tech armor", "an enchanted bracelet", "a divine relic", "a mystical scepter",
    "a futuristic drone", "a legendary shield", "a hidden relic", "a powerful charm", "a glowing crystal", "a magical staff", "a secret weapon",
    "a mystical tablet", "a futuristic scanner", "an enchanted weapon", "a divine book", "a rare artifact", "a unique relic", "a high-tech device",
    "a powerful orb", "a mystical artifact", "a sacred weapon", "an enchanted necklace", "a futuristic gadget", "a legendary blade", "a mystical scroll"
]

# Define character attributes
traits = ["brave", "curious", "mysterious", "gentle", "cunning", "friendly", "adventurous", "resourceful"]
rendering_styles = [
#    "realistic",
    "illustration",
    "airbrush",
#    "photograph realism",
    "cartoonish",
    "anime",
#    "sketch",
    "vinyl style",
#    "film poster",
    "comic book",
    "3d image",
    "Pixar --ar 1:2 --stylize 750, 4K resolution highlights, Sharp focus, octane render, ray tracing, Ultra-High-Definition, 8k, UHD, HDR, (Masterpiece:1.5), (best quality:1.5)",
]

brands = ["The North Face", "Off-White", "Yeezy", "Stussy", "Patagonia", "Champion", "Supreme", "Air Jordan"]
clothing_types = ["puffer jacket", "hoodie", "denim jacket", "fleece vest", "bucket hat", "sports jersey",
                  "sweatshirt", "windbreaker", "cargo pants", "leggings", "skinny jeans", "mom jeans"]
colors = ["black", "white", "beige", "blue", "red", "yellow", "purple", "green"]
accessories = ["sunglasses", "hat", "backpack", "jewelry", "headphones"]

def generate_random_urban_character():
    # Generate random person description
    gender = "man"
    hair_style = random.choice(["shaved head", "fade haircut", "crew cut", "short fade haircut", "neatly trimmed beard", "vibrant dyed hair"])
    expression = random.choice(["confident", "friendly", "determined", "thoughtful", "playful", "mischievous"])

    # Generate random outfit description
    top_layer = f"{random.choice(colors)} {random.choice(brands)} {random.choice(clothing_types)}"
    if random.random() < 0.5:  # 50% chance of layering
      mid_layer = f"{random.choice(colors)} button-down shirt" if random.random() < 0.5 else f"graphic tee"
    else:
      mid_layer = ""
    bottom_layer = f"{random.choice(colors)} {random.choice(clothing_types)}"
    shoes = f"{random.choice(colors)} {random.choice(brands)} {random.choice(['sneakers', 'boots'])}"

    # Generate random accessories (optional)
    accessories_list = []
    if random.random() < 0.3:  # 30% chance of having accessories
      num_accessories = random.randint(1, 2)
      for _ in range(num_accessories):
        accessories_list.append(random.choice(accessories))
    accessories_text = ", ".join(accessories_list) if accessories_list else ""

    # Generate random city environment
    environment = random.choice(["bustling city street", "sun-drenched park path", "historic district", "vibrant city square", "rooftop overlooking the city skyline", "hidden alleys"])

    # Combine all elements into the prompt
    prompt = f"A {gender} with {hair_style} and a {expression} expression, sporting {top_layer}"
    if mid_layer:
      prompt += f" over {mid_layer}"
    prompt += f", {bottom_layer}, and {shoes}. {accessories_text} They are {random.choice(['walking', 'skateboarding', 'dancing', 'sipping coffee', 'leaning against a wall'])} in a {environment}."
    return prompt

def generate_random_character():
    occupation = random.choice(occupations)
    setting = random.choice(settings)
    trait = random.choice(traits)
    item = random.choice(items)
    rendering_style = random.choice(rendering_styles)
    
    #character = generate_random_urban_character()
    #character = karen_with_cat()

    #prompt = (
        # f"Create a {rendering_style} style {gender}, who is a {trait} {occupation} located in {setting}."
        #f"{rendering_style} style {character}."
    #)
    prompt = generate_hairstyle_prompt()

    return prompt


def karen_with_cat():
    spirited_away_scenes = [
    "outskirt of Japanese countryside with small old houses",
    "nighttime on the outskirt of Japanese countryside with small old houses",
    "out-of-focus train station",
    "Streets of Malaysia",
    "Streets of Malaysia"
    ]
    scene = random.choice(spirited_away_scenes)
    prompt = (
        f"a cute girl with a gray and white Persian cat with big eyes. whimsical expression. The background is {scene}."
    )
    return prompt


def generate_hairstyle_prompt():
    shot_types = ["closeup", "profile view", "three-quarter view", "overhead shot"]
    hair_types = ["curly", "straight", "wavy", "coily", "kinky", "fine", "thick"]
    hair_lengths = ["short", "medium", "long", "pixie cut", "shoulder-length"]
    hair_colors = ["salt and pepper", "grey"]
    hair_styles = [
        "bob", "asymmetrical cut", "undercut", "pompadour", "bun", "braids",
        "dreadlocks", "bangs", "side part", "top knot", "shag"
    ]
    hair_textures = ["", "silky", "frizzy", "smooth", "voluminous", "sleek"]
    styling_elements = ["", "highlights", "lowlights"]

    prompt = (
        f"66 year old Asian female, {random.choice(shot_types)}, "
        "high-resolution portrait, "
        f"{random.choice(hair_types)} hair, {random.choice(hair_lengths)} length, "
        f"{random.choice(hair_colors)}, {random.choice(hair_styles)}, "
        f"{random.choice(hair_textures)}, {random.choice(styling_elements)}, "
        "professional photography, studio lighting, fashion magazine aesthetic"
    )
    return prompt


# Generate multiple prompts
if __name__ == "__main__":
    for _ in range(5):
        print(generate_random_character())
        print()
