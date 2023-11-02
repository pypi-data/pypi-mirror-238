import re
import time
import datetime
import math
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from collections import Counter
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import pandas as pd

from tqdm.auto import tqdm
from torch.utils.data import DataLoader, Dataset
from utils.KoCharELECTRA.tokenization_kocharelectra import KoCharElectraTokenizer
from model.LSTM_CLS_Model import LSTM_Model, init_weights
# from generate_num import Label2Num

import gc

torch.cuda.empty_cache()
gc.collect()

tokenizer = KoCharElectraTokenizer.from_pretrained("monologg/kocharelectra-base-discriminator")

special_tokens_dict = {'additional_special_tokens': ['<N>', '</N>']}
tokenizer.add_special_tokens(special_tokens_dict)
print(tokenizer.all_special_tokens)
print(tokenizer.all_special_ids)

# 11568, 11569
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class CLSDataset(Dataset):
    def __init__(self, src_path, max_len):
        super(CLSDataset, self).__init__()
        self.src_sents = []
        self.tgt_sents = []
        self.pairs = []
        self.max_len = max_len

        print("TranslationDataset", src_path)

        with open(src_path, 'r', encoding='utf-8') as f:
            for line in f:
                pair = line.strip().split("\t")
                if len(pair) == 3:
                    src_sent, label, tagging = pair

                    # one-hot
                    try:
                        label = int(label)
                        one_hot_label = torch.zeros(10)
                        one_hot_label[label] = 1
                        self.pairs.append((src_sent, one_hot_label, tagging))
                    except:
                        print(f"[data error] {src_sent} -- {label} -- {tagging}")
                else:
                    print("[pair error]", pair)

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        src_sent, labels, tagging = self.pairs[idx]

        # 소스 문장 전처리
        src_ids = tokenizer.encode(src_sent, add_special_tokens=True, max_length=self.max_len, padding='max_length', truncation=True)
        src_tensor = torch.tensor(src_ids)

        return src_tensor, labels, tagging

def train(model, train_data, val_data, optimizer, criterion, device, epochs, clip, patience, batch_size, scheduler, save_path):
    best_loss = float('inf')
    train_losses, val_losses = [], []
    early_stop_count = 0
    df_wrong = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])
    df_correct = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])

    for epoch in range(epochs):
        model.train()
        train_loss = 0

        epoch_iterator = tqdm(train_data, desc=f"Training epoch {epoch+1}/{epochs} loss=X.X", dynamic_ncols=True)
        for index, batch in enumerate(epoch_iterator):
            src_batch, label, tagging = batch
            label = label.float()
            # encode and decode the batch
            src_tensor = src_batch.to(device)
            label = label.to(device)

            optimizer.zero_grad()

            output = model(src_tensor, device)


            loss = criterion(output, label)

            # backpropagation
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
            optimizer.step()

            train_loss += loss.item()

            epoch_iterator.set_description(f"Training epoch {epoch+1}/{epochs} Loss={loss}")


        train_loss /= len(train_data)
        train_losses.append(train_loss)

        # evaluate on validation set
        val_loss, acc, precision, recall, f1, correct_df, wrong_df = evaluate(model, val_data, criterion, batch_size, device)
        val_losses.append(val_loss)

        print(f"Epoch: {epoch+1}, Train Loss: {train_loss:.4f},|"
              f" Val Loss: {val_loss:.4f} Acc : {acc}, Precision : {precision}, Recall : {recall}, F1 : {f1}" )



        # early stopping
        if val_loss < best_loss:
            early_stop_count = 0
            best_loss = val_loss
            torch.save(model.state_dict(), f"{save_path}")
            # # collect predictions and labels
            # predicted_classes = torch.argmax(output, dim=1).cpu().numpy().tolist()
            # true_classes = torch.argmax(label, dim=1).cpu().numpy().tolist()
            # src = src_tensor.cpu().numpy().tolist()
            #
            # # collect correct and wrong predictions
            # for i in range(len(predicted_classes)):
            #     src_decode = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in src[i]],
            #                                   skip_special_tokens=True)
            #     if predicted_classes[i] == true_classes[i]:
            #         df_correct = df_correct.append(
            #             {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i],
            #              'Tagging': tagging[i]},
            #             ignore_index=True)
            #     else:
            #         df_wrong = df_wrong.append(
            #             {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i],
            #              'Tagging': tagging[i]},
            #             ignore_index=True)
            #     # train
            #     df_correct.to_csv("./results/correct_CLS_cnn_train.csv", index=False, encoding='utf-8-sig')
            #     df_wrong.to_csv("./results/wrong_CLS_cnn_train.csv", index=False, encoding='utf-8-sig')
            #
            #     # val
            #     correct_df.to_csv("./results/correct_CLS_cnn_val.csv", index=False, encoding='utf-8-sig')
            #     wrong_df.to_csv("./results/wrong_CLS_cnn_val.csv", index=False, encoding='utf-8-sig')
        else:
            early_stop_count += 1
            print("early_stop_count:", early_stop_count)
            if early_stop_count >= patience:
                print(f"Validation loss didn't improve for {patience} epochs. Training stopped.")
                break

        scheduler.step()

    return train_losses, val_losses


