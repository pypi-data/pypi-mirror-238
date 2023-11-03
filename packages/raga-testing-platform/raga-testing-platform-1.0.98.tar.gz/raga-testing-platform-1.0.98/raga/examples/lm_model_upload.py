from raga import *

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= "LM-Model-Upload-Run-Test-v1", access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Production-America-Stop.zip", name="Production-America-Stop", version="0.0.1")
lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Production-Canada-Stop-Quebec.zip", name="Production-Canada-Stop-Quebec", version="0.0.1")
lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Production-Vienna-Alto.zip", name="Production-Vienna-Alto", version="0.0.1")
lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Production-Vienna-Stop.zip", name="Production-Vienna-Stop", version="0.0.1")


# lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Complex-America-Stop_Config_test_missing.zip", name="Complex-America-Stop_Config_test_missing", version="0.0.1")

# lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Complex-America-Stop_executable_missing.zip", name="Complex-America-Stop_executable_missing", version="0.0.1")

# lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Complex-America-Stop_Config_test_missmatch_model_name.zip", name="Complex-America-Stop_Config_test_missmatch_model_name", version="0.0.1")

# lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/lm_models/Complex-America-Stop-DLC_test.zip", name="Complex-America-Stop-DLC_test", version="0.0.1")
