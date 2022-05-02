import random
import nltk
nltk.download('words')
from nltk.corpus import words

opts = set([w.lower() for w in words.words() if len(w) == 5])
not_included = ['scaut']
opts = [x for x in opts if x not in not_included]

class Word:
    
    def __init__(self, opts):
        self.contains = []
        self.does_not_contain = [] 
        self.sd = {}
        self.tried_words = []
        self.opts = opts
    
    def add(self, letters):
        self.contains.extend(list(letters))
    
    def subtract(self, letters):
        self.does_not_contain.extend(list(letters))
        
    def check_word(self, word):
        for key in self.sd.keys():
            if word[key] != self.sd[key]:
                return False
        return True
        
    def specify(self, letter, idx):
        self.sd[idx] = letter
        
    def tried(self, word):
        self.tried_words.append(word)
        
    def check_vowel(self, word, threshold=3):
      n = 0
      for l in list('aeious'):
          if l in word:
              n += 1
      return n >= threshold
    
    def vowel_word(self):
      vowel_words =[w for w in opts if check_vowel(w)]
      return random.choice(vowel_words)
    
    def generate_options(self):
        optc = [x for x in self.opts if all([letter in x for letter in self.contains])]
        opts_nc = [x for x in optc if not any([letter in x for letter in self.does_not_contain])]
        
        opts_specific = [x for x in opts_nc if self.check_word(x)]
        opts_specific = [x for x in opts_specific if x not in self.tried_words]
        return opts_specific

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    
    args = parser.parse_args()
    action = args.action
    
    if action == 'new':
      return Word()
