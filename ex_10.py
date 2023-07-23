class TestLenOfPhrase():
    def test_len_phrase(self):
        phrase = input("Set a phrase (15 characters or less): ")

        assert len(phrase) <= 15, "Phrase over 15 characters"