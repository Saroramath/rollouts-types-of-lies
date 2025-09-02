import json
import os
from collections import Counter

def analyze_dataset(json_file_path, output_suffix):
    """Analyze a single dataset and save results with unique suffix"""
    
    print(f"\n{'='*80}")
    print(f"ANALYZING DATASET: {json_file_path}")
    print(f"{'='*80}")
    
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {json_file_path}: {e}")
        return None
    
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
            false_positives.append({
                'sample_id': result['sample_id'],
                'user_prompt': result['user_prompt'],
                'model_response': result['model_response'],
                'model_response_mean_score': result['model_response_mean_score'],
                'complete_prompt_mean_score': result['complete_prompt_mean_score']
            })
        elif true_label == 1 and pred_label == 0:
            false_negatives.append({
                'sample_id': result['sample_id'],
                'user_prompt': result['user_prompt'],
                'model_response': result['model_response'],
                'model_response_mean_score': result['model_response_mean_score'],
                'complete_prompt_mean_score': result['complete_prompt_mean_score']
            })
    
    print(f"False Positives (FP): {len(false_positives)}")
    print(f"False Negatives (FN): {len(false_negatives)}")
    
    # Save misclassifications with unique suffix
    fp_filename = f'false_positives_{output_suffix}.json'
    fn_filename = f'false_negatives_{output_suffix}.json'
    
    with open(fp_filename, 'w') as f:
        json.dump(false_positives, f, indent=2)
    
    with open(fn_filename, 'w') as f:
        json.dump(false_negatives, f, indent=2)
    
    print(f"Saved false positives to: {fp_filename}")
    print(f"Saved false negatives to: {fn_filename}")
    
    return false_positives, false_negatives

def create_detailed_analysis(output_suffix):
    """Create detailed analysis for a specific dataset"""
    
    fp_filename = f'false_positives_{output_suffix}.json'
    fn_filename = f'false_negatives_{output_suffix}.json'
    
    if not os.path.exists(fp_filename) or not os.path.exists(fn_filename):
        print(f"Missing files for {output_suffix}")
        return
    
    with open(fp_filename, 'r') as f:
        false_positives = json.load(f)
    
    with open(fn_filename, 'r') as f:
        false_negatives = json.load(f)
    
    analysis_filename = f'detailed_analysis_{output_suffix}.md'
    
    with open(analysis_filename, 'w') as f:
        f.write(f"# Detailed Analysis for {output_suffix.upper()} Dataset\n\n")
        
        f.write("## Overview\n")
        f.write(f"- **False Positives (FP)**: {len(false_positives)} cases\n")
        f.write(f"- **False Negatives (FN)**: {len(false_negatives)} cases\n\n")
        
        # False Positives Analysis
        f.write("## False Positives Analysis\n\n")
        
        if false_positives:
            fp_scores = [fp['model_response_mean_score'] for fp in false_positives]
            f.write(f"- **Score range**: {min(fp_scores):.4f} to {max(fp_scores):.4f}\n")
            f.write(f"- **Average score**: {sum(fp_scores)/len(fp_scores):.4f}\n\n")
            
            # Group by score ranges
            high_fps = [fp for fp in false_positives if fp['model_response_mean_score'] >= 2.0]
            medium_fps = [fp for fp in false_positives if 1.0 <= fp['model_response_mean_score'] < 2.0]
            low_fps = [fp for fp in false_positives if fp['model_response_mean_score'] < 1.0]
            
            f.write(f"- **High (2.0+)**: {len(high_fps)} samples\n")
            f.write(f"- **Medium (1.0-2.0)**: {len(medium_fps)} samples\n")
            f.write(f"- **Low (0.0-1.0)**: {len(low_fps)} samples\n\n")
            
            # Show top examples
            f.write("### Top False Positive Examples\n\n")
            for i, fp in enumerate(sorted(false_positives, key=lambda x: x['model_response_mean_score'], reverse=True)[:5]):
                f.write(f"**Example {i+1} (Sample {fp['sample_id']})**\n")
                f.write(f"- Score: {fp['model_response_mean_score']:.4f}\n")
                f.write(f"- Prompt: {fp['user_prompt'][:200]}...\n")
                f.write(f"- Response: {fp['model_response'][:200]}...\n\n")
        
        # False Negatives Analysis
        f.write("## False Negatives Analysis\n\n")
        
        if false_negatives:
            fn_scores = [fn['model_response_mean_score'] for fn in false_negatives]
            f.write(f"- **Score range**: {min(fn_scores):.4f} to {max(fn_scores):.4f}\n")
            f.write(f"- **Average score**: {sum(fn_scores)/len(fn_scores):.4f}\n\n")
            
            # Group by score ranges
            near_threshold = [fn for fn in false_negatives if fn['model_response_mean_score'] >= -0.5]
            low_fns = [fn for fn in false_negatives if -1.0 <= fn['model_response_mean_score'] < -0.5]
            very_low_fns = [fn for fn in false_negatives if fn['model_response_mean_score'] < -1.0]
            
            f.write(f"- **Near threshold (-0.5 to 0.0)**: {len(near_threshold)} samples\n")
            f.write(f"- **Low (-1.0 to -0.5)**: {len(low_fns)} samples\n")
            f.write(f"- **Very low (< -1.0)**: {len(very_low_fns)} samples\n\n")
            
            # Show top examples
            f.write("### Top False Negative Examples\n\n")
            for i, fn in enumerate(sorted(false_negatives, key=lambda x: x['model_response_mean_score'])[:5]):
                f.write(f"**Example {i+1} (Sample {fn['sample_id']})**\n")
                f.write(f"- Score: {fn['model_response_mean_score']:.4f}\n")
                f.write(f"- Prompt: {fn['user_prompt'][:200]}...\n")
                f.write(f"- Response: {fn['model_response'][:200]}...\n\n")
    
    print(f"Created detailed analysis: {analysis_filename}")

def main():
    """Analyze all available datasets"""
    
    # Define the datasets to analyze
    datasets = [
        ("token_level_scores_gemma2_9b_layer19_labeled.json", "labeled"),
        ("token_level_scores_gemma2_9b_layer19_dishonest_labeled.json", "dishonest_labeled"),
        ("token_level_scores_gemma2_9b_layer19_reward_labeled.json", "reward_labeled"),
        ("token_level_scores_gemma2_9b_layer19_threat_labeled.json", "threat_labeled")
    ]
    
    print("Starting analysis of all datasets...")
    
    for json_file, suffix in datasets:
        if os.path.exists(json_file):
            print(f"\nProcessing {json_file}...")
            try:
                false_positives, false_negatives = analyze_dataset(json_file, suffix)
                if false_positives is not None:
                    create_detailed_analysis(suffix)
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        else:
            print(f"File not found: {json_file}")
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*80}")
    print("Created files for each dataset:")
    for _, suffix in datasets:
        print(f"- false_positives_{suffix}.json")
        print(f"- false_negatives_{suffix}.json")
        print(f"- detailed_analysis_{suffix}.md")

if __name__ == "__main__":
    main()







