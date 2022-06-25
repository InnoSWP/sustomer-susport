from similarity_providers import abs_sim_provider, sus_sim_provider


def test_abs_encode_question():
    encoded = abs_sim_provider.encode_question("What is the strongest muscle in the humans bpdy?")
    assert encoded == ''


def test_abs_similarity():
    first_encoded = abs_sim_provider.encode_question("What is the strongest muscle in the humans bpdy?")
    second_encoded = abs_sim_provider.encode_question("Human's body best muscle")
    assert abs_sim_provider.similarity(first_encoded, second_encoded) == 0


def test_sus_encode_question():
    encoded = sus_sim_provider.encode_question("What is the strongest muscle in the humans bpdy?")
    assert len(eval(encoded)) == 768


def test_sus_similarity():
    first_encoded = sus_sim_provider.encode_question("What is the strongest muscle in the humans bpdy?")
    second_encoded = sus_sim_provider.encode_question("Human's body best muscle")
    assert sus_sim_provider.similarity(first_encoded, second_encoded) > 0.7
