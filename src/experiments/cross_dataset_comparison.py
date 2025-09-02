import json
import os

def load_dataset_metrics(json_file_path):
    """Load metrics from a dataset JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        return data['metrics']
    except Exception as e:
        print(f"Error loading {json_file_path}: {e}")
        return None

def load_misclassifications(suffix):
    """Load misclassifications for a specific dataset"""
    fp_file = f'false_positives_{suffix}.json'
    fn_file = f'false_negatives_{suffix}.json'
    
    false_positives = []
    false_negatives = []
    
    if os.path.exists(fp_file):
        with open(fp_file, 'r') as f:
            false_positives = json.load(f)
    
    if os.path.exists(fn_file):
        with open(fn_file, 'r') as f:
            false_negatives = json.load(f)
    
    return false_positives, false_negatives

def create_cross_dataset_comparison():
    """Create a comprehensive comparison across all datasets"""
    
    datasets = [
        ("token_level_scores_gemma2_9b_layer19_labeled.json", "labeled"),
        ("token_level_scores_gemma2_9b_layer19_dishonest_labeled.json", "dishonest_labeled"),
        ("token_level_scores_gemma2_9b_layer19_reward_labeled.json", "reward_labeled"),
        ("token_level_scores_gemma2_9b_layer19_threat_labeled.json", "threat_labeled")
    ]
    
    comparison_data = {}
    
    print("Loading metrics from all datasets...")
    
    for json_file, suffix in datasets:
        if os.path.exists(json_file):
            metrics = load_dataset_metrics(json_file)
            if metrics:
                comparison_data[suffix] = metrics
                print(f"Loaded {suffix}: accuracy={metrics['accuracy']:.4f}")
    
    # Create comparison report
    report_filename = "cross_dataset_comparison.md"
    
    with open(report_filename, 'w') as f:
        f.write("# Cross-Dataset Performance Comparison\n\n")
        
        # Overall performance table
        f.write("## Overall Performance Comparison\n\n")
        f.write("| Dataset | Accuracy | Precision | Recall | F1 | TP | TN | FP | FN |\n")
        f.write("|---------|----------|-----------|--------|----|----|----|----|----|\n")
        
        for suffix, metrics in comparison_data.items():
            f.write(f"| {suffix.replace('_', ' ').title()} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | {metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['confusion']['tp']} | {metrics['confusion']['tn']} | {metrics['confusion']['fp']} | {metrics['confusion']['fn']} |\n")
        
        f.write("\n")
        
        # Key observations
        f.write("## Key Observations\n\n")
        
        # Find best and worst performing datasets
        best_dataset = max(comparison_data.items(), key=lambda x: x[1]['accuracy'])
        worst_dataset = min(comparison_data.items(), key=lambda x: x[1]['accuracy'])
        
        f.write(f"- **Best performing dataset**: {best_dataset[0].replace('_', ' ').title()} (Accuracy: {best_dataset[1]['accuracy']:.4f})\n")
        f.write(f"- **Worst performing dataset**: {worst_dataset[0].replace('_', ' ').title()} (Accuracy: {worst_dataset[1]['accuracy']:.4f})\n")
        f.write(f"- **Performance range**: {worst_dataset[1]['accuracy']:.4f} - {best_dataset[1]['accuracy']:.4f}\n\n")
        
        # Analyze false positive patterns
        f.write("## False Positive Analysis\n\n")
        f.write("| Dataset | FP Count | FP Rate |\n")
        f.write("|---------|----------|----------|\n")
        
        for suffix, metrics in comparison_data.items():
            total_samples = metrics['n_samples']
            fp_count = metrics['confusion']['fp']
            fp_rate = fp_count / total_samples
            f.write(f"| {suffix.replace('_', ' ').title()} | {fp_count} | {fp_rate:.4f} |\n")
        
        f.write("\n")
        
        # Analyze false negative patterns
        f.write("## False Negative Analysis\n\n")
        f.write("| Dataset | FN Count | FN Rate |\n")
        f.write("|---------|----------|----------|\n")
        
        for suffix, metrics in comparison_data.items():
            total_samples = metrics['n_samples']
            fn_count = metrics['confusion']['fn']
            fn_rate = fn_count / total_samples
            f.write(f"| {suffix.replace('_', ' ').title()} | {fn_count} | {fn_rate:.4f} |\n")
        
        f.write("\n")
        
        # Dataset-specific insights
        f.write("## Dataset-Specific Insights\n\n")
        
        for suffix, metrics in comparison_data.items():
            f.write(f"### {suffix.replace('_', ' ').title()}\n")
            f.write(f"- **Accuracy**: {metrics['accuracy']:.4f}\n")
            f.write(f"- **False Positives**: {metrics['confusion']['fp']} ({metrics['confusion']['fp']/metrics['n_samples']:.1%})\n")
            f.write(f"- **False Negatives**: {metrics['confusion']['fn']} ({metrics['confusion']['fn']/metrics['n_samples']:.1%})\n")
            
            # Load misclassifications for detailed analysis
            false_positives, false_negatives = load_misclassifications(suffix)
            
            if false_positives:
                fp_scores = [fp['model_response_mean_score'] for fp in false_positives]
                f.write(f"- **FP Score Range**: {min(fp_scores):.4f} to {max(fp_scores):.4f}\n")
                f.write(f"- **FP Average Score**: {sum(fp_scores)/len(fp_scores):.4f}\n")
            
            if false_negatives:
                fn_scores = [fn['model_response_mean_score'] for fn in false_negatives]
                f.write(f"- **FN Score Range**: {min(fn_scores):.4f} to {max(fn_scores):.4f}\n")
                f.write(f"- **FN Average Score**: {sum(fn_scores)/len(fn_scores):.4f}\n")
            
            f.write("\n")
        
        # Pattern analysis across datasets
        f.write("## Cross-Dataset Pattern Analysis\n\n")
        
        # Check if certain datasets have more ambiguous labels
        f.write("### Label Ambiguity Analysis\n\n")
        
        for suffix, metrics in comparison_data.items():
            total_samples = metrics['n_samples']
            fp_rate = metrics['confusion']['fp'] / total_samples
            fn_rate = metrics['confusion']['fn'] / total_samples
            
            f.write(f"**{suffix.replace('_', ' ').title()}**:\n")
            f.write(f"- False Positive Rate: {fp_rate:.1%}\n")
            f.write(f"- False Negative Rate: {fn_rate:.1%}\n")
            f.write(f"- Total Error Rate: {fp_rate + fn_rate:.1%}\n")
            
            if fp_rate + fn_rate > 0.25:  # High error rate threshold
                f.write(f"- **Note**: High error rate suggests potential label ambiguity\n")
            
            f.write("\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        
        f.write("### For High Error Rate Datasets\n")
        high_error_datasets = [(suffix, metrics) for suffix, metrics in comparison_data.items() 
                              if (metrics['confusion']['fp'] + metrics['confusion']['fn']) / metrics['n_samples'] > 0.25]
        
        for suffix, metrics in high_error_datasets:
            f.write(f"- **{suffix.replace('_', ' ').title()}**: Consider reviewing label quality and consistency\n")
        
        f.write("\n### For Low Error Rate Datasets\n")
        low_error_datasets = [(suffix, metrics) for suffix, metrics in comparison_data.items() 
                             if (metrics['confusion']['fp'] + metrics['confusion']['fn']) / metrics['n_samples'] <= 0.15]
        
        for suffix, metrics in low_error_datasets:
            f.write(f"- **{suffix.replace('_', ' ').title()}**: Good label quality, can be used as reference\n")
    
    print(f"Created cross-dataset comparison: {report_filename}")

if __name__ == "__main__":
    create_cross_dataset_comparison()







