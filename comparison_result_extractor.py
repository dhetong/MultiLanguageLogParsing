import csv
import pandas as pd

base_file_df = pd.read_csv('Data/GroundTruth/Hadoop_event_groundtruth.csv')
result_file_df = pd.read_csv('Data/Output/Hadoop_translated_content.log_structured.csv')

comparison_result_file = open('Data/ComparisonResult/EventTemplate/Hadoop_translated_comparison.csv', 'w')
comparison_result_output = csv.writer(comparison_result_file)
comparison_result_output.writerow(['EventId', 'EventTemplate', 'BaseId', 'BaseTemplate', 'Content', 'Type'])

base_for_comb_df = base_file_df[['Content','EventId','EventTemplate']]
base_for_comb_df = base_for_comb_df.rename(columns={'EventId':'BaseId', 'EventTemplate':'BaseTemplate'})
result_for_comb_df = result_file_df[['EventId','EventTemplate']]

comparison_df = pd.concat([result_for_comb_df, base_for_comb_df], axis=1, join='inner')

result_id_list = comparison_df['EventId'].tolist()
result_id_list = list(dict.fromkeys(result_id_list))
base_id_list = comparison_df['BaseId'].tolist()
base_id_list = list(dict.fromkeys(base_id_list))

for base_id in base_id_list:
    comparison_base_tmp_df = comparison_df[comparison_df['BaseId'] == base_id]
    result_id_tmp_list = list(dict.fromkeys(comparison_base_tmp_df['EventId'].tolist()))
    if(len(result_id_tmp_list) > 1):
        pass
    else:
        result_id = result_id_tmp_list[0]
        comparison_result_tmp_df = comparison_df[comparison_df['EventId'] == result_id]
        if(len(comparison_result_tmp_df) > len(comparison_base_tmp_df)):
            pass
        elif(len(comparison_result_tmp_df) <  len(comparison_base_tmp_df)):
            pass