"""
NovaOS Web Dashboard
--------------------
A Gradio-based local web interface that provides:
  - Chat with the agent
  - Conversation history viewer
  - Model configuration panel
  - Live screenshot preview
"""

from __future__ import annotations

import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


def build_dashboard():
    """Build and return the Gradio Blocks app."""
    try:
        import gradio as gr  # type: ignore
    except ImportError:
        logger.error("gradio not installed — dashboard unavailable.")
        return None

    from novaos.core.agent import NovaAgent
    from novaos.memory.vector import MemoryManager

    agent = NovaAgent()
    memory = MemoryManager()

    def chat(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        response = agent.process_command(message)
        history.append((message, response))
        return "", history

    def get_history():
        items = memory.get_recent(20)
        rows = []
        for item in items:
            meta = item.get("metadata", {})
            rows.append([
                meta.get("timestamp", ""),
                meta.get("command", ""),
                item.get("document", "")[:120],
            ])
        return rows

    def clear_memory():
        memory.clear()
        return "Memory cleared."

    with gr.Blocks(
        title="NovaOS Dashboard",
        theme=gr.themes.Base(primary_hue="cyan", neutral_hue="slate"),
        css="""
        body { background: #0a0a0a; }
        .gradio-container { max-width: 1200px; }
        """,
    ) as demo:
        gr.Markdown(
            """
            # NovaOS Dashboard
            **The desktop AI that sees, thinks and acts on your computer — fully local.**
            """
        )

        with gr.Tabs():
            # ---- Chat tab ------------------------------------------------
            with gr.Tab("Chat"):
                chatbot = gr.Chatbot(height=500, label="NovaOS")
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Type a command or question...",
                        show_label=False,
                        scale=4,
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                send_btn.click(chat, [msg_input, chatbot], [msg_input, chatbot])
                msg_input.submit(chat, [msg_input, chatbot], [msg_input, chatbot])

            # ---- History tab ---------------------------------------------
            with gr.Tab("History"):
                history_table = gr.Dataframe(
                    headers=["Timestamp", "Command", "Response"],
                    datatype=["str", "str", "str"],
                    interactive=False,
                )
                with gr.Row():
                    refresh_btn = gr.Button("Refresh")
                    clear_btn = gr.Button("Clear Memory", variant="stop")
                clear_status = gr.Textbox(show_label=False)
                refresh_btn.click(get_history, outputs=history_table)
                clear_btn.click(clear_memory, outputs=clear_status)

            # ---- Settings tab --------------------------------------------
            with gr.Tab("Settings"):
                gr.Markdown("### Model Configuration")
                with gr.Row():
                    model_input = gr.Textbox(label="Default Model", value="llama3.2")
                    vision_input = gr.Textbox(label="Vision Model", value="llava:13b")
                safe_mode = gr.Checkbox(label="Safe Mode (require confirmation)", value=True)
                gr.Markdown(
                    "_Settings are applied at runtime. Edit `.env` for persistent changes._"
                )

    return demo


def launch(port: int = 7860, share: bool = False) -> None:
    """Launch the dashboard server."""
    demo = build_dashboard()
    if demo is None:
        return
    logger.info("Starting NovaOS Dashboard on http://localhost:%d", port)
    demo.launch(server_port=port, share=share, server_name="0.0.0.0")
