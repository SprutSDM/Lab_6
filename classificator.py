#encoding: utf8
import string
import math
import scripts

class NaiveBayesClassifier:
    
    def __init__(self, alpha = 1):
        self.alpha = alpha
        return
    

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        targets = list(set(y)) # список состояний
        words = dict() # список слов
        all_targets = dict() # количество слов в этом состоянии
        
        self.targets = targets
        self.words = words
        self.all_targets = all_targets
        
        for _target in targets:
            all_targets[_target] = 0

        for (msg, target) in zip(X, y):
            for word in scripts.morph_analyzer(msg):
                if word not in words: # если видим это слово впервые
                    words[word] = dict()
                    for _target in targets:
                        words[word][_target] = 0 # для каждого состояния количество повторов этого слова = 0
                words[word][target] += 1
                all_targets[target] += 1

        chances = dict() # вероятность встретить слово в этом состоянии
        for word in words:
            chances[word] = dict()
            for target in targets:
                chances[word][target] = (words[word][target] + self.alpha) / (all_targets[target] + self.alpha * len(words))
        self.chances = chances
        
        '''line = [(words[word]['never'], word) for word in words]
        line.sort(reverse=True)
        print(*line, sep='\n')'''

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pre = list()
        for msg in X:
            final_state = None
            final_state_target = ''
            for target in self.targets:
                state = math.log(self.all_targets[target])
                for word in scripts.morph_analyzer(msg):
                    if word in self.words:
                        state += math.log(self.chances[word][target])
                if final_state == None:
                    final_state = state
                    final_state_target = target
                elif state > final_state:
                    final_state = state
                    final_state_target = target
            pre.append(final_state_target)
        return pre
    
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        line = self.predict(X_test)
        cnt = 0
        for i in range(len(y_test)):
            cnt += int(y_test[i] == line[i])
        return cnt / len(y_test)

def test():
    import scripts
    import csv
    with open('SMSSpamCollection.csv') as f:
        data = list(csv.reader(f, delimiter='\t'))
    nbc = NaiveBayesClassifier(0.05)
    X = [scripts.clean(elem[1]) for elem in data]
    y = [elem[0] for elem in data]
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    nbc.fit(X_train, y_train)
    print(nbc.score(X_test, y_test))