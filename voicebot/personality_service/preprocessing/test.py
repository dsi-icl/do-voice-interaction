import nlpaug.augmenter.word as naw
aug1 = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="insert", aug_min=3, aug_max=3)
x=str(aug1.augment("Oh my God, he's lost it. He's totally lost it.")[0])
print(x)
aug2 = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="substitute", aug_min=3, aug_max=3)
y=str(aug2.augment("Oh my God, he's lost it. He's totally lost it.")[0])
print(y)

# print(x.replace(" ' ", "'"))









