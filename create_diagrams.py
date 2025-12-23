#!/usr/bin/env python3
"""
Component Diagram Generator for Supplier Performance Predictor
Creates detailed component interaction diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import matplotlib.pyplot as plt

def create_component_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Supplier Performance Predictor - Component Interactions', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Define colors
    colors = {
        'user': '#3498db',
        'web': '#2ecc71', 
        'api': '#f39c12',
        'ai': '#9b59b6',
        'data': '#e74c3c',
        'external': '#34495e'
    }
    
    # User Components
    user_circle = Circle((1, 8), 0.5, facecolor=colors['user'], edgecolor='black')
    ax.add_patch(user_circle)
    ax.text(1, 8, 'User', fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Web Frontend Components
    frontend_box = FancyBboxPatch((2.5, 7), 2, 2, boxstyle="round,pad=0.1",
                                  facecolor=colors['web'], edgecolor='black')
    ax.add_patch(frontend_box)
    ax.text(3.5, 8, 'Frontend\n• Dashboard\n• Admin Panel\n• Forms', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # API Gateway
    api_box = FancyBboxPatch((6, 7), 2, 2, boxstyle="round,pad=0.1",
                             facecolor=colors['api'], edgecolor='black')
    ax.add_patch(api_box)
    ax.text(7, 8, 'FastAPI\n• Auth\n• Routes\n• Validation', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # AI Components
    ai_box = FancyBboxPatch((9.5, 7), 2, 2, boxstyle="round,pad=0.1",
                            facecolor=colors['ai'], edgecolor='black')
    ax.add_patch(ai_box)
    ax.text(10.5, 8, 'AI Engine\n• OpenAI\n• FAISS\n• Analysis', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Database Components
    db_box = FancyBboxPatch((2.5, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                            facecolor=colors['data'], edgecolor='black')
    ax.add_patch(db_box)
    ax.text(3.5, 5.25, 'Database\n• Users\n• Settings\n• Logs', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Data Processing
    data_proc_box = FancyBboxPatch((6, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                                   facecolor=colors['data'], edgecolor='black')
    ax.add_patch(data_proc_box)
    ax.text(7, 5.25, 'Data Layer\n• CSV Parser\n• Vector DB\n• Cache', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # External Services
    azure_box = FancyBboxPatch((9.5, 4.5), 2, 1.5, boxstyle="round,pad=0.1",
                               facecolor=colors['external'], edgecolor='black')
    ax.add_patch(azure_box)
    ax.text(10.5, 5.25, 'External\n• Azure AI\n• LangSmith\n• APIs', 
            fontsize=9, fontweight='bold', ha='center', va='center', color='white')
    
    # File System
    files_box = FancyBboxPatch((2.5, 2), 5, 1.5, boxstyle="round,pad=0.1",
                               facecolor='#95a5a6', edgecolor='black')
    ax.add_patch(files_box)
    ax.text(5, 2.75, 'File System\nsuppliers.csv | orders.csv | vendors.csv', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Docker Container boundary
    container_box = FancyBboxPatch((1.5, 1.5), 10, 8, boxstyle="round,pad=0.2",
                                   facecolor='none', edgecolor='blue', linewidth=3, linestyle='--')
    ax.add_patch(container_box)
    ax.text(6.5, 1.7, 'Docker Container', fontsize=10, fontweight='bold', 
            ha='center', color='blue')
    
    # Add arrows for data flow
    def add_simple_arrow(start, end, color='black'):
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color=color))
    
    # User interactions
    add_simple_arrow((1.5, 8), (2.5, 8), 'blue')
    add_simple_arrow((4.5, 8), (6, 8), 'green')
    add_simple_arrow((8, 8), (9.5, 8), 'purple')
    
    # Database connections
    add_simple_arrow((6.5, 7), (4, 6), 'red')
    add_simple_arrow((7, 7), (7, 6), 'red')
    add_simple_arrow((10, 7), (10, 6), 'gray')
    
    # File system access
    add_simple_arrow((5, 4.5), (5, 3.5), 'orange')
    
    # Add legend
    legend_elements = [
        ('User Interface', colors['user']),
        ('Web Components', colors['web']),
        ('API Layer', colors['api']),
        ('AI Services', colors['ai']),
        ('Data Storage', colors['data']),
        ('External APIs', colors['external'])
    ]
    
    for i, (label, color) in enumerate(legend_elements):
        y_pos = 0.8 - i * 0.1
        rect = FancyBboxPatch((12.5, y_pos-0.03), 0.3, 0.06, 
                              facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        ax.text(12.9, y_pos, label, fontsize=8, va='center')
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'Data Flow - Supplier Analysis Process', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Process boxes
    processes = [
        ((1, 6), "CSV\nUpload"),
        ((3, 6), "Data\nValidation"),
        ((5, 6), "Vector\nEmbedding"),
        ((7, 6), "AI\nAnalysis"),
        ((9, 6), "Results\nProcessing"),
        ((11, 6), "UI\nDisplay")
    ]
    
    for (x, y), label in processes:
        box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, 
                             boxstyle="round,pad=0.05",
                             facecolor='lightblue', edgecolor='black')
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Add arrows between processes
    for i in range(len(processes)-1):
        start_x = processes[i][0][0] + 0.4
        end_x = processes[i+1][0][0] - 0.4
        y = 6
        ax.annotate('', xy=(end_x, y), xytext=(start_x, y),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    
    # Add database interactions
    db_box = FancyBboxPatch((4, 3.5), 4, 1, boxstyle="round,pad=0.1",
                            facecolor='orange', edgecolor='black')
    ax.add_patch(db_box)
    ax.text(6, 4, 'Database Operations\nStore Results | Retrieve History | User Data', 
            fontsize=9, fontweight='bold', ha='center', va='center')
    
    # Database arrows
    ax.annotate('', xy=(5, 5.7), xytext=(5.5, 4.5),
               arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.annotate('', xy=(7, 5.7), xytext=(6.5, 4.5),
               arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.annotate('', xy=(9, 5.7), xytext=(7.5, 4.5),
               arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    
    # External services
    ext_box = FancyBboxPatch((1, 2), 10, 1, boxstyle="round,pad=0.1",
                             facecolor='purple', edgecolor='black')
    ax.add_patch(ext_box)
    ax.text(6, 2.5, 'External Services: Azure OpenAI API | LangSmith Tracing | Health Monitoring', 
            fontsize=9, fontweight='bold', ha='center', va='center', color='white')
    
    # External service arrows
    ax.annotate('', xy=(7, 5.7), xytext=(6, 3),
               arrowprops=dict(arrowstyle='<->', lw=2, color='purple'))
    
    plt.tight_layout()
    return fig

def main():
    # Create component diagram
    fig1 = create_component_diagram()
    plt.savefig('component_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    # Create data flow diagram
    fig2 = create_data_flow_diagram()
    plt.savefig('dataflow_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("Additional diagrams created successfully!")
    print("- component_diagram.png (Component interactions)")
    print("- dataflow_diagram.png (Data flow visualization)")

if __name__ == "__main__":
    main()
