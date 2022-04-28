import engine
import Vocabulary
import Sentence

if __name__ == "__main__":
    text = engine.read_text_from_file("test.docx")
    voc = engine.process_text(text)
    engine.write_text_to_file("newTest", voc)