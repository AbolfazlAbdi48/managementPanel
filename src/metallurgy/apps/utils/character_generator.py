def random_character_generator(number):
    import random
    # list of characters
    characters = "!#$%123456879qwertyuioplkjhgfdsazxcvbnmASDFGHJKLMNBVCXQWERTYUIOP"
    # random password
    random_characters = "".join(random.sample(characters, number))

    return random_characters
