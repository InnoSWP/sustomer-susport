from similarity_providers import abs_sim_provider, sus_sim_provider


QUESTION : str = "What is the strongest muscle in the humans body?"
def test_abs_encode_question():
    encoded = abs_sim_provider.encode_question(QUESTION)
    assert encoded == ''


def test_abs_similarity():
    first_encoded = abs_sim_provider.encode_question(QUESTION)
    second_encoded = abs_sim_provider.encode_question("Human's body best muscle")
    assert abs_sim_provider.similarity(first_encoded, second_encoded) == 0


def test_sus_encode_question():
    encoded = sus_sim_provider.encode_question(QUESTION)
    assert len(eval(encoded)) == 768


def test_sus_similarity():
    first_encoded = sus_sim_provider.encode_question(QUESTION)
    second_encoded = sus_sim_provider.encode_question("Human's body best muscle")
    assert sus_sim_provider.similarity(first_encoded, second_encoded) > 0.7
