from typing import List


class Tokenizer:
    @staticmethod
    def to_sentences(text: str) -> List[str]:
        return text.split("###SENT###")

    @staticmethod
    def to_words(sentence: str) -> List[str]:
        return [w.strip() for w in sentence.split(" ")]
