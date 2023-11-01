from raga import *
import datetime


run_name = f"failure_mode_analysis_semantic_segmentation_v2-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="GBEAALGlGsq7HrtU8M2c", secret_key="kpFKGZcP7Q0e1ONEH0kZNOIMS19G4P1f6710ddC0", host="http://13.126.220.245:8080")

rules = FMARules()

rules.add(metric = "Precision",  metric_threshold = 0.5, label = "ALL", type="label", background_label="Unlabelled", include_background=False)
rules.add(metric = "Precision",  metric_threshold = 0.5, label = "ALL", type="label", background_label="Unlabelled", include_background=False)

rules.add(metric = "wIoU", metric_threshold = 0.5, weights={"car": 2, "unlabelled": 1}, type="label")



cls_default = clustering(method="k-means", embedding_col="Embedding", level="image", args= {"numOfClusters": 5})

edge_case_detection = failure_mode_analysis(test_session=test_session,
                                            dataset_name = "failure_mode_analysis_sementic_v1",
                                            test_name = "Test",
                                            model = "ModelA",
                                            gt = "ModelGT",
                                            rules = rules,
                                            output_type="semantic_segmentation",
                                            clustering=cls_default,
                                            type="embedding")

test_session.add(edge_case_detection)

test_session.run()