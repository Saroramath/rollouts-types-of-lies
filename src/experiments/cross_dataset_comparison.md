# Cross-Dataset Performance Comparison

## Overall Performance Comparison

| Dataset | Accuracy | Precision | Recall | F1 | TP | TN | FP | FN |
|---------|----------|-----------|--------|----|----|----|----|----|
| Labeled | 0.8890 | 0.8048 | 0.8879 | 0.8443 | 301 | 588 | 73 | 38 |
| Dishonest Labeled | 0.9290 | 0.9290 | 1.0000 | 0.9632 | 929 | 0 | 71 | 0 |
| Reward Labeled | 0.8150 | 0.8097 | 0.9239 | 0.8631 | 583 | 232 | 137 | 48 |
| Threat Labeled | 0.7180 | 0.6731 | 0.9176 | 0.7765 | 490 | 228 | 238 | 44 |

## Key Observations

- **Best performing dataset**: Dishonest Labeled (Accuracy: 0.9290)
- **Worst performing dataset**: Threat Labeled (Accuracy: 0.7180)
- **Performance range**: 0.7180 - 0.9290

## False Positive Analysis

| Dataset | FP Count | FP Rate |
|---------|----------|----------|
| Labeled | 73 | 0.0730 |
| Dishonest Labeled | 71 | 0.0710 |
| Reward Labeled | 137 | 0.1370 |
| Threat Labeled | 238 | 0.2380 |

## False Negative Analysis

| Dataset | FN Count | FN Rate |
|---------|----------|----------|
| Labeled | 38 | 0.0380 |
| Dishonest Labeled | 0 | 0.0000 |
| Reward Labeled | 48 | 0.0480 |
| Threat Labeled | 44 | 0.0440 |

## Dataset-Specific Insights

### Labeled
- **Accuracy**: 0.8890
- **False Positives**: 73 (7.3%)
- **False Negatives**: 38 (3.8%)
- **FP Score Range**: 0.0175 to 4.6348
- **FP Average Score**: 1.3269
- **FN Score Range**: -1.6688 to -0.0634
- **FN Average Score**: -0.8774

### Dishonest Labeled
- **Accuracy**: 0.9290
- **False Positives**: 71 (7.1%)
- **False Negatives**: 0 (0.0%)
- **FP Score Range**: 2.1732 to 5.5225
- **FP Average Score**: 3.6821

### Reward Labeled
- **Accuracy**: 0.8150
- **False Positives**: 137 (13.7%)
- **False Negatives**: 48 (4.8%)
- **FP Score Range**: 0.0015 to 2.7309
- **FP Average Score**: 1.0894
- **FN Score Range**: -0.9906 to -0.0255
- **FN Average Score**: -0.2333

### Threat Labeled
- **Accuracy**: 0.7180
- **False Positives**: 238 (23.8%)
- **False Negatives**: 44 (4.4%)
- **FP Score Range**: 0.0030 to 2.9135
- **FP Average Score**: 0.7942
- **FN Score Range**: -0.4445 to -0.0012
- **FN Average Score**: -0.1507

## Cross-Dataset Pattern Analysis

### Label Ambiguity Analysis

**Labeled**:
- False Positive Rate: 7.3%
- False Negative Rate: 3.8%
- Total Error Rate: 11.1%

**Dishonest Labeled**:
- False Positive Rate: 7.1%
- False Negative Rate: 0.0%
- Total Error Rate: 7.1%

**Reward Labeled**:
- False Positive Rate: 13.7%
- False Negative Rate: 4.8%
- Total Error Rate: 18.5%

**Threat Labeled**:
- False Positive Rate: 23.8%
- False Negative Rate: 4.4%
- Total Error Rate: 28.2%
- **Note**: High error rate suggests potential label ambiguity

## Recommendations

### For High Error Rate Datasets
- **Threat Labeled**: Consider reviewing label quality and consistency

### For Low Error Rate Datasets
- **Labeled**: Good label quality, can be used as reference
- **Dishonest Labeled**: Good label quality, can be used as reference
