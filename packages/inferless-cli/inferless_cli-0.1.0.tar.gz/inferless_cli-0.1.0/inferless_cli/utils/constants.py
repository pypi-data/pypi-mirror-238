# Base constants used in the CLI
base_url = "https://devapi.inferless.com/api"
web_url = "https://console-dev.inferless.com"
docs_url = "https://docs.inferless.com"
# aws_access_key_id = "AKIAZ4F6ZRSI65TZX3HB"
# aws_secret_access_key = "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"
s3_bucket_name = "naveen-test-cli-upload"

# Generate a key for encryption
encryption_key = b"2pQ66OFqaNZp5-by-ZkI4DKXKWKrGKkh0vVFeal4niQ="

# Browser endpoints
cli_auth_url = f"{web_url}/user/keys"
io_docs_url = "https://docs.inferless.com/model-import/input-output-json"


# API endpoints
get_connected_accounts_url = f"{base_url}/accounts/list/connected/"
get_prefilled_io_url = f"{base_url}/model_import/huggingface/prefill"
get_volumes_list_url = f"{base_url}/volumes/list/"
get_templates_list_url = f"{base_url}/workspace/models/templates/list/"
get_workspace_models_url = f"{base_url}/workspace/models/list/"
delete_model_url = f"{base_url}/workspace/models/delete/"
deactivate_model_url = f"{base_url}/models/deactivate/"
rebuild_model_url = f"{base_url}/model_import/rebuild_model/"
activate_model_url = f"{base_url}/models/activate/"
validate_token_url = f"{base_url}/cli-tokens/exchange/"
get_workspaces = f"{base_url}/workspace/list"
import_model_url = f"{base_url}/model_import/create_update/"
upload_io_url = f"{base_url}/model_import/model_input_output_files/"
update_model_configurations_url = f"{base_url}/model_import/model_configuration/"
start_import_url = f"{base_url}/model_import/start_import/"
get_model_details_url = f"{base_url}/model_import"
get_model_code_url = f"{base_url}/models/code/"
validate_import_model_url = f"{base_url}/model_import/validate_model/"
set_variables_url = f"{base_url}/models/variables/set"
initilize_model_upload_url = (
    f"{base_url}/model_import/uploads/initializeMultipartUpload/"
)
get_signed_url_for_model_upload_url = (
    f"{base_url}/model_import/uploads/getMultipartPreSignedUrls/"
)
complete_model_upload_url = f"{base_url}/model_import/uploads/finalizeMultipartUpload/"


