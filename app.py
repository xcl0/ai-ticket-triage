import gradio as gr
from main import triage_ticket


def analyze_ticket(text):
    try:
        result = triage_ticket(text)

        return (
            result.summary,
            result.category,
            result.priority,
            result.assigned_team,
            result.reason
        )
    except RuntimeError as error:
        raise gr.Error(str(error)) from error

demo = gr.Interface(
    fn=analyze_ticket,
    inputs=gr.Textbox(
        label="Customer Support Ticket",
        lines=4,
        placeholder="Describe your issue..."
    ),
    outputs=[
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Category"),
        gr.Textbox(label="Priority"),
        gr.Textbox(label="Assigned Team"),
        gr.Textbox(label="Reason")
    ],
    flagging_mode="never",
    title="AI Ticket Triage",
    description="Analyze customer support tickets using Gemini AI."
)

if __name__ == "__main__":
    demo.launch(show_error=True)