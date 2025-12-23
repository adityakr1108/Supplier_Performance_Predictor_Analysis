#!/usr/bin/env python3
"""
Architecture Diagram Generator for Supplier Performance Predictor
Creates a comprehensive system architecture diagram showing all components
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'frontend': '#3498db',      # Blue
        'backend': '#2ecc71',       # Green
        'database': '#f39c12',      # Orange
        'ai': '#9b59b6',           # Purple
        'observability': '#e74c3c', # Red
        'docker': '#34495e',        # Dark gray
        'data': '#1abc9c',         # Teal
        'user': '#95a5a6'          # Light gray
    }
    
    # Title
    ax.text(8, 11.5, 'Supplier Performance Predictor - System Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # User Layer
    user_box = FancyBboxPatch((1, 9.5), 3, 1, boxstyle="round,pad=0.1", 
                              facecolor=colors['user'], edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(2.5, 10, 'Users\n(Admin, Analysts)', fontsize=10, fontweight='bold', 
            ha='center', va='center')
    
    # Frontend Layer
    frontend_box = FancyBboxPatch((5.5, 9.5), 5, 1, boxstyle="round,pad=0.1", 
                                  facecolor=colors['frontend'], edgecolor='black', linewidth=2)
    ax.add_patch(frontend_box)
    ax.text(8, 10, 'Frontend Layer\nHTML/CSS/JavaScript + Jinja2 Templates', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # API Gateway / Load Balancer
    nginx_box = FancyBboxPatch((12, 9.5), 3, 1, boxstyle="round,pad=0.1", 
                               facecolor=colors['docker'], edgecolor='black', linewidth=2)
    ax.add_patch(nginx_box)
    ax.text(13.5, 10, 'Nginx\nReverse Proxy', fontsize=10, fontweight='bold', 
            ha='center', va='center')
    
    # Backend API Layer
    backend_box = FancyBboxPatch((2, 7.5), 6, 1.5, boxstyle="round,pad=0.1", 
                                 facecolor=colors['backend'], edgecolor='black', linewidth=2)
    ax.add_patch(backend_box)
    ax.text(5, 8.25, 'FastAPI Backend\n• Authentication & Authorization\n• RESTful APIs\n• Business Logic', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # AI Services Layer
    ai_box = FancyBboxPatch((9, 7.5), 6, 1.5, boxstyle="round,pad=0.1", 
                            facecolor=colors['ai'], edgecolor='black', linewidth=2)
    ax.add_patch(ai_box)
    ax.text(12, 8.25, 'AI Services Layer\n• Azure OpenAI Integration\n• Supplier Analysis\n• Performance Prediction', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Data Processing Layer
    data_proc_box = FancyBboxPatch((1, 5.5), 4, 1.5, boxstyle="round,pad=0.1", 
                                   facecolor=colors['data'], edgecolor='black', linewidth=2)
    ax.add_patch(data_proc_box)
    ax.text(3, 6.25, 'Data Processing\n• CSV Data Ingestion\n• FAISS Vector DB\n• Data Validation', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Database Layer
    db_box = FancyBboxPatch((6, 5.5), 4, 1.5, boxstyle="round,pad=0.1", 
                            facecolor=colors['database'], edgecolor='black', linewidth=2)
    ax.add_patch(db_box)
    ax.text(8, 6.25, 'Database Layer\n• SQLite (Development)\n• MySQL (Production)\n• User Management & Settings', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Observability Layer
    obs_box = FancyBboxPatch((11, 5.5), 4, 1.5, boxstyle="round,pad=0.1", 
                             facecolor=colors['observability'], edgecolor='black', linewidth=2)
    ax.add_patch(obs_box)
    ax.text(13, 6.25, 'Observability\n• LangSmith Tracing\n• Performance Metrics\n• Error Monitoring', 
            fontsize=10, fontweight='bold', ha='center', va='center')
    
    # External Services
    azure_box = FancyBboxPatch((1, 3.5), 3, 1, boxstyle="round,pad=0.1", 
                               facecolor='#0078d4', edgecolor='black', linewidth=2)
    ax.add_patch(azure_box)
    ax.text(2.5, 4, 'Azure OpenAI\nGPT-4 Models', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white')
    
    langsmith_box = FancyBboxPatch((5, 3.5), 3, 1, boxstyle="round,pad=0.1", 
                                   facecolor='#ff6b35', edgecolor='black', linewidth=2)
    ax.add_patch(langsmith_box)
    ax.text(6.5, 4, 'LangSmith\nAI Observability', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white')
    
    # Docker Infrastructure
    docker_box = FancyBboxPatch((9, 3.5), 6, 1, boxstyle="round,pad=0.1", 
                                facecolor=colors['docker'], edgecolor='black', linewidth=2)
    ax.add_patch(docker_box)
    ax.text(12, 4, 'Docker Infrastructure\nContainerized Deployment with Docker Compose', 
            fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    
    # Data Sources
    data_sources_box = FancyBboxPatch((2, 1.5), 12, 1, boxstyle="round,pad=0.1", 
                                      facecolor=colors['data'], edgecolor='black', linewidth=2)
    ax.add_patch(data_sources_box)
    ax.text(8, 2, 'Data Sources: suppliers.csv | orders.csv | vendors.csv', 
            fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Add connections/arrows
    def add_arrow(start, end, style='<->', color='black'):
        arrow = ConnectionPatch(start, end, "data", "data", 
                               arrowstyle=style, shrinkA=5, shrinkB=5, 
                               mutation_scale=20, fc=color, ec=color, linewidth=2)
        ax.add_artist(arrow)
    
    # User to Frontend
    add_arrow((4, 10), (5.5, 10))
    
    # Frontend to Backend
    add_arrow((8, 9.5), (5, 9))
    
    # Backend to AI Services
    add_arrow((8, 8.25), (9, 8.25))
    
    # Backend to Database
    add_arrow((5, 7.5), (8, 7))
    
    # Backend to Data Processing
    add_arrow((3, 7.5), (3, 7))
    
    # AI Services to Observability
    add_arrow((12, 7.5), (13, 7))
    
    # AI Services to Azure OpenAI
    add_arrow((12, 7.5), (2.5, 4.5))
    
    # Observability to LangSmith
    add_arrow((13, 5.5), (6.5, 4.5))
    
    # Data Processing to Data Sources
    add_arrow((3, 5.5), (5, 2.5))
    
    # Docker Infrastructure connections
    add_arrow((12, 4.5), (8, 7.5))
    add_arrow((12, 4.5), (13, 5.5))
    
    # Add component details in text boxes
    details_text = """