# UI/UX constants
inferless_dir_path = ".inferless"
frameworks = ["ONNX", "TENSORFLOW", "PYTORCH"]
# upload_methods = ["GIT", "HUGGINGFACE"]
upload_methods = ["GIT", "LOCAL"]
machine_types = ["A100", "T4"]
taskType = [
    {
        "id": "audio-classification",
        "value": "audio-classification",
        "display_name": "Audio Classification",
        "task_category": "transformer",
    },
    {
        "id": "automatic-speech-recognition",
        "value": "automatic-speech-recognition",
        "display_name": "Automatic Speech Recognition",
        "task_category": "transformer",
    },
    {
        "id": "conversational",
        "value": "conversational",
        "display_name": "Conversational",
        "task_category": "transformer",
    },
    {
        "id": "depth-estimation",
        "value": "depth-estimation",
        "display_name": "Depth Estimation",
        "task_category": "transformer",
    },
    {
        "id": "Depth-to-Image",
        "value": "Depth-to-Image",
        "display_name": "Depth-to-Image",
        "task_category": "diffuser",
    },
    {
        "id": "document-question-answering",
        "value": "document-question-answering",
        "display_name": "Document Question Answering",
        "task_category": "transformer",
    },
    {
        "id": "feature-extraction",
        "value": "feature-extraction",
        "display_name": "Feature Extraction",
        "task_category": "transformer",
    },
    {
        "id": "fill-mask",
        "value": "fill-mask",
        "display_name": "Fill Mask",
        "task_category": "transformer",
    },
    {
        "id": "image-classification",
        "value": "image-classification",
        "display_name": "Image Classification",
        "task_category": "transformer",
    },
    {
        "id": "image-segmentation",
        "value": "image-segmentation",
        "display_name": "Image Segmentation",
        "task_category": "transformer",
    },
    {
        "id": "image-to-text",
        "value": "image-to-text",
        "display_name": "Image To Text",
        "task_category": "transformer",
    },
    {
        "id": "Image-Variation",
        "value": "Image-Variation",
        "display_name": "Image-Variation",
        "task_category": "diffuser",
    },
    {
        "id": "Image-to-Image",
        "value": "Image-to-Image",
        "display_name": "Image-to-Image",
        "task_category": "diffuser",
    },
    {
        "id": "Inpaint",
        "value": "Inpaint",
        "display_name": "Inpaint",
        "task_category": "diffuser",
    },
    {
        "id": "InstructPix2Pix",
        "value": "InstructPix2Pix",
        "display_name": "InstructPix2Pix",
        "task_category": "diffuser",
    },
    {
        "id": "object-detection",
        "value": "object-detection",
        "display_name": "Object Detection",
        "task_category": "transformer",
    },
    {
        "id": "question-answering",
        "value": "question-answering",
        "display_name": "Question Answering",
        "task_category": "transformer",
    },
    {
        "id": "Stable-Diffusion-Latent-Upscaler",
        "value": "Stable-Diffusion-Latent-Upscaler",
        "display_name": "Stable-Diffusion-Latent-Upscaler",
        "task_category": "diffuser",
    },
    {
        "id": "summarization",
        "value": "summarization",
        "display_name": "Summarization",
        "task_category": "transformer",
    },
    {
        "id": "Super-Resolution",
        "value": "Super-Resolution",
        "display_name": "Super-Resolution",
        "task_category": "diffuser",
    },
    {
        "id": "table-question-answering",
        "value": "table-question-answering",
        "display_name": "Table Question Answering",
        "task_category": "transformer",
    },
    {
        "id": "text-classification",
        "value": "text-classification",
        "display_name": "Text Classification",
        "task_category": "transformer",
    },
    {
        "id": "text-generation",
        "value": "text-generation",
        "display_name": "Text Generation",
        "task_category": "transformer",
    },
    {
        "id": "Text-to-Image",
        "value": "Text-to-Image",
        "display_name": "Text-to-Image",
        "task_category": "diffuser",
    },
    {
        "id": "text2text-generation",
        "value": "text2text-generation",
        "display_name": "Text2text Generation",
        "task_category": "transformer",
    },
    {
        "id": "token-classification",
        "value": "token-classification",
        "display_name": "Token Classification",
        "task_category": "transformer",
    },
    {
        "id": "translation",
        "value": "translation",
        "display_name": "Translation",
        "task_category": "transformer",
    },
    {
        "id": "video-classification",
        "value": "video-classification",
        "display_name": "Video Classification",
        "task_category": "transformer",
    },
    {
        "id": "visual-question-answering",
        "value": "visual-question-answering",
        "display_name": "Visual Question Answering",
        "task_category": "transformer",
    },
    {
        "id": "zero-shot-audio-classification",
        "value": "zero-shot-audio-classification",
        "display_name": "Zero Shot Audio Classification",
        "task_category": "transformer",
    },
    {
        "id": "zero-shot-classification",
        "value": "zero-shot-classification",
        "display_name": "Zero Shot Classification",
        "task_category": "transformer",
    },
    {
        "id": "zero-shot-image-classification",
        "value": "zero-shot-image-classification",
        "display_name": "Zero Shot Image Classification",
        "task_category": "transformer",
    },
    {
        "id": "zero-shot-object-detection",
        "value": "zero-shot-object-detection",
        "display_name": "Zero Shot Object Detection",
        "task_category": "transformer",
    },
]
huggingface_type = [
    {"id": "transformer", "value": "transformer", "display_name": "Transformer"},
    {"id": "diffuser", "value": "diffuser", "display_name": "Diffuser"},
]
github = "GITHUB"
huggingface = "HUGGINGFACE"
git = "GIT"

default_input_json = {
    "inputs": [
        {
            "data": ["Once upon a time"],
            "name": "prompt",
            "shape": [1],
            "datatype": "BYTES",
        }
    ]
}

default_output_json = {
    "outputs": [
        {
            "data": [
                "Once upon a time the sun was up he would look down to the valley below and wonder wis"
            ],
            "name": "generated_text",
            "shape": [1],
            "datatype": "BYTES",
        }
    ]
}

default_input_file_name = "input.json"
default_output_file_name = "output.json"
default_machine_values = {
    "shared": {
        "T4": {
            "min_cpu": "1",
            "max_cpu": "2",
            "cpu": "2",
            "memory": "10",
            "min_memory": "1",
            "max_memory": "20",
        },
        "A100": {
            "min_cpu": "1",
            "max_cpu": "5",
            "cpu": "2",
            "memory": "20",
            "min_memory": "1",
            "max_memory": "40",
        },
        "A10": {
            "min_cpu": "1",
            "max_cpu": "2",
            "cpu": "2",
            "memory": "10",
            "min_memory": "1",
            "max_memory": "40",
        },
    },
    "dedicated": {
        "T4": {
            "min_cpu": "3",
            "max_cpu": "3",
            "cpu": "3",
            "memory": "20",
            "min_memory": "20",
            "max_memory": "20",
        },
        "A100": {
            "min_cpu": "20",
            "max_cpu": "20",
            "cpu": "20",
            "memory": "200",
            "min_memory": "200",
            "max_memory": "200",
        },
        "A10": {
            "min_cpu": "7",
            "max_cpu": "7",
            "cpu": "7",
            "memory": "30",
            "min_memory": "30",
            "max_memory": "30",
        },
    },
}
