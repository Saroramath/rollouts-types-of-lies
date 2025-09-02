import json

def analyze_misclassifications_detailed():
    """Detailed analysis of misclassifications with better formatting"""
    
    # Load the misclassification files
    with open('false_positives.json', 'r') as f:
        false_positives = json.load(f)
    
    with open('false_negatives.json', 'r') as f:
        false_negatives = json.load(f)
    
    print("=" * 80)
    print("DETAILED MISCLASSIFICATION ANALYSIS")
    print("=" * 80)
    
    # False Positives Analysis
    print(f"\n🔴 FALSE POSITIVES ({len(false_positives)} cases)")
    print("Predicted: DECEPTIVE | Actually: NOT DECEPTIVE")
    print("-" * 60)
    
    # Group by score ranges
    fp_score_ranges = {
        "High (2.0+)": [],
        "Medium (1.0-2.0)": [],
        "Low (0.0-1.0)": []
    }
    
    for fp in false_positives:
        score = fp['model_response_mean_score']
        if score >= 2.0:
            fp_score_ranges["High (2.0+)"].append(fp)
        elif score >= 1.0:
            fp_score_ranges["Medium (1.0-2.0)"].append(fp)
        else:
            fp_score_ranges["Low (0.0-1.0)"].append(fp)
    
    for range_name, samples in fp_score_ranges.items():
        if samples:
            print(f"\n📊 {range_name}: {len(samples)} samples")
            avg_score = sum(s['model_response_mean_score'] for s in samples) / len(samples)
            print(f"   Average score: {avg_score:.4f}")
            
            # Show a few examples from each range
            for i, sample in enumerate(samples[:3]):
                print(f"\n   Example {i+1} (Sample {sample['sample_id']}):")
                print(f"   Score: {sample['model_response_mean_score']:.4f}")
                print(f"   Prompt: {sample['user_prompt'][:150]}...")
                print(f"   Response: {sample['model_response'][:150]}...")
    
    # False Negatives Analysis
    print(f"\n\n🟡 FALSE NEGATIVES ({len(false_negatives)} cases)")
    print("Predicted: NOT DECEPTIVE | Actually: DECEPTIVE")
    print("-" * 60)
    
    # Group by score ranges
    fn_score_ranges = {
        "Near threshold (-0.5 to 0.0)": [],
        "Low (-1.0 to -0.5)": [],
        "Very low (< -1.0)": []
    }
    
    for fn in false_negatives:
        score = fn['model_response_mean_score']
        if score >= -0.5:
            fn_score_ranges["Near threshold (-0.5 to 0.0)"].append(fn)
        elif score >= -1.0:
            fn_score_ranges["Low (-1.0 to -0.5)"].append(fn)
        else:
            fn_score_ranges["Very low (< -1.0)"].append(fn)
    
    for range_name, samples in fn_score_ranges.items():
        if samples:
            print(f"\n📊 {range_name}: {len(samples)} samples")
            avg_score = sum(s['model_response_mean_score'] for s in samples) / len(samples)
            print(f"   Average score: {avg_score:.4f}")
            
            # Show a few examples from each range
            for i, sample in enumerate(samples[:3]):
                print(f"\n   Example {i+1} (Sample {sample['sample_id']}):")
                print(f"   Score: {sample['model_response_mean_score']:.4f}")
                print(f"   Prompt: {sample['user_prompt'][:150]}...")
                print(f"   Response: {sample['model_response'][:150]}...")
    
    # Summary statistics
    print(f"\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    fp_scores = [fp['model_response_mean_score'] for fp in false_positives]
    fn_scores = [fn['model_response_mean_score'] for fn in false_negatives]
    
    print(f"False Positives:")
    print(f"  - Count: {len(false_positives)}")
    print(f"  - Score range: {min(fp_scores):.4f} to {max(fp_scores):.4f}")
    print(f"  - Average score: {sum(fp_scores)/len(fp_scores):.4f}")
    
    print(f"\nFalse Negatives:")
    print(f"  - Count: {len(false_negatives)}")
    print(f"  - Score range: {min(fn_scores):.4f} to {max(fn_scores):.4f}")
    print(f"  - Average score: {sum(fn_scores)/len(fn_scores):.4f}")
    
    # Identify patterns
    print(f"\n" + "=" * 80)
    print("PATTERN ANALYSIS")
    print("=" * 80)
    
    # Check for common prompt patterns in FPs
    fp_prompts = [fp['user_prompt'] for fp in false_positives]
    common_fp_patterns = {}
    for prompt in fp_prompts:
        if "copied answers" in prompt.lower():
            common_fp_patterns["copied answers"] = common_fp_patterns.get("copied answers", 0) + 1
        if "exaggerated" in prompt.lower():
            common_fp_patterns["exaggerated"] = common_fp_patterns.get("exaggerated", 0) + 1
        if "missed deadline" in prompt.lower():
            common_fp_patterns["missed deadline"] = common_fp_patterns.get("missed deadline", 0) + 1
    
    print(f"Common prompt patterns in False Positives:")
    for pattern, count in sorted(common_fp_patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"  - '{pattern}': {count} cases")
    
    # Check for common prompt patterns in FNs
    fn_prompts = [fn['user_prompt'] for fn in false_negatives]
    common_fn_patterns = {}
    for prompt in fn_prompts:
        if "missed a meeting" in prompt.lower():
            common_fn_patterns["missed a meeting"] = common_fn_patterns.get("missed a meeting", 0) + 1
        if "plagiarized" in prompt.lower():
            common_fn_patterns["plagiarized"] = common_fn_patterns.get("plagiarized", 0) + 1
    
    print(f"\nCommon prompt patterns in False Negatives:")
    for pattern, count in sorted(common_fn_patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"  - '{pattern}': {count} cases")

if __name__ == "__main__":
    analyze_misclassifications_detailed()








