from random import random

class MarkovChain:
    
    def __init__(self, data):
        self.data = data

    def generate_text(self, max_no_of_chars=140):
        text_words = []
        no_of_chars = 0
        nextWord = "--start--"
        while no_of_chars < max_no_of_chars:
            nextWord = self.generate_next_word(self.model[nextWord])
            if nextWord == "--end--":
                text_words.append(".")
                nextWord = "--start--"
            else:
                text_words.append(nextWord)
            no_of_chars = len(" ".join(text_words).replace(" .", "."))
        text = " ".join(text_words).replace(" .", ".")
        end = text.rfind('.')
        return text[:end+1]

    def generate_next_word(self, word_model):
        r = random()
        for word, probability in word_model:
            if probability > r:
                return word

    def generate_model(self):
        sentences = self.get_sentences()
        words = self.get_words(sentences)
        frequency = self.get_frequencies(words)
        self.model = self.calculate_probability(frequency)

    def calculate_probability(self, frequency_model):
        model = {}
        for word in frequency_model:
            total = sum(frequency_model[word].values())
            cumulative_frequency = []
            for nextWord, frequency in frequency_model[word].items():
                probability = float(frequency)/float(total)
                cumulative_frequency.append([nextWord, probability])
            cumulative_frequency.sort(key = lambda f: f[1])
            for i in range(1, len(cumulative_frequency)):
                cumulative_frequency[i][1] += cumulative_frequency[i-1][1]
            model[word] = cumulative_frequency
        return model

    def get_frequencies(self, words):
        frequency = {}
        for i in range(len(words) - 1):
            word = words[i]
            if word == "--end--":
                continue
            nextWord = words[i+1]
            if word not in frequency:
                frequency[word] = {}
            if nextWord not in frequency[word]:
                frequency[word][nextWord] = 1
            else:
                frequency[word][nextWord] += 1
        return frequency

    def get_sentences(self):
        lines = [line for text in self.data for line in text.splitlines()]
        sentences = [sentence for line in lines
                for sentence in line.split("\s*(.!?)+\s*")]
        table = { ord(i) : None for i in ',.:;!?")('}
        se_sentences = ["--start-- " + sentence.translate(table) + " --end--"
                for sentence in sentences]
        return se_sentences

    def get_words(self, sentences):
        words = [word.lower() for sentence in sentences
                for word in sentence.split()]
        return words
