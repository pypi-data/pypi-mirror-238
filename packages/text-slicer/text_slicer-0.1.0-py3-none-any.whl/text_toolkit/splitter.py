import re
from .logger import logger  

def split_sentences(text):
    try:    
        # 初始变量设置
        end_positions = [m.end() for m in re.finditer(r"[。？！]", text)]
        sentences = []
        start_idx = 0
        cache = ""  # 用于缓存需要合并的句子

        for end_pos in end_positions:
            # 检查是否有引号紧跟在句子结束标记后面
            if end_pos < len(text) and text[end_pos] == "”":
                end_pos += 1
            sentence = text[start_idx:end_pos]

            # 如果句子包含左引号但不包含右引号，将其缓存以便与下一句合并
            if "“" in sentence and "”" not in sentence:
                cache = sentence
                start_idx = end_pos
                continue
            # 如果缓存不为空，则与当前句子合并
            if cache:
                sentence = cache + sentence
                cache = ""

            sentences.append(sentence)
            start_idx = end_pos

        # 添加最后一句（如果有的话）
        if start_idx < len(text):
            last_sentence = text[start_idx:]
            # 检查最后一句是否应该与前一句合并（例如，因为省略号）
            if last_sentence.startswith("……"):
                sentences[-1] = sentences[-1] + last_sentence
            else:
                sentences.append(last_sentence)

        # 处理省略号，确保它们出现在相关句子的末尾
        refined_sentences = []
        for sentence in sentences:
            if "……" in sentence:
                parts = sentence.split("……")
                for i in range(len(parts) - 1):
                    refined_sentences.append(parts[i] + "……")
                refined_sentences.append(parts[-1])
            else:
                refined_sentences.append(sentence)

        return refined_sentences
    except Exception as e:
            logger.error(f"An error occurred while slice_by_sentence text: {e}")
            raise