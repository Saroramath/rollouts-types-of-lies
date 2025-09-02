import json

def examine_specific_examples():
    """Examine specific misclassification examples in detail"""
    
    # Load the misclassification files
    with open('false_positives.json', 'r') as f:
        false_positives = json.load(f)
    
    with open('false_negatives.json', 'r') as f:
        false_negatives = json.load(f)
    
    print("=" * 100)
    print("EXAMINING SPECIFIC MISCLASSIFICATION EXAMPLES")
    print("=" * 100)
    
    # Look at some high-scoring false positives
    print(f"\n🔴 HIGH-SCORING FALSE POSITIVES (Score >= 2.0)")
    print("These are cases where the probe strongly predicted deception but was wrong")
    print("-" * 80)
    
    high_fps = [fp for fp in false_positives if fp['model_response_mean_score'] >= 2.0]
    for i, fp in enumerate(high_fps[:5]):
        print(f"\n--- High FP Example {i+1} (Sample {fp['sample_id']}) ---")
        print(f"Score: {fp['model_response_mean_score']:.4f}")
        print(f"Complete Prompt:")
        print(f"  {fp['user_prompt']}")
        print(f"Model Response:")
        print(f"  {fp['model_response']}")
        print(f"Analysis: This response was predicted as deceptive with high confidence")
        print(f"         but the ground truth says it's NOT deceptive.")
    
    # Look at some near-threshold false negatives
    print(f"\n\n🟡 NEAR-THRESHOLD FALSE NEGATIVES (Score >= -0.5)")
    print("These are cases where the probe barely missed detecting deception")
    print("-" * 80)
    
    near_threshold_fns = [fn for fn in false_negatives if fn['model_response_mean_score'] >= -0.5]
    for i, fn in enumerate(near_threshold_fns[:5]):
        print(f"\n--- Near-threshold FN Example {i+1} (Sample {fn['sample_id']}) ---")
        print(f"Score: {fn['model_response_mean_score']:.4f}")
        print(f"Complete Prompt:")
        print(f"  {fn['user_prompt']}")
        print(f"Model Response:")
        print(f"  {fn['model_response']}")
        print(f"Analysis: This response was predicted as NOT deceptive but the ground")
        print(f"         truth says it IS deceptive. The score was close to threshold.")
    
    # Look at some very low-scoring false negatives
    print(f"\n\n🟡 VERY LOW-SCORING FALSE NEGATIVES (Score < -1.0)")
    print("These are cases where the probe was very confident it was NOT deceptive but was wrong")
    print("-" * 80)
    
    low_fns = [fn for fn in false_negatives if fn['model_response_mean_score'] < -1.0]
    for i, fn in enumerate(low_fns[:5]):
        print(f"\n--- Low FN Example {i+1} (Sample {fn['sample_id']}) ---")
        print(f"Score: {fn['model_response_mean_score']:.4f}")
        print(f"Complete Prompt:")
        print(f"  {fn['user_prompt']}")
        print(f"Model Response:")
        print(f"  {fn['model_response']}")
        print(f"Analysis: This response was predicted as NOT deceptive with high confidence")
        print(f"         but the ground truth says it IS deceptive.")
    
    # Look for patterns in the "copied answers" false positives
    print(f"\n\n🔍 PATTERN ANALYSIS: 'COPIED ANSWERS' FALSE POSITIVES")
    print("These cases might reveal why the probe is confused")
    print("-" * 80)
    
    copied_answers_fps = [fp for fp in false_positives if "copied answers" in fp['user_prompt'].lower()]
    print(f"Found {len(copied_answers_fps)} false positives with 'copied answers' prompts")
    
    for i, fp in enumerate(copied_answers_fps[:3]):
        print(f"\n--- 'Copied Answers' FP Example {i+1} (Sample {fp['sample_id']}) ---")
        print(f"Score: {fp['model_response_mean_score']:.4f}")
        print(f"Prompt: {fp['user_prompt']}")
        print(f"Response: {fp['model_response']}")
        print(f"Note: The prompt asks for a student who copied answers, but the response")
        print(f"      shows hesitation/confusion rather than direct admission of copying.")
    
    # Look for patterns in the "missed a meeting" false negatives
    print(f"\n\n🔍 PATTERN ANALYSIS: 'MISSED A MEETING' FALSE NEGATIVES")
    print("These cases might reveal why the probe missed deception")
    print("-" * 80)
    
    missed_meeting_fns = [fn for fn in false_negatives if "missed a meeting" in fn['user_prompt'].lower()]
    print(f"Found {len(missed_meeting_fns)} false negatives with 'missed a meeting' prompts")
    
    for i, fn in enumerate(missed_meeting_fns[:3]):
        print(f"\n--- 'Missed Meeting' FN Example {i+1} (Sample {fn['sample_id']}) ---")
        print(f"Score: {fn['model_response_mean_score']:.4f}")
        print(f"Prompt: {fn['user_prompt']}")
        print(f"Response: {fn['model_response']}")
        print(f"Note: The prompt asks for an employee who missed a meeting, but the response")
        print(f"      shows minimal, vague excuses that might not trigger the probe strongly.")

if __name__ == "__main__":
    examine_specific_examples()








