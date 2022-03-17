from transformers import T5Tokenizer, T5ForConditionalGeneration


def sum_text(texts_set, model_name, max_length=200, no_repeat_ngram_size=3, num_beams=5, top_k=0):
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)

    output_sum = []
    input_ids = tokenizer(
        texts_set,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=max_length
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        no_repeat_ngram_size=no_repeat_ngram_size,
        num_beams=num_beams,
        top_k=top_k
    )

    for ids in output_ids:
        output_sum.append(tokenizer.decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False))

    return output_sum
