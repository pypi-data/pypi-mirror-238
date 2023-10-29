
hidden_state_size = 768

class Classifier(torch.nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.num_labels = num_labels
        self.bert = AutoModel.from_pretrained(model_name)
        for param in self.bert.parameters():
            param.requires_grad = False
        self.pre_classifier = torch.nn.Linear(hidden_state_size, 4*hidden_state_size)
        self.gelu = torch.nn.GELU()
        self.dropout = torch.nn.Dropout(0.1)
        self.classifier = torch.nn.Linear(4*hidden_state_size, num_labels)

    def forward(self, input_ids, attention_mask, token_type_ids, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = outputs[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = self.gelu(pooler)
        pooler = self.dropout(pooler)
        logits = self.classifier(pooler)

        loss = None
        if labels is not None:
            loss_fct = CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
