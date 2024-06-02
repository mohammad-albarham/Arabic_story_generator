import gradio as gr
from llm_models import get_text_image_pairs
import time
from tqdm import tqdm

title_markdown = ("""
<div style="display: flex; justify-content: center; align-items: center; text-align: center; direction: rtl;">
  <img src="https://s11.ax1x.com/2023/12/28/piqvDMV.png" alt="MoE-LLaVA🚀" style="max-width: 120px; height: auto; margin-right: 20px;">
  <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
    <h1 style="margin: 0; font-size: 4em;">الراوي</h1>
                  <br>
    <h2 style="margin: 0; font-size: 1.5em;">صانع القصص بالذكاء الاصطناعي التوليدي</h2>
  </div>
</div>
""")

def get_text_images_values(k, input_prompt):

    pages = int(k)

    segments_list, images_names =  get_text_image_pairs(pages,input_prompt)
    return segments_list, images_names

css = """
.gradio-container {direction: rtl}
.gradio-container-4-18-0 .prose h1 {direction: rtl};
}
"""

with gr.Blocks(css=css) as demo:

    gr.Markdown(title_markdown)

    prompt = gr.Textbox(label="معلومات بسيطة عن القصة",
                info="أدخل بعض المعلومات عن القصة، مثلاً: خالد صبي في الرابعة من عمره، ويحب أن يصبح طياراً في المستقبل",
                placeholder="خالد صبي في الرابعة من عمره، ويحب أن يصبح طياراً في المستقبل",
                text_align="right",
                rtl=True,
                elem_classes="rtl-textbox",
                elem_id="rtl-textbox")


    with gr.Row():
        

        max_textboxes = 10 # Define the max number of textboxed, so we will add the max number of textboxes and images to the layout

        def variable_outputs(k, segments_list):
            k = int(k)
            return [gr.Textbox(label= f"الصفحة رقم {i+1}", value=item, text_align="right", visible=True) for i, item in enumerate(segments_list)] + [gr.Textbox(visible=False, text_align="right", rtl=True)]*(max_textboxes-k)

        def variable_outputs_image(k,images_names):
            k = int(k)
            return [gr.Image(value=item, scale=1, visible=True) for item in images_names] + [gr.Image(scale=1,visible=False)]*(max_textboxes-k)
    
        with gr.Column():
            s = gr.Slider(1, max_textboxes, value=1, step=1, info="أقصى عدد صفحات يمكن توليده هو 10 صفحات",label="كم عدد صفحات القصة التي تريدها؟")
            textboxes = []
            imageboxes = []
            for i in tqdm(range(max_textboxes)):
                with gr.Row():
                    i_t = gr.Image(visible=False)
                    t = gr.Textbox(visible=False)
                    imageboxes.append(i_t)
                    textboxes.append(t)

            segment_list = gr.JSON(value=[],visible=False)
            images_list = gr.JSON(value=[], visible=False)

    submit = gr.Button(value="أنشئ القصة الآن")

    submit.click(
        fn=get_text_images_values,
        inputs=[s,prompt],
        outputs=[segment_list, images_list]
    ).then(
        fn=variable_outputs,
        inputs=[s, segment_list],
        outputs=textboxes,
    ).then(
        fn=variable_outputs_image,
        inputs=[s, images_list],
        outputs=imageboxes,
    )

demo.launch()