import pandas as pd
import great_expectations as gx

def check_quality(df: pd.DataFrame, suite_name: str = "default_suite") -> dict:
    """
    Checks data quality using Great Expectations.
    
    Args:
        df: The pandas DataFrame to check.
        suite_name: Name of the expectation suite.
        
    Returns:
        A dictionary containing the validation results.
    """
    context = gx.get_context()
    
    datasource_name = "pandas_datasource"
    data_asset_name = "my_dataframe"
    
    # Use Fluent Data Sources API
    # Check if datasource exists, if not add it
    try:
        # Try new API (GX 1.0+)
        if hasattr(context, "data_sources"):
             try:
                 datasource = context.data_sources.get(datasource_name)
             except KeyError:
                 datasource = context.data_sources.add_pandas(datasource_name)
        else:
             # Fallback for older versions or if 'sources' is the attribute
             try:
                 datasource = context.get_datasource(datasource_name)
             except ValueError:
                 datasource = context.sources.add_pandas(datasource_name)
    except Exception as e:
        # Last resort: try adding it directly via add_pandas if previous attempts failed
        # This handles cases where get fails but add works
        if hasattr(context, "data_sources"):
            datasource = context.data_sources.add_pandas(datasource_name)
        else:
            datasource = context.sources.add_pandas(datasource_name)
    
    # Add/Get data asset
    try:
        data_asset = datasource.get_asset(data_asset_name)
    except LookupError:
        data_asset = datasource.add_dataframe_asset(name=data_asset_name)
        
    # Build batch request
    batch_request = data_asset.build_batch_request(options={"dataframe": df})
    
    # Create Validator
    validator = context.get_validator(
        batch_request=batch_request,
        create_expectation_suite_with_name=suite_name
    )
    
    # Add some default expectations for demonstration
    for col in df.columns:
        validator.expect_column_to_exist(col)
        if df[col].dtype == 'object':
             validator.expect_column_values_to_not_be_null(col)

    # Run validation
    validation_result = validator.validate()
    
    return validation_result.to_json_dict()
