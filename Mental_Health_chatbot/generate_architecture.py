import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Colors
primary_color = '#2E86AB'
secondary_color = '#A23B72'
accent_color = '#F18F01'
bg_color = '#C73E1D'
text_color = '#333333'

# Title
ax.text(5, 9.5, 'Mental Health Chatbot - System Architecture', 
        fontsize=18, fontweight='bold', ha='center', color=text_color)

# Frontend Layer
frontend_box = FancyBboxPatch((0.5, 7.5), 4, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#E8F4FD', 
                              edgecolor=primary_color, 
                              linewidth=2)
ax.add_patch(frontend_box)
ax.text(2.5, 8.6, 'Frontend Layer', fontsize=12, fontweight='bold', ha='center')
ax.text(2.5, 8.2, '• HTML/CSS/JavaScript (index.html, style.css, script.js)', fontsize=9, ha='center')
ax.text(2.5, 7.9, '• Voice Input (Speech Recognition API)', fontsize=9, ha='center')
ax.text(2.5, 7.6, '• Local Storage (Chat History)', fontsize=9, ha='center')

# Interface Options
web_box = FancyBboxPatch((5.5, 8.2), 1.8, 0.6, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#FFF2E8', 
                         edgecolor=accent_color)
ax.add_patch(web_box)
ax.text(6.4, 8.5, 'Web Interface', fontsize=9, fontweight='bold', ha='center')

gradio_box = FancyBboxPatch((5.5, 7.5), 1.8, 0.6, 
                            boxstyle="round,pad=0.05", 
                            facecolor='#FFF2E8', 
                            edgecolor=accent_color)
ax.add_patch(gradio_box)
ax.text(6.4, 7.8, 'Gradio UI', fontsize=9, fontweight='bold', ha='center')

telegram_box = FancyBboxPatch((7.5, 7.5), 1.8, 1.3, 
                              boxstyle="round,pad=0.05", 
                              facecolor='#FFF2E8', 
                              edgecolor=accent_color)
ax.add_patch(telegram_box)
ax.text(8.4, 8.4, 'Telegram Bot', fontsize=9, fontweight='bold', ha='center')
ax.text(8.4, 8.1, '(telegram_bot.py)', fontsize=8, ha='center')

# API Layer
api_box = FancyBboxPatch((0.5, 5.5), 9, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor='#F0F8E8', 
                         edgecolor=secondary_color, 
                         linewidth=2)
ax.add_patch(api_box)
ax.text(5, 6.6, 'API Layer - Flask Backend (app.py)', fontsize=12, fontweight='bold', ha='center')
ax.text(5, 6.2, '• REST API Endpoints (/chat, /)', fontsize=10, ha='center')
ax.text(5, 5.9, '• CORS Configuration • Request/Response Handling • Error Management', fontsize=10, ha='center')


core_box = FancyBboxPatch((0.5, 3.5), 9, 1.5, 
                          boxstyle="round,pad=0.1", 
                          facecolor='#FDF2F8', 
                          edgecolor=bg_color, 
                          linewidth=2)
ax.add_patch(core_box)
ax.text(5, 4.6, 'Core Logic Layer - Chatbot Agent (chat_bot_agent.py)', fontsize=12, fontweight='bold', ha='center')
ax.text(5, 4.2, '• Agent Configuration (template.json) • Language Support (EN/Tamil)', fontsize=10, ha='center')
ax.text(5, 3.9, '• Multi-Model Support (OpenAI GPT-4o / Groq) • DuckDuckGo Search Integration', fontsize=10, ha='center')


openai_box = FancyBboxPatch((0.5, 1.5), 2, 1.2, 
                            boxstyle="round,pad=0.1", 
                            facecolor='#E8F5E8', 
                            edgecolor='#10B981')
ax.add_patch(openai_box)
ax.text(1.5, 2.3, 'OpenAI', fontsize=10, fontweight='bold', ha='center')
ax.text(1.5, 2.0, 'GPT-4o', fontsize=9, ha='center')
ax.text(1.5, 1.7, '(Tamil)', fontsize=9, ha='center')

groq_box = FancyBboxPatch((3, 1.5), 2, 1.2, 
                          boxstyle="round,pad=0.1", 
                          facecolor='#E8F5E8', 
                          edgecolor='#10B981')
ax.add_patch(groq_box)
ax.text(4, 2.3, 'Groq', fontsize=10, fontweight='bold', ha='center')
ax.text(4, 2.0, 'LLM Models', fontsize=9, ha='center')
ax.text(4, 1.7, '(English)', fontsize=9, ha='center')

search_box = FancyBboxPatch((5.5, 1.5), 2, 1.2, 
                            boxstyle="round,pad=0.1", 
                            facecolor='#E8F5E8', 
                            edgecolor='#10B981')
ax.add_patch(search_box)
ax.text(6.5, 2.3, 'DuckDuckGo', fontsize=10, fontweight='bold', ha='center')
ax.text(6.5, 2.0, 'Search API', fontsize=9, ha='center')
ax.text(6.5, 1.7, '(Real-time Info)', fontsize=9, ha='center')

env_box = FancyBboxPatch((8, 1.5), 1.5, 1.2, 
                         boxstyle="round,pad=0.1", 
                         facecolor='#FEF3C7', 
                         edgecolor='#F59E0B')
ax.add_patch(env_box)
ax.text(8.75, 2.3, 'Environment', fontsize=9, fontweight='bold', ha='center')
ax.text(8.75, 2.0, 'Variables', fontsize=9, ha='center')
ax.text(8.75, 1.7, '(.env)', fontsize=9, ha='center')

# Data Flow Arrows
# Frontend to API
arrow1 = ConnectionPatch((2.5, 7.5), (5, 7.0), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc=primary_color, ec=primary_color)
ax.add_patch(arrow1)

# Gradio to Core
arrow2 = ConnectionPatch((6.4, 7.5), (5, 5.0), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc=accent_color, ec=accent_color)
ax.add_patch(arrow2)

# Telegram to Core
arrow3 = ConnectionPatch((8.4, 7.5), (6, 5.0), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc=accent_color, ec=accent_color)
ax.add_patch(arrow3)

# API to Core
arrow4 = ConnectionPatch((5, 5.5), (5, 5.0), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc=secondary_color, ec=secondary_color)
ax.add_patch(arrow4)

# Core to External Services
arrow5 = ConnectionPatch((3.5, 3.5), (1.5, 2.7), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc='#10B981', ec='#10B981')
ax.add_patch(arrow5)

arrow6 = ConnectionPatch((4.5, 3.5), (4, 2.7), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc='#10B981', ec='#10B981')
ax.add_patch(arrow6)

arrow7 = ConnectionPatch((6.5, 3.5), (6.5, 2.7), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc='#10B981', ec='#10B981')
ax.add_patch(arrow7)

# Features Box
features_box = FancyBboxPatch((0.5, 0.2), 9, 0.8, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#F8F9FA', 
                              edgecolor='#6C757D')
ax.add_patch(features_box)
ax.text(5, 0.7, 'Key Features', fontsize=11, fontweight='bold', ha='center')
ax.text(5, 0.4, '• Multi-language Support (English/Tamil) • Voice Input • Chat History • Theme Toggle ', fontsize=9, ha='center')

plt.tight_layout()
plt.savefig('mental_health_chatbot_architecture.png', dpi=300, bbox_inches='tight')
plt.show()

print("Architecture diagram saved as 'mental_health_chatbot_architecture.png'")