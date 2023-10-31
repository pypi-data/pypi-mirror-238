from math import isclose
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyformatters_summarizer.summarizer import (
    SummarizerProcessor,
    SummarizerParameters,
    TrfModel,
)


def test_summarizer_french():
    parameters = SummarizerParameters(
        model=TrfModel.camembert2camembert_shared_finetuned_french_summarization
    )
    formatter = SummarizerProcessor()
    original_doc = Document(
        text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
        Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
        L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
        « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
        Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
        Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
        Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
        « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
        Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
        Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
        """
    )
    doc = original_doc.copy(deep=True)
    docs = formatter.process([doc], parameters)
    summary = docs[0].text
    assert len(summary) < len(original_doc.text)

    parameters.as_altText = "summary"
    doc = original_doc.copy(deep=True)
    docs = formatter.process([doc], parameters)
    summarized: Document = docs[0]
    summary = summarized.altTexts[0].text
    assert len(summary) < len(original_doc.text)

    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "summarized.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


def test_summarizer_english():
    parameters = SummarizerParameters(model=TrfModel.pegasus_xsum)
    formatter = SummarizerProcessor()
    original_doc = Document(
        text="""The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris.
    Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930.
    It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft).
    Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.
        """
    )
    doc = original_doc.copy(deep=True)
    docs = formatter.process([doc], parameters)
    summary = docs[0].text
    assert len(summary) < len(original_doc.text)
    assert len(summary) >= parameters.min_length * len(original_doc.text)
    assert isclose(len(summary), parameters.max_length * len(original_doc.text), rel_tol=0.6)

    parameters.as_altText = "summary"
    doc = original_doc.copy(deep=True)
    docs = formatter.process([doc], parameters)
    summarized: Document = docs[0]
    summary = summarized.altTexts[0].text
    assert len(summary) < len(original_doc.text)
    assert len(summary) >= parameters.min_length * len(original_doc.text)
    assert isclose(len(summary), parameters.max_length * len(original_doc.text), rel_tol=0.6)


def test_summarizer_boerhinger():
    parameters = SummarizerParameters(
        model=TrfModel.distilbart_xsum_12_6,
        do_sample=False,
        num_beams=4,
        length_penalty=2.0,
        no_repeat_ngram_size=3,
    )
    formatter = SummarizerProcessor()
    doc = Document(
        text="Adipose tissue development during early life: novel insights into energy balance from small and large mammals\n\nSince the rediscovery of brown adipose tissue (BAT) in adult human subjects in 2007, there has been a dramatic resurgence in research interest in its role in heat production and energy balance. This has coincided with a reassessment of the origins of BAT and the suggestion that brown preadipocytes could share a common lineage with skeletal myoblasts. In precocial newborns, such as sheep, the onset of non-shivering thermogenesis through activation of the BAT-specific uncoupling protein 1 (UCP1) is essential for effective adaptation to the cold exposure of the extra-uterine environment. This is mediated by a combination of endocrine adaptations which accompany normal parturition at birth and further endocrine stimulation from the mother's milk. Three distinct adipose depots have been identified in all species studied to date. These contain either primarily white, primarily brown or a mix of brown and white adipocytes. The latter tissue type is present, at least, in the fetus and, thereafter, appears to take on the characteristics of white adipose tissue during postnatal development. It is becoming apparent that a range of organ-specific mechanisms can promote UCP1 expression. They include the liver, heart and skeletal muscle, and involve unique endocrine systems that are stimulated by cold exposure and/or exercise. These multiple pathways that promote BAT function vary with age and between species that may determine the potential to be manipulated in early life. Such interventions could modify, or reverse, the normal ontogenic pathway by which BAT disappears after birth, thereby facilitating BAT thermogenesis through the life cycle."
    )
    docs = formatter.process([doc], parameters)
    summary = docs[0].text
    assert "Peter Gough" in summary

    parameters = SummarizerParameters(model=TrfModel.distilbart_xsum_12_6)
    docs = formatter.process([doc], parameters)
    summary = docs[0].text
    assert "Peter Gough" not in summary
