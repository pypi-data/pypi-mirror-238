from raga import *
import datetime

run_name = f"drift-test-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name = run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

rules = DriftDetectionRules()

rules.add(type="multi_class_anomaly_detection", dist_metric="Mahalanobis", _class="ALL")
edge_case_detection = data_drift_detection(test_session=test_session,
                                           test_name="Drift-detection-test-HW_OD",
                                           train_dataset_name="drift_honeywell_traffic_gt_object_detection_v2",
                                           field_dataset_name="drift_honeywell_traffic_pred_object_detection",
                                           train_embed_col_name="ImageVectorsM1",
                                           field_embed_col_name = "ImageVectorsM1",
                                           output_type = "multi_class_object_detection",
                                           level = "image",
                                           rules = rules)

# edge_case_detection = data_drift_detection(test_session=test_session,
#                                            test_name="Drift-detection-test",
#                                            train_dataset_name="grassLands-v1",
#                                            field_dataset_name="barrenland_v1",
#                                            train_embed_col_name="Annotations",
#                                            field_embed_col_name = "Annotations",
#                                            output_type = "semantic_segmentation",
#                                            level = "image",
#                                            aggregation_level=["location", "vehicle_no", "channel"],
#                                            rules = rules)

# edge_case_detection = data_drift_detection(test_session=test_session,
#                                            test_name="Drift-detection-test",
#                                            train_dataset_name="grasslands-v1",
#                                            field_dataset_name="barrenlands-v1",
#                                            train_embed_col_name="ImageVectorsM1",
#                                            field_embed_col_name = "ImageVectorsM1",
#                                            output_type = "semantic_segmentation",
#                                            level = "image",
#                                            rules = rules)

# edge_case_detection = data_drift_detection(test_session=test_session,
#                                            test_name="Drift-detection-test",
#                                            dataset_name="super_resolution_data_v1",
#                                            embed_col_name="imageEmbedding",
#                                            output_type = "super_resolution",
#                                            rules = rules)

# # add payload into test_session object
# test_session.add(edge_case_detection)
# #run added test
# test_session.run()


# project_name = "Semantic Segmentation - Images"
# run_name = f"Demo-Run-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
# test_session = TestSession(project_name="Semantic Segmentation - Images", run_name= run_name, access_key="DlGhu2Y9D7Kbc955Y0tz", secret_key="euSZgU49jkIV4CTekcKvpqdk93sQpZdRe338ym1N", host="http://13.126.220.245:8080")

# rules = DriftDetectionRules()
# rules.add(type="anomaly_detection", dist_metric="Mahalanobis", _class="ALL", threshold=21.0)

# edge_case_detection = data_drift_detection(test_session=test_session,
#                                            test_name="Drift-detection-test",
#                                            train_dataset_name="grasslands-final",
#                                            field_dataset_name="barrenlands-final",
#                                            train_embed_col_name="ImageEmbedding",
#                                            field_embed_col_name = "ImageEmbedding",
#                                            output_type = "semantic_segmentation",
#                                            level = "image",
#                                            rules = rules)


test_session.add(edge_case_detection)

test_session.run()


