from raga import *
import datetime

# run_name = f"AB-event-unlabelled-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
run_name = f"AB-event-unlabelled-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


filters = Filter()
filters.add(TimestampFilter(gte="2022-03-15T00:00:00Z", lte="2024-10-30T00:00:00Z"))

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name = "AB-event-unlabelled-oct-20-v1", access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")


rules = EventABTestRules() 
rules.add(metric = "difference_percentage", IoU = 0.5, _class = "ALL", threshold = 0.5, conf_threshold=0.5)
rules.add(metric = "difference_count", IoU = 0.5, _class = "ALL", threshold = 0.5, conf_threshold=0.5)

model_comparison_check = event_ab_test(test_session=test_session, 
                                       dataset_name="test-lm-loader-30-oct-v1",
                                       test_name="AB-test-unlabelled",
                                       modelA = "Production-America-Stop",
                                       modelB = "Complex-America-Stop",
                                       object_detection_modelA="Production-America-Stop",
                                       object_detection_modelB = "Complex-America-Stop",
                                       type = "metadata", 
                                       sub_type = "unlabelled", 
                                       output_type = "event_detection",
                                       rules = rules,
                                       aggregation_level=["weather"], 
                                       filter=filters)

# add payload into test_session object
test_session.add(model_comparison_check)
#run added test
test_session.run()