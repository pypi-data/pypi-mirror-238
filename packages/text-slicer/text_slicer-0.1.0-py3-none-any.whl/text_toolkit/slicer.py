# text_toolkit\slicer.py
from .splitter import split_sentences
from .cleaner import clean_text
from .logger import logger 

def slice_by_sentence(text, chunk_size=200):
    if chunk_size < 200:
        raise ValueError("The chunk_size parameter cannot be less than 200.")
    try:  
        clean_text(text)
        sentences = split_sentences(text)
        chunks = []
        chunk = ""
        length = 0

        for sentence in sentences:
            if length + len(sentence) <= chunk_size:
                chunk += sentence
                length += len(sentence)
            else:
                chunks.append(chunk)
                chunk = sentence
                length = len(sentence)

        if chunk:
            chunks.append(chunk)

        return chunks
    except Exception as e:
            logger.error(f"An error occurred while slice_by_sentence text: {e}")
            raise