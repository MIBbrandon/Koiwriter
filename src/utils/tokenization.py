def rules_for_tokens(word: str) -> list[str]:
    """All the words in Koilang only have at most two characters to represent a ripple, 
    and it's either a vowel or "h", so separating a word into tokens that can map to
    the ripples is very straightforward. If the language evolves with more complex rules,
    I recommend switching to using a parser like PEST or something similar.

    Args:
        word (str): Word to tokenize

    Returns:
        List[str]: List of tokens as strings
    """
    def both_chars_go_together(char_before: str, char_now: str) -> bool:
        # CONSONANTS
        # Ending in 'h'
        if char_now == 'h' and char_before in ['c', 'k', 'p', 's', 't', 'v', ]:
            return True
        # Ending in 's'
        if char_now == 's' and char_before in ['t']:
            return True
        
        # VOWELS
        # Ending in 'e'
        if char_now == 'e' and char_before in ['a']:
            return True
        
        # Ending in 'i'
        if char_now == 'i' and char_before in ['a', 'i', 'o']:
            return True
        
        # Ending in 'e'
        if char_now == 'u' and char_before in ['a', 'e']:
            return True

        # None of the previous conditions where met
        return False
    word = word.strip().lower()
    
    tokens = []
    
    # Start at second char
    i = 1
    word_length = len(word)
    last_char_index = word_length - 1
    while i < word_length:
        
        char_before = word[i-1]
        char_now = word[i]
        
        # Add both chars as one token or just add char_before
        if both_chars_go_together(char_before, char_now):
            tokens.append(f'{char_before}{char_now}')
            
            if i + 1 == last_char_index:  # If only one char left after char_now
                tokens.append(word[i+1])  # Just add that last char
                break  # End tokenizing
            else:
                i += 1  # Skip char_now becoming char_before in the next iteration
            
        else:
            tokens.append(char_before)  # Add char normally
            if i == last_char_index:  # If char_now is the last char in the word
                tokens.append(char_now)
        
        i += 1

    # Overwrite single tick to backtick
    for i, t in enumerate(tokens):
        if t == "'":
            tokens[i] = "`"
    
    return tokens