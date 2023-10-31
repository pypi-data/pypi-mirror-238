import torch

def EMOLoss(logits: torch.Tensor, labels: torch.Tensor, cost_embedding: torch.Tensor, ignore_index=-100, mode=1) -> torch.Tensor:
    """
    Args:
        logits (Tensor, requried): the output logits after lm_head, before applying softmax
        labels (Tensor, required): the ground truth next tokens
        cost_embedding (Tensor, required): the cost embedding used to compute the transport cost between individual pairs of tokens
        ignore_index (Tensor, optional): usually set to -100 as in nn.CrossEntropyLoss
        mode (Int, optional): 1 by default, it means putting more weight on the MLE loss. Setting mode=2 will put more emphasis on EMO loss. 
    Shape:
        - logits: (batch_size, seq_len, vocab_size) 
        - labels: (batch_size, seq_len)
        - cost_embedding: (vocab_size, hidden_size)
    """
    # ======================================================================== #
    #                   Compute the MLE loss
    # ======================================================================== #
    mask = labels[:, 1:].contiguous().view(-1)
    mask = (mask!=ignore_index).to(logits.dtype)
    loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
    logits = logits[:, :-1, :].contiguous().view(-1, logits.shape[-1])
    labels = labels[:, 1:].contiguous().view(-1)
    mle_loss = loss_fct(logits, labels)

    # ======================================================================== #
    #                   Compute the EMO loss
    # ======================================================================== #
    labels_tmp = labels.clone()
    labels_tmp[labels_tmp==(ignore_index)] = 0
    one_hot = torch.nn.functional.one_hot(labels_tmp, num_classes=logits.shape[-1]).to(logits.dtype)
    stable_onehot = (one_hot+1e-15) / torch.linalg.vector_norm((one_hot+1e-15), ord=1, dim=-1, keepdim=True) # (bsz*seq_len, vocab_size)
    embedding_matrix = cost_embedding # (vocab_size, hidden_size)
    embedding_matrix = embedding_matrix / torch.linalg.vector_norm(embedding_matrix, ord=2, dim=1, keepdim=True)
    p_contextual_repr = stable_onehot @ embedding_matrix # (bsz*seq_len, hidden_size)
    q_grad = torch.log_softmax(logits, dim=-1).exp() # (bsz*seq_len, vocab_size)
    q_contextual_repr = q_grad @ embedding_matrix # (bsz*seq_len, hidden_size)
    emo_loss = (1 - torch.sum(p_contextual_repr*q_contextual_repr, dim=-1)) # (bsz*seq_len,)
    emo_loss = emo_loss * mask

    # ======================================================================== #
    #                   Compose the final loss
    # ======================================================================== #
    if mode == 1:
        loss = (torch.min((mle_loss / (emo_loss+1e-10)).detach(), torch.ones_like(mle_loss, dtype=mle_loss.dtype, device=mle_loss.device)*3.0) * emo_loss + mle_loss) * 0.5
    else:
        loss = ((emo_loss / (mle_loss+1e-10)).detach() * mle_loss + emo_loss) * 0.5
    loss = (loss * mask).sum() / (1e-15 + mask.sum())
    return loss