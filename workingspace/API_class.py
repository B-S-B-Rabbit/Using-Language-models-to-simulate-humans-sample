from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

PRETRAINED = 'workingspace/pretrained'
MAX_REQUEST_LENGTH = 40


def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def infer(inp, model, tokenizer, device) -> str:
    inp = "<startofstring> " + inp + " <bot>: "
    inp = tokenizer(inp, return_tensors="pt")

    unit = inp["input_ids"].to(device)
    a = inp["attention_mask"].to(device)

    output = model.generate(unit, attention_mask=a, max_length=MAX_REQUEST_LENGTH)
    output = tokenizer.decode(output[0])
    return output


def load_pretrained() -> tuple:
    device = get_device()

    tokenizer = GPT2Tokenizer.from_pretrained(PRETRAINED)
    tokenizer.add_special_tokens({"pad_token": "<pad>",
                                  "bos_token": "<startofstring>",
                                  "eos_token": "<endofstring>"})
    tokenizer.add_tokens(["<bot>:"])

    model = GPT2LMHeadModel.from_pretrained(PRETRAINED)
    model.resize_token_embeddings(len(tokenizer))
    model.eval()

    return model, tokenizer, device


class API:
    def __init__(self):
        self.model, self.tokenizer, self.device = load_pretrained()

    def get_bot_answer(self, request: str) -> str:
        result = infer(request, self.model, self.tokenizer, self.device)
        result = result.split("<bot>:")[1]
        result = result.replace("<pad>", '')
        result = result.replace("<endofstring>", '')
        return result
