import engine
import Vocabulary
import Sentence

if __name__ == "__main__":
    text = engine.read_text_from_file("test.docx")
    voc = engine.process_text(text)
    engine.write_text_to_file("newTest", voc)
    engine.write_vocabulary_to_file(voc, "t")
    tr = engine.read_vocabulary_from_file("t.pkl")
    sen1 = tr.get_sentence_by_id(0)
    print(sen1.get_string())
    print(sen1.get_elements())
    print(sen1.get_tree())
