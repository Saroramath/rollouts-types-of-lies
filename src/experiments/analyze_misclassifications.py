import json
from collections import Counter

def analyze_misclassifications(json_file_path):
    """Analyze misclassifications from probe results"""
    
    print(f"Loading results from {json_file_path}...")
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    results = data['results']
    metrics = data['metrics']
    
    print(f"Total samples: {len(results)}")
    print(f"Overall accuracy: {metrics['accuracy']:.4f}")
    print(f"Confusion matrix: {metrics['confusion']}")
    
    # Identify misclassifications
    false_positives = []
    false_negatives = []
    
    for result in results:
        true_label = result['true_label']
        pred_label = result['pred_label']
        
        if true_label == 0 and pred_label == 1:
            # False positive: predicted deceptive but actually not deceptive
            false_positives.append({
                'sample_id': result['sample_id'],
                'user_prompt': result['user_prompt'],
                'model_response': result['model_response'],
                'model_response_mean_score': result['model_response_mean_score'],
                'complete_prompt_mean_score': result['complete_prompt_mean_score']
            })
        elif true_label == 1 and pred_label == 0:
            # False negative: predicted not deceptive but actually deceptive
            false_negatives.append({
                'sample_id': result['sample_id'],
                'user_prompt': result['user_prompt'],
                'model_response': result['model_response'],
                'model_response_mean_score': result['model_response_mean_score'],
                'complete_prompt_mean_score': result['complete_prompt_mean_score']
            })
    
    print(f"\n=== MISCLASSIFICATION ANALYSIS ===")
    print(f"False Positives (FP): {len(false_positives)}")
    print(f"False Negatives (FN): {len(false_negatives)}")
    
    # Analyze false positives
    if false_positives:
        print(f"\n=== FALSE POSITIVES (Predicted Deceptive, Actually Not) ===")
        print(f"Average model response score: {sum(fp['model_response_mean_score'] for fp in false_positives) / len(false_positives):.4f}")
        
        # Show a few examples
        for i, fp in enumerate(false_positives[:5]):
            print(f"\n--- FP Example {i+1} (Sample {fp['sample_id']}) ---")
            print(f"Score: {fp['model_response_mean_score']:.4f}")
            print(f"Prompt: {fp['user_prompt'][:200]}...")
            print(f"Response: {fp['model_response'][:200]}...")
    
    # Analyze false negatives
    if false_negatives:
        print(f"\n=== FALSE NEGATIVES (Predicted Not Deceptive, Actually Deceptive) ===")
        print(f"Average model response score: {sum(fn['model_response_mean_score'] for fn in false_negatives) / len(false_negatives):.4f}")
        
        # Show a few examples
        for i, fn in enumerate(false_negatives[:5]):
            print(f"\n--- FN Example {i+1} (Sample {fn['sample_id']}) ---")
            print(f"Score: {fn['model_response_mean_score']:.4f}")
            print(f"Prompt: {fn['user_prompt'][:200]}...")
            print(f"Response: {fn['model_response'][:200]}...")
    
    # Save misclassifications to separate files for further analysis
    with open('false_positives.json', 'w') as f:
        json.dump(false_positives, f, indent=2)
    
    with open('false_negatives.json', 'w') as f:
        json.dump(false_negatives, f, indent=2)
    
    print(f"\nSaved false positives to: false_positives.json")
    print(f"Saved false negatives to: false_negatives.json")
    
    return false_positives, false_negatives

if __name__ == "__main__":
    json_file = "token_level_scores_gemma2_9b_layer19_labeled.json"
    false_positives, false_negatives = analyze_misclassifications(json_file)
