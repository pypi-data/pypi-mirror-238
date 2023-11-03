import torch
import torchaudio
import wave


# from gxl_ai_utils import AiConstant
# MAX_VOCAB_SIZE = 10000
# MIN_FREQUENCY = 2
# UNK, PAD = '<UNK>', '<PAD>'
# DATA_PATH = AiConstant.DATA_PATH + "text_data/"


# test pass
# def build_vocab(train_path=DATA_PATH + 'train.txt', tokenizer=lambda x: [y for y in x], vocab_size=MAX_VOCAB_SIZE,
#                 min_freq=MIN_FREQUENCY, reserved_tokens=None):
#     if reserved_tokens is None:
#         reserved_tokens = [UNK, PAD]
#     vocab = {}
#     with open(train_path, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             content = line.strip().split('\t')[0]
#             tokens = tokenizer(content)
#             for token in tokens:
#                 if token in vocab:
#                     vocab[token] += 1
#                 else:
#                     vocab[token] = 1
#     sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)[:vocab_size]
#     sorted_vocab = [x for x in sorted_vocab if x[1] > min_freq]
#     vocab_dict = {x[0]: i for i, x in enumerate(sorted_vocab)}
#     for token in reserved_tokens:
#         vocab_dict[token] = len(vocab_dict)
#     return vocab_dict
#
#
# def load_list_from_disk(data_path, vocab, tokenizer, pad_size=40):
#     """文本分类任务中,通过分词器将文本语句转成ids"""
#     contents = []
#     if not os.path.exists(data_path):
#         print(f'error: path does not exist when loading {data_path} datalist')
#         return None
#     with open(data_path, 'r', encoding='UTF-8') as f:
#         for line in tqdm(f):
#             lin = line.strip()
#             if not lin:
#                 continue
#             content, label = lin.split('\t')
#             words_line = []
#             token = tokenizer(content)
#             seq_len = len(token)
#             if pad_size:
#                 if len(token) < pad_size:
#                     token.extend([vocab.get(PAD)] * (pad_size - len(token)))
#                 else:
#                     token = token[:pad_size]
#                     seq_len = pad_size
#             # word to id
#             for word in token:
#                 words_line.append(vocab.get(word, vocab.get(UNK)))
#             # contents.append((words_line, seq_len, int(label)))
#             contents.append((words_line, int(label)))
#     return contents  # [([...], 0,29), ([...], 1,11), ...]
#
#
# def extract_pretrained_embedding_vector(vocab_path, train_path, pretrain_emb_path, emb_save_path, emb_size=300):
#     if os.path.exists(vocab_path):
#         word_to_id = pickle.load(open(vocab_path, 'rb'))
#     else:
#         word_to_id = build_vocab(train_path)
#         pickle.dump(word_to_id, open(vocab_path, 'wb'))
#     embeddings = np.random.rand(len(word_to_id), emb_size)
#     if os.path.exists(pretrain_emb_path):
#         f = open(pretrain_emb_path, 'r', encoding='UTF-8')  # f 好(汉字) 1234423432...(emb_size)
#         for i, line in f.readlines():
#             words = line.strip().split(' ')
#             for word in words:
#                 if word in word_to_id:
#                     embeddings[word_to_id[word]] = np.asarray([float(x) for x in words[1:emb_size + 1]])
#         f.close()
#     np.savez_compressed(emb_save_path, embeddings)
#

def get_sample_count(audio_file_path: str):
    """
    得到路径所指音频的采样点数
    output->
    sample_count: 采样点数
    sample_rate: 采样率
    """
    return _get_sample_count_wave(audio_file_path)


def _get_sample_count_wave(file_path):
    """比较快"""
    with wave.open(file_path, 'rb') as audio_file:
        sample_count = audio_file.getnframes()
        sample_rate = audio_file.getframerate()
    return sample_count, sample_rate


def _get_sample_count_torchaudio(file_path):
    """比较慢"""
    waveform, sr = torchaudio.load(file_path)
    return len(waveform[0]), sr


def get_padding_mask(seq_q: torch.Tensor, seq_k: torch.Tensor, pad_id: int = 0):
    """
    根据seq_k 中pad_id的位置， 得到seq_q对于seq_k的padding_attn_mask,
    seq_q 只是提供q_len,并不影响mask的分布,
    input->
    seq_q: (batch_size, len_q)
    seq_k: (batch_size, len_k)
    output->
    mask: (batch_size, len_q, len_k)
    """
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    mask = seq_k.eq(pad_id)
    mask = mask.unsqueeze(1).expand(batch_size, len_q, len_k)
    return mask


def get_sequence_mask(seq):
    """
    得到一个序列的self-attention的mask
    input->
    seq: [batch_size, seq_len]
    output->
    mask: [batch_size, seq_len, seq_len]
    """
    batch_size, seq_len = seq.size()
    mask = torch.triu(torch.ones((seq_len, seq_len), dtype=torch.uint8, device=seq.device), diagonal=1)
    mask = mask.unsqueeze(0).expand(batch_size, -1, -1)
    return mask
