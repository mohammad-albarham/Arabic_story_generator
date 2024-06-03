# Gradio Application

<img src="image_logo.png" style="width:50%; height:auto;">


This is a Gradio application that allows you to generate an Arabic story using generative AI models.

## Installation

1. Clone this repository:

    ```shell
    git clone https://github.com/mohammad-albarham/Arabic_story_generator.git
    ```

2. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

## Usage

0. Add the keys for OPEN AI API model and stability AI API in [models.py](https://github.com/mohammad-albarham/Arabic_story_generator/blob/3702d6cad85fe38ff5944d7f99f43a37d7dec151/llm_models.py#L16) and [image_generator.py](https://github.com/mohammad-albarham/Arabic_story_generator/blob/3702d6cad85fe38ff5944d7f99f43a37d7dec151/image_generator.py#L22)
1. Run the application:

    ```shell
    gradio app.py
    ```

2. Open your web browser and navigate to [http://localhost:7860](http://localhost:7860).

3. Add your a description and the needed number of pages and click on generate story.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

[ACADEMIC PUBLIC LICENSE](https://github.com/mohammad-albarham/Arabic_story_generator/tree/main?tab=License-1-ov-file)
