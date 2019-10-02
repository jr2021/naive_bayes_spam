import os

ZERO = 0.00001


def get_occurrences(filename):
    results = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                count, word = line.strip().split(' ')
                results[word] = int(count)

        return results

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s" % str(e))
        raise


def get_words(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            words = [word for line in file for word in line.split()]

        return words

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


def total(dictionary):
    ret = 0
    for value in dictionary.values():
        ret += value
    return ret


class SpamHam:
    """ Naive Bayes spam filter
        :attr spam: dictionary of occurrences for spam messages {word: count}
        :attr ham: dictionary of occurrences for ham messages {word: count}
    """

    def __init__(self, spam_file, ham_file):
        self.spam = get_occurrences(spam_file)
        self.ham = get_occurrences(ham_file)
        self.spam_total = total(self.spam)
        self.ham_total = total(self.ham)

    def evaluate_from_file(self, filename):
        words = get_words(filename)
        return self.eval(words)

    def evaluate_from_input(self):
        words = input().split()
        return self.eval(words)

    def given(self, word, spam):
        try:
            if spam:
                return self.spam[word] / self.spam_total
            else:
                return self.ham[word] / self.ham_total
        except Exception:
            return ZERO

    def eval(self, words):
        r = 1
        for word in words:
            r *= (self.given(word, True) / self.given(word, False))
        return r / (r + 1)
