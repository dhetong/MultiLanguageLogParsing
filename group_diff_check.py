import pandas as pd
import csv
from scipy.special import comb

def get_agreement(series_groundtruth, series_parsedlog, comparison_result_file, debug=False):
    comparison_result_output = open(comparison_result_file, 'w')
    comparison_result_csv = csv.writer(comparison_result_output)
    comparison_result_csv.writerow(['event_id', 'groundtruth_id'])

    series_groundtruth_valuecounts = series_groundtruth.value_counts()
    real_pairs = 0
    for count in series_groundtruth_valuecounts:
        if count > 1:
            real_pairs += comb(count, 2)

    series_parsedlog_valuecounts = series_parsedlog.value_counts()
    parsed_pairs = 0
    for count in series_parsedlog_valuecounts:
        if count > 1:
            parsed_pairs += comb(count, 2)

    accurate_pairs = 0
    accurate_events = 0
    for parsed_eventId in series_parsedlog_valuecounts.index:
        logIds = series_parsedlog[series_parsedlog == parsed_eventId].index
        series_groundtruth_logId_valuecounts = series_groundtruth[logIds].value_counts()
        error_eventIds = (
            parsed_eventId,
            series_groundtruth_logId_valuecounts.index.tolist(),
        )
        error = True
        if series_groundtruth_logId_valuecounts.size == 1:
            groundtruth_eventId = series_groundtruth_logId_valuecounts.index[0]
            if (
                    logIds.size
                    == series_groundtruth[series_groundtruth == groundtruth_eventId].size
            ):
                accurate_events += logIds.size
                error = False
        if error and debug:
            comparison_result_csv.writerow([parsed_eventId, series_groundtruth_logId_valuecounts.index.tolist()])
            # print(
            #     "(parsed_eventId, groundtruth_eventId) =",
            #     error_eventIds,
            #     "failed",
            #     logIds.size,
            #     "messages",
            # )
        for count in series_groundtruth_logId_valuecounts:
            if count > 1:
                accurate_pairs += comb(count, 2)

    agreement = float(accurate_events) / series_groundtruth.size
    return agreement

df_groundtruth = pd.read_csv('Data/GroundTruth/HPC_event_groundtruth.csv')
df_ori_result = pd.read_csv('Data/Output/HPC_correspond_content.log_structured.csv')
df_trans_result = pd.read_csv('Data/Output/HPC_translated_content.log_structured.csv')
df_trans_split_result = pd.read_csv('Data/Output/HPC_translated_content.log_split_structured.csv')

agreement = get_agreement(df_ori_result["EventId"], df_trans_result["EventId"],
                          'Data/ComparisonResult/EventID/baseline_agreement_HPC.csv', True)
accuracy = get_agreement(df_groundtruth["EventId"], df_trans_result["EventId"],
                         'Data/ComparisonResult/EventID/baseline_accuracy_HPC.csv', True)
agreement_split = get_agreement(df_ori_result["EventId"], df_trans_split_result["EventId"],
                                'Data/ComparisonResult/EventID/split_agreemet_HPC.csv', True)
accuracy_split = get_agreement(df_groundtruth["EventId"], df_trans_split_result["EventId"],
                               'Data/ComparisonResult/EventID/split_accuracy_HPC.csv', True)

print("Baseline:")
print(agreement)
print(accuracy)

print("Split:")
print(agreement_split)
print(accuracy_split)
