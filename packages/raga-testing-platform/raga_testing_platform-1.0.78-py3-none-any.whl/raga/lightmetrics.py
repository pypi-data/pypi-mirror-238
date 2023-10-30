from typing import Optional
from raga import TestSession, ModelABTestRules, FMARules, LQRules, EventABTestRules, Filter

def lightmetrics_inference_generator(test_session:TestSession, dataset_name: str, model_name:str, model_inference_col_name:str, event_inference_col_name:str, filter:Filter):
    from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA, REQUIRED_ARG_V2
    dataset_id = lightmetrics_inference_generator_validation(test_session, dataset_name, model_name, model_inference_col_name, event_inference_col_name, filter)
    payload = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "model": model_name,
            "modelInferenceColName": model_inference_col_name,
            "eventInferenceColName": event_inference_col_name,
            'filter':filter.get()
        }
    res_data = test_session.http_client.post(f"api/experiment/test/lm/inferenceGenerator", data=payload, headers={"Authorization": f'Bearer {test_session.token}'})

    if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)


def lightmetrics_inference_generator_validation(test_session:TestSession, dataset_name:str, model_name:str, model_inference_col_name:str, event_inference_col_name:str, filter:Filter):
    from raga.constants import INVALID_RESPONSE, INVALID_RESPONSE_DATA, REQUIRED_ARG_V2

    assert isinstance(test_session, TestSession), f"{REQUIRED_ARG_V2.format('test_session', 'instance of the TestSession')}"
    assert isinstance(dataset_name, str) and dataset_name, f"{REQUIRED_ARG_V2.format('dataset_name', 'str')}"
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})

    if not isinstance(res_data, dict):
            raise ValueError(INVALID_RESPONSE)
    
    dataset_id = res_data.get("data", {}).get("id")

    if not dataset_id:
        raise KeyError(INVALID_RESPONSE_DATA)
    assert isinstance(model_name, str) and model_name, f"{REQUIRED_ARG_V2.format('model_name', 'str')}"
    assert isinstance(model_inference_col_name, str) and model_inference_col_name, f"{REQUIRED_ARG_V2.format('model_inference_col_name', 'str')}"
    assert isinstance(event_inference_col_name, str) and event_inference_col_name, f"{REQUIRED_ARG_V2.format('event_inference_col_name', 'str')}"
    assert isinstance(filter, Filter) and filter, f"{REQUIRED_ARG_V2.format('filter', 'instance of the Filter')}"
    return dataset_id