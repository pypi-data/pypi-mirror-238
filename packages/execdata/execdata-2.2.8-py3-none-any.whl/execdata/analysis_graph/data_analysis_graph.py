'''
Date         : 2023-11-02 12:47:29
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-11-02 15:42:43
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\analysisgraph\data_analysis_graph.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from tabulate import tabulate


def top_correlation(df, target_feature, top_feature_number=10, correlation_boundary=0.05):
    # Calculate the correlation with the target variable and sort by values
    correlations = []
    for column in df.columns:
        if column != target_feature:
            correlation = df[target_feature].corr(df[column])
            if abs(correlation) > correlation_boundary:
                correlation = round(correlation, 2)
                correlations.append((column, correlation))

    # top_feature_number = 10 #default value
    # Sort the correlations by values and select the top 10
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    top_features = correlations[:top_feature_number]

    # Extract column name
    top_feature_column_names = [item[0] for item in top_features]
    # print(column_names)

    # Display the top 12 feature correlations as a table
    headers = ["Feature", "Abs Cor"]
    table = tabulate(top_features, headers=headers, tablefmt="github")

    print(
        f"Top {top_feature_number} Feature Correlations (sorted by absolute values):")
    print(table)

    return top_feature_column_names
