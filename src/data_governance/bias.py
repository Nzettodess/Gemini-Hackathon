import pandas as pd
from fairlearn.metrics import MetricFrame, selection_rate, count
from sklearn.metrics import accuracy_score
from typing import Optional, List, Dict, Any

def detect_bias(
    df: pd.DataFrame, 
    sensitive_column: str, 
    target_column: Optional[str] = None,
    predictions_column: Optional[str] = None
) -> Dict[str, Any]:
    """
    Detects bias in a dataset using Fairlearn.
    
    Args:
        df: The dataset.
        sensitive_column: The column representing the sensitive group (e.g., 'gender', 'race').
        target_column: The ground truth label column (optional).
        predictions_column: The model predictions column (optional).
        
    Returns:
        A dictionary with bias metrics.
    """
    
    metrics = {
        "count": count
    }
    
    y_true = df[target_column] if target_column else None
    y_pred = df[predictions_column] if predictions_column else None
    
    # If we have a target, we can check for label imbalance (Selection Rate on y_true)
    if target_column:
        metrics["label_positive_rate"] = selection_rate
        
    # If we have predictions, we can check for Selection Rate on y_pred (Demographic Parity)
    # and Accuracy if we also have y_true
    if predictions_column:
        metrics["prediction_positive_rate"] = selection_rate
        if target_column:
            metrics["accuracy"] = accuracy_score
            
    # If no target/pred, we just return counts (representation)
    if not target_column and not predictions_column:
        # Just return representation
        counts = df[sensitive_column].value_counts(normalize=True).to_dict()
        return {"representation": counts}

    # Construct MetricFrame
    # Note: MetricFrame expects y_true and y_pred as positional args usually, 
    # but we can pass them conditionally.
    # To simplify, we'll instantiate MetricFrame differently based on availability.
    
    results = {}
    
    # 1. Analyze Representation (Counts)
    # MetricFrame requires y_pred, so we pass dummy if needed
    dummy_pred = y_true if y_true is not None else df[sensitive_column]
    
    mf_count = MetricFrame(
        metrics={"count": count},
        y_true=y_true if y_true is not None else df[sensitive_column], # Dummy
        y_pred=dummy_pred,
        sensitive_features=df[sensitive_column]
    )
    results["group_counts"] = mf_count.by_group.to_dict()
    
    # 2. Analyze Target (Label Bias)
    if target_column:
        mf_target = MetricFrame(
            metrics={"label_rate": selection_rate},
            y_true=y_true,
            y_pred=y_true, # selection_rate uses y_pred, so we pass y_true as y_pred to measure label rate
            sensitive_features=df[sensitive_column]
        )
        results["label_bias"] = {
            "by_group": mf_target.by_group.to_dict(),
            "overall": mf_target.overall.item() if hasattr(mf_target.overall, "item") else mf_target.overall,
            "difference": mf_target.difference(method='between_groups')
        }
        
    # 3. Analyze Predictions (Model Bias)
    if predictions_column:
        metrics_dict = {"prediction_rate": selection_rate}
        if target_column:
            metrics_dict["accuracy"] = accuracy_score
            
        mf_pred = MetricFrame(
            metrics=metrics_dict,
            y_true=y_true if y_true is not None else y_pred,
            y_pred=y_pred,
            sensitive_features=df[sensitive_column]
        )
        results["model_bias"] = {
            "by_group": mf_pred.by_group.to_dict(),
            "difference": mf_pred.difference(method='between_groups')
        }

    return results
