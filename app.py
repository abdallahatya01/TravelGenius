import gradio as gr
from crewai import Crew
from agents import create_travel_planner_agent
from tasks import create_travel_planning_task
from tools import web_search_tool
from config import TAVILY_API_KEY, GROQ_API_KEY

# ============================
#     MAIN TRAVEL FUNCTION
# ============================
def generate_travel_plan(destination, budget, days, travelers):
    """Generates travel plan for Markdown display"""
    
    if not TAVILY_API_KEY or not GROQ_API_KEY:
        msg = "❌ **Error**: Check your API keys in the .env file (TAVILY_API_KEY, GROQ_API_KEY)"
        yield msg

    try:
        loading = "⏳ **Planning your trip...** (may take 30–60 seconds)"
        yield loading

        # Create agent and task
        planner_agent = create_travel_planner_agent()
        planning_task = create_travel_planning_task(planner_agent, web_search_tool)

        crew = Crew(
            agents=[planner_agent],
            tasks=[planning_task],
            verbose=False,
        )

        inputs = {
            "destination": destination,
            "budget": float(budget),
            "days": int(days),
            "travelers": int(travelers)
        }

        result = crew.kickoff(inputs=inputs)

        if hasattr(result, 'raw'):
            output_text = result.raw
        elif isinstance(result, str):
            output_text = result
        else:
            output_text = str(result)

        yield output_text

    except Exception as e:
        err = f"❌ **Error during planning**: {str(e)}"
        yield err


# ============================
#     GRADIO UI
# ============================
def create_gradio_interface():
    with gr.Blocks(title="🌍 Smart Travel Assistant", theme=gr.themes.Soft()) as app:

        gr.Markdown("""
            # 🌍 Smart Travel Assistant
            Plan your trip intelligently and get a complete itinerary including flights, accommodations, attractions, and restaurants.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                destination = gr.Textbox(
                    label="🎯 Destination",
                    placeholder="Example: Russia - Moscow & St. Petersburg",
                    value="Russia - Moscow"
                )
                budget = gr.Number(label="💰 Budget (USD)", value=2500, minimum=500, step=100)
                days = gr.Slider(label="📅 Number of days", minimum=3, maximum=21, value=7, step=1)
                travelers = gr.Number(label="👥 Number of travelers", value=1, minimum=1, step=1)
                generate_btn = gr.Button("🚀 Generate Travel Plan", variant="primary")

            with gr.Column(scale=2):
                # Markdown للعرض
                output_md = gr.Markdown("Click the button to generate your travel plan...")

        # زر توليد الخطة
        generate_btn.click(
            fn=generate_travel_plan,
            inputs=[destination, budget, days, travelers],
            outputs=output_md
        )

        # أمثلة جاهزة
        gr.Examples(
            examples=[
                ["Russia - Moscow & St. Petersburg", 2500, 10, 1],
                ["Japan - Tokyo", 3000, 7, 2],
                ["Turkey - Istanbul", 1500, 5, 1],
                ["Egypt - Cairo & Luxor", 1200, 6, 1],
            ],
            inputs=[destination, budget, days, travelers]
        )

    return app


# ============================
#     MAIN APP START
# ============================
if __name__ == "__main__":
    travel_app = create_gradio_interface()

    print("\n" + "="*60)
    print("🌍 Travel Genius AI Assistant is Starting...")
    print("="*60)
    print("✅ Running at: http://localhost:7860")
    print("="*60 + "\n")

    travel_app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True,
    )
