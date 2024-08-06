import gradio as gr
from src.utils.ui_settings import UISettings
from src.utils.load_config import LoadConfig
from src.utils.chatbot import ChatBot

CONFIG = LoadConfig()


class HomeApp:
    """
    This class loads gradio interface.
    """
    def __init__(self):
        self.chat_bot = ChatBot()

    def clear_pressed(self):
        # Clear the second history in the chatbot
        self.chat_bot.clear_second_history(flag=True)
        print("Clear button was pressed.")

    def launch_interface(self):
        # Define the Gradio interface
        with gr.Blocks() as demo:
            with gr.Tabs():
                with gr.TabItem("HomeApp"):
                    ############
                    # First ROW:
                    ############
                    with gr.Row() as row_one:
                        chatbot = gr.Chatbot(
                            CONFIG.default_message,
                            elem_id="chatbot",
                            bubble_full_width=False,
                            height=500
                        )
                        # **Adding like/dislike icons
                        chatbot.like(UISettings.feedback, None, None)
                    #############
                    # SECOND ROW:
                    #############
                    with gr.Row():
                        input_txt = gr.Textbox(
                            lines=4,
                            scale=8,
                            placeholder="Enter text and press enter",
                            container=False,
                        )
                    ############
                    # Third ROW:
                    ############
                    with gr.Row() as row_two:
                        text_submit_btn = gr.Button(value="Submit text")
                        clear_button = gr.ClearButton([input_txt, chatbot])
                        clear_button.click(fn=self.clear_pressed)

                    ##########
                    # Process:
                    ##########
                    txt_msg = input_txt.submit(fn=self.chat_bot.respond,
                                               inputs=[chatbot, input_txt],
                                               outputs=[input_txt, chatbot],
                                               queue=False).then(lambda: gr.Textbox(interactive=True),
                                                                 None, [input_txt], queue=False)
                    submit_btn = text_submit_btn.click(fn=self.chat_bot.respond,
                                                       inputs=[chatbot, input_txt],
                                                       outputs=[input_txt, chatbot],
                                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                                         None, [input_txt], queue=False)

        # Launch the Gradio interface
        demo.launch()


if __name__ == "__main__":
    app = HomeApp()
    app.launch_interface()