def evaluate(model, dataloader, criterion, batch_size, device):
    """Evaluate the model on validation/test dataset"""
    model.eval()
    total_loss = 0.
    predictions, labels = [], []
    df_wrong = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])
    df_correct = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])

    pbar = tqdm(dataloader, desc="Validation")
    with torch.no_grad():
        for index, batch in enumerate(pbar):
            src, label, tagging = batch
            label = label.float()

            src = src.to(device)
            label = label.to(device)

            output = model(src, device)

            loss = criterion(output, label)
            total_loss += loss.item()

            # collect predictions and labels
            predictions += torch.argmax(output, dim=1).cpu().numpy().tolist()
            labels += torch.argmax(label, dim=1).cpu().numpy().tolist()
            pbar.set_description(f"LOSS = {loss:.4f}")

            # collect predictions and labels
            # predicted_classes = torch.argmax(output, dim=1).cpu().numpy().tolist()
            # true_classes = torch.argmax(label, dim=1).cpu().numpy().tolist()
            # src = src.cpu().numpy().tolist()
            #
            # # collect correct and wrong predictions
            # for i in range(len(predicted_classes)):
            #     src_decode = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in src[i]],
            #                                   skip_special_tokens=True)
            #     if predicted_classes[i] == true_classes[i]:
            #         df_correct = df_correct.append(
            #             {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i],
            #              'Tagging': tagging[i]},
            #             ignore_index=True)
            #     else:
            #         df_wrong = df_wrong.append(
            #             {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i],
            #              'Tagging': tagging[i]},
            #             ignore_index=True)
    print("label :", Counter(labels))
    print("pred :" , Counter(predictions))
    # calculate evaluation metrics
    accuracy = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions, average='weighted')
    recall = recall_score(labels, predictions, average='weighted')
    f1 = f1_score(labels, predictions, average='weighted')

    avg_loss = total_loss / len(dataloader)


    return avg_loss, accuracy, precision, recall, f1, df_correct, df_wrong


def translate_sentence(dataloader, batch_size, model, device):
    model.eval()
    df_wrong = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])
    df_correct = pd.DataFrame(columns=['Source', 'Target', 'Prediction', "Tagging"])

    """Evaluate the model on validation/test dataset"""
    predictions, labels = [], []

    with torch.no_grad():
        for batch in dataloader:
            src, label, tagging = batch
            label = label.float()

            src = src.to(device)
            label = label.to(device)

            output = model(src, device)

            # collect predictions and labels
            predictions += torch.argmax(output, dim=1).cpu().numpy().tolist()
            labels += torch.argmax(label, dim=1).cpu().numpy().tolist()

            # collect predictions and labels
            predicted_classes = torch.argmax(output, dim=1).cpu().numpy().tolist()
            true_classes = torch.argmax(label, dim=1).cpu().numpy().tolist()
            src = src.cpu().numpy().tolist()

            # collect correct and wrong predictions
            for i in range(len(predicted_classes)):
                src_decode = tokenizer.decode([str(x).replace('11568', '412').replace('11569', '413') for x in src[i]], skip_special_tokens=True)
                input_src = tokenizer.decode(src[i])
                if predicted_classes[i] == true_classes[i]:
                    df_correct = df_correct.append(
                        {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i], 'Tagging': tagging[i]},
                        ignore_index=True)
                else:
                    df_wrong = df_wrong.append(
                        {'Source': src_decode, 'Target': true_classes[i], 'Prediction': predicted_classes[i], 'Tagging': tagging[i]},
                        ignore_index=True)


    # 결과 저장
    df_correct.to_excel("./results/correct_CLS_cnn_test.xlsx", index=False, encoding='utf-8-sig')
    df_wrong.to_excel("./results/wrong_CLS_cnn_test.xlsx", index=False, encoding='utf-8-sig')

