#encoding: utf8
import string

class NaiveBayesClassifier:
    
    def __init__(self, alpha):
        self.alpha = alpha
        return
    

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        targets = list(set(y)) # список состояний
        words = dict() # список слов
        #all_words = dict() # количество встретившихся одинаковых слов
        all_targets = dict() # количество слов в этом состоянии
        cnt = 0 # коли
        for _target in targets:
            all_targets[_target] = 0

        for (msg, target) in zip(X, y):
            for word in msg.split():
                if word not in words: # если видим это слово впервые
                    words[word] = dict()
                    #all_words[word] = 0
                    for _target in targets:
                        words[word][_target] = 0 # для каждого состояния количество повторов этого слова = 0
                words[word][target] += 1
                #all_words[word] += 1
                all_targets[target] += 1
        chances = dict() # вероятность встретить слово в этом состоянии
        for word in words:
            chances[word] = dict()
            for target in targets:
                chances[word][target] = (words[word][target] + self.alpha) / (all_targets[target] + self.alpha * len(words))
        self.chances = chances

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pass
    
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass

train = [
    ('I love this sandwich.', 'pos'),
    ('This is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('This is my best work.', 'pos'),
    ("What an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg') ]
import scripts
nbc = NaiveBayesClassifier(1)
X = [scripts.clean(x[0]) for x in train]
Y = [elem[1] for elem in train]
nbc.fit(X, Y)