Key Features:
• Multi-tenant Architecture with User Isolation
• Auto-approval System with Admin Controls
• Real-time AI Analysis with Azure OpenAI
• Vector Database for Similarity Search
• Comprehensive Observability with LangSmith
• Production-ready Docker Deployment
• RESTful API with Interactive Documentation
    """
    
    ax.text(0.5, 0.5, details_text, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))
    
    # Add technology stack
    tech_stack = """
Technology Stack:
• Backend: FastAPI, Python 3.9+
• Database: SQLite/MySQL with SQLAlchemy ORM
• AI: Azure OpenAI, FAISS Vector Database
• Frontend: HTML5, CSS3, JavaScript, Jinja2
• Containerization: Docker, Docker Compose
• Observability: LangSmith, Health Checks
• Security: JWT Authentication, CORS
    """
    
    ax.text(0.5, 8.5, tech_stack, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    return fig

def main():
    # Create the diagram
    fig = create_architecture_diagram()
    
    # Save as high-resolution PNG
    plt.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Save as SVG for scalability
    plt.savefig('architecture_diagram.svg', format='svg', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("Architecture diagrams created successfully!")
    print("- architecture_diagram.png (High-resolution PNG)")
    print("- architecture_diagram.svg (Scalable Vector Graphics)")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