def inference(data, batch_size, model):
    # INIT LOGGERS
    # start = time.time()
    starter, ender = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
    dummy_input = torch.LongTensor([[1,2, 3]]).to(device)
    repetitions = len(data)
    timings = np.zeros((repetitions, 1))
    model.eval()
    print(dummy_input.shape)
    # GPU WARM UP
    for _ in range(10):
        _ = model(dummy_input, device)

    """Evaluate the model on validation/test dataset"""
    predictions, labels = [], []

    with torch.no_grad():
        for i, batch in enumerate(data):
            starter.record()
            src, label, tagging = batch
            label = label.float()

            src = src.to(device)
            label = label.to(device)

            output = model(src, device)
            ender.record()

            # WAIT FOR GPU SYNC
            torch.cuda.synchronize()
            curr_time = starter.elapsed_time(ender)
            timings[i] = curr_time

            # collect predictions and labels
            # predictions += torch.argmax(output, dim=1).cpu().numpy().tolist()
            # labels += torch.argmax(label, dim=1).cpu().numpy().tolist()

    mean_syn = np.sum(timings) / repetitions
    std_syn = np.std(timings)
    print(mean_syn)

    # end = time.time()
    # sec = (end - start)
    # result = datetime.timedelta(seconds=sec)
    # print("time:", result)
    # print(len(data))


def main():
    print(device)
    # 하이퍼파라미터 설정
    hidden_size = 512 # 512
    embed_size = 512 #
    dropout = 0.3
    num_layers = 2
    batch_size = 64
    learning_rate = 1e-3
    num_epochs = 300
    patience = 10
    max_len = 128
    num_classes = 10

    random_seed = 42
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


    # 데이터셋 생성
    train_data = CLSDataset('data/wo_sp_kt_train.txt', max_len)
    val_data = CLSDataset('data/wo_sp_kt_val.txt', max_len)
    test_data = CLSDataset('data/wo_sp_kt_test.txt', max_len)
    train_sampler = RandomSampler(train_data)
    val_sampler = SequentialSampler(val_data)

    # 데이터로더 생성
    train_loader = DataLoader(train_data, batch_size=batch_size, sampler=train_sampler)
    val_loader = DataLoader(val_data, batch_size=batch_size, sampler=val_sampler)
    test_loader = DataLoader(test_data, batch_size=batch_size)

    src_vocab_size = len(tokenizer.get_vocab())

    model = LSTM_Model(num_classes, src_vocab_size, embed_size, hidden_size, num_layers, dropout, num_filters=32, kernel_size=5)
    print(model)
    model.to(device)
    model.apply(init_weights)

    # 데이터 불균형
    """
    label
    0      76141
    1      19884
    2         56
    3      10965
    4      12699
    5       6296
    6          5
    7     125414
    8        749
    9        209
    10      3689
    """
    # num_ins = [76141, 19884, 56, 10965, 12699, 6296, 125414, 749, 209, 3689]
    # weights = [1 - (x/sum(num_ins)) for x in num_ins]

    # print("weight: ", weights)
    # class_weights = torch.FloatTensor(weights).to(device)
    # criterion = nn.CrossEntropyLoss(weight=class_weights)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    # optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=1e-5)
    criterion = criterion.to(device)

    model.load_state_dict(torch.load("./results/save_model/lstm_model.pt"))

    train(model, train_loader, val_loader, optimizer, criterion, device,
          num_epochs, 1, patience, batch_size, scheduler, save_path="./results/save_model/lstm_kt_model.pt")

    model.load_state_dict(torch.load("./results/save_model/lstm_kt_model.pt"))

    test_loss, acc, precision, recall, f1, _, _ = evaluate(model, test_loader, criterion, batch_size, device)
    print(f'Test Loss: {test_loss:.3f} | Acc : {acc}, Precision : {precision}, Recall : {recall}, F1 : {f1}" ')

    # translate_sentence(test_loader, batch_size, model, device)
    inference(test_loader, batch_size, model)

if __name__ == '__main__':
    main()