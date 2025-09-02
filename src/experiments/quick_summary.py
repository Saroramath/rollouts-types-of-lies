import json
import os

def quick_summary():
    """Show a quick summary of all datasets"""
    
    datasets = [
        ("token_level_scores_gemma2_9b_layer19_labeled.json", "labeled"),
        ("token_level_scores_gemma2_9b_layer19_dishonest_labeled.json", "dishonest_labeled"),
        ("token_level_scores_gemma2_9b_layer19_reward_labeled.json", "reward_labeled"),
        ("token_level_scores_gemma2_9b_layer19_threat_labeled.json", "threat_labeled")
    ]
    
    print("=" * 100)
    print("QUICK SUMMARY OF ALL DATASETS")
    print("=" * 100)
    
    summary_data = []
    
    for json_file, suffix in datasets:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                metrics = data['metrics']
                total_samples = metrics['n_samples']
                fp_count = metrics['confusion']['fp']
                fn_count = metrics['confusion']['fn']
                fp_rate = fp_count / total_samples
                fn_rate = fn_count / total_samples
                total_error_rate = fp_rate + fn_rate
                
                summary_data.append({
                    'suffix': suffix,
                    'accuracy': metrics['accuracy'],
                    'fp_count': fp_count,
                    'fn_count': fn_count,
                    'fp_rate': fp_rate,
                    'fn_rate': fn_rate,
                    'total_error_rate': total_error_rate
                })
                
                print(f"\n📊 {suffix.upper().replace('_', ' ')}")
                print(f"   Accuracy: {metrics['accuracy']:.4f}")
                print(f"   False Positives: {fp_count} ({fp_rate:.1%})")
                print(f"   False Negatives: {fn_count} ({fn_rate:.1%})")
                print(f"   Total Error Rate: {total_error_rate:.1%}")
                
                # Load misclassifications for additional insights
                fp_file = f'false_positives_{suffix}.json'
                fn_file = f'false_negatives_{suffix}.json'
                
                if os.path.exists(fp_file) and os.path.exists(fn_file):
                    with open(fp_file, 'r') as f:
                        fps = json.load(f)
                    with open(fn_file, 'r') as f:
                        fns = json.load(f)
                    
                    if fps:
                        fp_scores = [fp['model_response_mean_score'] for fp in fps]
                        print(f"   FP Score Range: {min(fp_scores):.4f} to {max(fp_scores):.4f}")
                    
                    if fns:
                        fn_scores = [fn['model_response_mean_score'] for fn in fns]
                        print(f"   FN Score Range: {min(fn_scores):.4f} to {max(fn_scores):.4f}")
                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
    
    # Overall insights
    print(f"\n" + "=" * 100)
    print("OVERALL INSIGHTS")
    print("=" * 100)
    
    if summary_data:
        # Find best and worst performers
        best = max(summary_data, key=lambda x: x['accuracy'])
        worst = min(summary_data, key=lambda x: x['accuracy'])
        
        print(f"🏆 Best performing dataset: {best['suffix']} (Accuracy: {best['accuracy']:.4f})")
        print(f"⚠️  Worst performing dataset: {worst['suffix']} (Accuracy: {worst['accuracy']:.4f})")
        
        # Find datasets with most potential label ambiguity
        most_ambiguous = max(summary_data, key=lambda x: x['total_error_rate'])
        least_ambiguous = min(summary_data, key=lambda x: x['total_error_rate'])
        
        print(f"\n🔍 Most potential label ambiguity: {most_ambiguous['suffix']} (Error rate: {most_ambiguous['total_error_rate']:.1%})")
        print(f"✅ Least potential label ambiguity: {least_ambiguous['suffix']} (Error rate: {least_ambiguous['total_error_rate']:.1%})")
        
        # Performance ranking
        print(f"\n📈 Performance Ranking (by accuracy):")
        ranked = sorted(summary_data, key=lambda x: x['accuracy'], reverse=True)
        for i, dataset in enumerate(ranked):
            print(f"   {i+1}. {dataset['suffix']}: {dataset['accuracy']:.4f}")
        
        # Error rate ranking
        print(f"\n⚠️  Error Rate Ranking (by total error rate):")
        error_ranked = sorted(summary_data, key=lambda x: x['total_error_rate'], reverse=True)
        for i, dataset in enumerate(error_ranked):
            print(f"   {i+1}. {dataset['suffix']}: {dataset['total_error_rate']:.1%} error rate")
    
    print(f"\n" + "=" * 100)
    print("FILES CREATED:")
    print("=" * 100)
    
    for suffix in [d['suffix'] for d in summary_data]:
        print(f"✅ false_positives_{suffix}.json")
        print(f"✅ false_negatives_{suffix}.json")
        print(f"✅ detailed_analysis_{suffix}.md")
    
    print(f"✅ cross_dataset_comparison.md")
    print(f"✅ quick_summary.py")

if __name__ == "__main__":
    quick_summary()







