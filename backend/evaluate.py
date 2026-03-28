import time
import requests
from jiwer import wer

API_URL = "http://127.0.0.1:5000/translate"

#  Metrics
def compute_accuracy(gt, pred):
    correct = sum([1 for g, p in zip(gt, pred) if g == p])
    return correct / len(gt) if gt else 0

def precision(gt, pred):
    correct = len(set(gt) & set(pred))
    return correct / len(pred) if pred else 0

def recall(gt, pred):
    correct = len(set(gt) & set(pred))
    return correct / len(gt) if gt else 0

def f1(p, r):
    return 2 * (p * r) / (p + r) if (p + r) else 0

def sequence_accuracy(gt, pred):
    return 1 if gt == pred else 0


results = []

print("\n START TESTING (10 sentences)\n")

for i in range(10):
    print(f"\n--- Sample {i+1} ---")

    input(" Record audio and save as input.wav, then press ENTER...")

    gt_text = input("Enter ACTUAL sentence: ").lower()
    gt_isl = input("Enter expected ISL tokens: ").lower().split()

    #  Send to API (FIXED: using input.wav)
    with open("input.wav", "rb") as f:
        files = {"audio": f}

        start = time.time()
        response = requests.post(API_URL, files=files)
        end = time.time()

    # Safety check
    if response.status_code != 200:
        print("API Error:", response.text)
        continue

    data = response.json()

    #  Extract outputs safely
    pred_text = data.get("text", "").lower()
    pred_isl = data.get("tokens", [])

    print("Predicted Text:", pred_text)
    print("Predicted ISL:", pred_isl)

    #  Metrics
    w = wer(gt_text, pred_text)
    acc = compute_accuracy(gt_isl, pred_isl)
    p = precision(gt_isl, pred_isl)
    r = recall(gt_isl, pred_isl)
    f = f1(p, r)
    lat = end - start
    seq = sequence_accuracy(gt_isl, pred_isl)

    results.append({
        "wer": w,
        "accuracy": acc,
        "precision": p,
        "recall": r,
        "f1": f,
        "latency": lat,
        "sequence": seq
    })


def avg(key):
    return sum(r[key] for r in results) / len(results) if results else 0


print("\n=========== FINAL RESULTS ===========")
print(f"WER: {avg('wer'):.3f}")
print(f"ISL Accuracy: {avg('accuracy'):.3f}")
print(f"Precision: {avg('precision'):.3f}")
print(f"Recall: {avg('recall'):.3f}")
print(f"F1 Score: {avg('f1'):.3f}")
print(f"Latency: {avg('latency'):.3f} sec")
print(f"Sequence Accuracy: {avg('sequence'):.3f}")
print("====================================")