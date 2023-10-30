from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_restore_punctuation.restore_punctuation import (
    RestorePunctuationProcessor,
    RestorePunctuationParameters, PunctuationModel,
)


def test_model():
    model = RestorePunctuationProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == RestorePunctuationParameters


def test_restore_punctuation_fr():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/CNRRENC_013.txt")

    with source.open("r") as fin:
        text = fin.read()
        processor = RestorePunctuationProcessor()
        parameters = RestorePunctuationParameters(model=PunctuationModel.punctuation_fullstop_truecase_romance)
        docs = processor.process([Document(text=text)], parameters)
        json_file = Path(testdir, "data/CNRRENC_013_noseg.json")
        dl = DocumentList(__root__=docs)
        with json_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)

        parameters = RestorePunctuationParameters(model=PunctuationModel.punctuation_fullstop_truecase_romance, sentences=True)
        docs = processor.process([Document(text=text)], parameters)
        json_file = Path(testdir, "data/CNRRENC_013_seg.json")
        dl = DocumentList(__root__=docs)
        with json_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
