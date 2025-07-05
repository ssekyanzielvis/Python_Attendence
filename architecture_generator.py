import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import numpy as np
import pandas as pd
import plotly.io as pio
import os
import logging
from tqdm import tqdm
import importlib.util
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set Plotly renderer to browser for non-Jupyter environments
pio.renderers.default = 'browser'

class AttendanceAppArchitectureDiagrams:
    """Class to generate architecture diagrams for an employee attendance system."""
    
    def __init__(self, output_dir='diagrams', output_format='png'):
        """Initialize the diagram generator with configuration settings."""
        self.config = {
            'colors': {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'accent': '#F18F01',
                'success': '#C73E1D',
                'background': '#F5F5F5',
                'text': '#333333',
                'api': '#4CAF50',
                'database': '#FF9800',
                'mobile': '#2196F3',
                'security': '#F44336',
                'cloud': '#BBDEFB',
                'monitoring': '#4CAF50'
            },
            'figure_size': {
                'system': (16, 12),
                'mobile': (14, 10),
                'api': (16, 12),
                'security': (14, 10),
                'data_flow': (16, 12),
                'file_structure': (16, 24),
                'user_flow': (18, 14),
                'deployment': (16, 12)
            },
            'font_sizes': {
                'title': 18,
                'subtitle': 14,
                'label': 10,
                'small_label': 8
            },
            'output_format': output_format.lower()  # png, svg, or pdf
        }
        self.output_dir = output_dir
        self.diagrams_generated = []
        os.makedirs(self.output_dir, exist_ok=True)
        self.validate_dependencies()
    
    def validate_dependencies(self):
        """Validate that all required dependencies are installed."""
        required = ['matplotlib', 'networkx', 'plotly', 'numpy', 'pandas', 'tqdm']
        for module in required:
            if not importlib.util.find_spec(module):
                logger.error(f"Missing dependency: {module}. Install with 'pip install {module}'")
                raise ImportError(f"Missing dependency: {module}")

    def _add_box(self, ax, pos, size, text, color, boxstyle="round,pad=0.1", linewidth=2, shadow=True):
        """Helper method to add a styled box to a Matplotlib axis."""
        box = FancyBboxPatch(pos, size[0], size[1], boxstyle=boxstyle, 
                            facecolor=color, edgecolor='black', linewidth=linewidth,
                            boxprops=dict(shadow=shadow, pad=0.1))
        ax.add_patch(box)
        ax.text(pos[0] + size[0]/2, pos[1] + size[1]/2, text, 
                ha='center', va='center', fontsize=self.config['font_sizes']['label'], 
                fontweight='bold', color='white')

    def _add_arrow(self, ax, start, end, color='black'):
        """Helper method to add an arrow between two points."""
        arrow = ConnectionPatch(start, end, "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=15, fc=color)
        ax.add_patch(arrow)

    def create_system_overview(self):
        """Create high-level system architecture diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['system'])
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')

            # Title
            ax.text(5, 9.5, 'Employee Attendance System - Architecture Overview', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # Components
            self._add_box(ax, (0.5, 7), (2, 1.5), 'Mobile App\n(React Native/Flutter)', 
                         self.config['colors']['mobile'])
            self._add_box(ax, (4, 7), (2, 1.5), 'API Gateway\n(FastAPI)', 
                         self.config['colors']['api'])
            self._add_box(ax, (7.5, 7), (2, 1.5), 'Authentication\n(JWT)', 
                         self.config['colors']['security'])
            services = [
                ('Attendance\nService', 1, 5),
                ('Employee\nService', 3, 5),
                ('Leave\nService', 5, 5),
                ('QR Code\nService', 7, 5),
                ('Notification\nService', 9, 5)
            ]
            for service, x, y in services:
                self._add_box(ax, (x-0.7, y-0.5), (1.4, 1), service, 
                             self.config['colors']['accent'], linewidth=1)
            self._add_box(ax, (1, 2.5), (2.5, 1.5), 'PostgreSQL\nDatabase', 
                         self.config['colors']['database'])
            self._add_box(ax, (4, 2.5), (2, 1.5), 'Redis\nCache', '#DC382D')
            self._add_box(ax, (6.5, 2.5), (2.5, 1.5), 'External Services\n(Email, SMS, Maps)', 
                         self.config['colors']['secondary'])

            # Arrows
            arrows = [
                ((2.5, 7.75), (4, 7.75)),
                ((6, 7.75), (7.5, 7.75)),
                ((5, 7), (5, 5.5)),
                ((2.25, 4.5), (2.25, 4)),
                ((5, 4.5), (5, 4)),
                ((7.75, 4.5), (7.75, 4))
            ]
            for start, end in arrows:
                self._add_arrow(ax, start, end)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'system_overview.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"System overview diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_system_overview: {e}")

    def create_mobile_app_structure(self):
        """Create mobile app structure diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['mobile'])
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 10)
            ax.axis('off')

            # Title
            ax.text(6, 9.5, 'Mobile App Structure & Architecture', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # App Shell
            self._add_box(ax, (1, 0.5), (10, 8), 'Mobile Application Shell', 
                         'lightgray', boxstyle="round,pad=0.2", shadow=True, linewidth=2)

            # Presentation Layer
            presentation_layers = [
                ('Login/Auth\nScreens', 2, 7),
                ('Dashboard\nScreen', 4, 7),
                ('Attendance\nScreens', 6, 7),
                ('Profile\nScreens', 8, 7),
                ('Settings\nScreens', 10, 7)
            ]
            for layer, x, y in presentation_layers:
                self._add_box(ax, (x-0.7, y-0.4), (1.4, 0.8), layer, 
                             self.config['colors']['mobile'], linewidth=1)

            # Navigation Layer
            self._add_box(ax, (1.5, 5.5), (9, 0.8), 
                         'Navigation Layer (React Navigation / Flutter Navigator)', 
                         self.config['colors']['accent'], linewidth=1)

            # State Management
            state_layers = [
                ('Redux/Bloc\nState Management', 3, 4.5),
                ('Local Storage\n(AsyncStorage)', 6, 4.5),
                ('API Client\n(Axios/Dio)', 9, 4.5)
            ]
            for layer, x, y in state_layers:
                self._add_box(ax, (x-1, y-0.4), (2, 0.8), layer, 
                             self.config['colors']['secondary'], linewidth=1)

            # Native Modules
            native_modules = [
                ('Camera\nModule', 2, 3),
                ('Location\nServices', 4, 3),
                ('Biometric\nAuth', 6, 3),
                ('Push\nNotifications', 8, 3),
                ('QR Scanner', 10, 3)
            ]
            for module, x, y in native_modules:
                self._add_box(ax, (x-0.7, y-0.4), (1.4, 0.8), module, 
                             self.config['colors']['success'], linewidth=1)

            # Device APIs
            self._add_box(ax, (1.5, 1.5), (9, 0.8), 
                         'Device APIs (GPS, Camera, Sensors, Storage)', 
                         'darkgray', linewidth=1)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'mobile_app_structure.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"Mobile app structure diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_mobile_app_structure: {e}")

    def create_api_endpoints_diagram(self):
        """Create API endpoints and communication flow diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['api'])
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 12)
            ax.axis('off')

            # Title
            ax.text(8, 11.5, 'API Endpoints & Communication Flow', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # Components
            self._add_box(ax, (1, 9), (3, 1.5), 'Mobile App\nClient', 
                         self.config['colors']['mobile'])
            self._add_box(ax, (6, 9), (4, 1.5), 'API Gateway\n(FastAPI)', 
                         self.config['colors']['api'])
            self._add_box(ax, (12, 9), (3, 1.5), 'JWT Auth\nMiddleware', 
                         self.config['colors']['security'])

            # API Endpoints
            endpoints = [
                ('Authentication API', '/api/v1/auth/*', 2, 7),
                ('Employee API', '/api/v1/employees/*', 5, 7),
                ('Attendance API', '/api/v1/attendance/*', 8, 7),
                ('Leave API', '/api/v1/leaves/*', 11, 7),
                ('QR Code API', '/api/v1/qr-codes/*', 14, 7)
            ]
            for name, endpoint, x, y in endpoints:
                self._add_box(ax, (x-1, y-0.5), (2, 1), f'{name}\n{endpoint}', 
                             self.config['colors']['accent'], linewidth=1)

            # HTTP Methods
            methods = [
                ('POST /login\nPOST /refresh\nGET /me', 2, 5.5),
                ('GET /\nPOST /\nPUT /{id}\nDELETE /{id}', 5, 5.5),
                ('POST /check-in\nPOST /check-out\nGET /history\nGET /reports', 8, 5.5),
                ('POST /request\nGET /\nPUT /{id}/approve\nGET /balance', 11, 5.5),
                ('POST /generate\nGET /\nPOST /validate\nDELETE /{id}', 14, 5.5)
            ]
            for method, x, y in methods:
                self._add_box(ax, (x-1, y-0.7), (2, 1.4), method, 'lightblue', linewidth=1)

            # Services Layer
            services = [
                ('Auth Service', 2, 3.5),
                ('Employee Service', 5, 3.5),
                ('Attendance Service', 8, 3.5),
                ('Leave Service', 11, 3.5),
                ('QR Service', 14, 3.5)
            ]
            for service, x, y in services:
                self._add_box(ax, (x-1, y-0.4), (2, 0.8), service, 
                             self.config['colors']['secondary'], linewidth=1)

            # Database Layer
            self._add_box(ax, (3, 1.5), (10, 1), 'PostgreSQL Database + Redis Cache', 
                         self.config['colors']['database'])

            # Arrows
            arrows = [
                ((4, 9.75), (6, 9.75)),
                ((10, 9.75), (12, 9.75)),
                ((2, 6.5), (2, 3.9)),
                ((5, 6.5), (5, 3.9)),
                ((8, 6.5), (8, 3.9)),
                ((11, 6.5), (11, 3.9)),
                ((14, 6.5), (14, 3.9)),
                ((8, 3.1), (8, 2.5))
            ]
            for start, end in arrows:
                self._add_arrow(ax, start, end)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'api_endpoints.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"API endpoints diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_api_endpoints_diagram: {e}")

    def create_security_architecture(self):
        """Create security architecture diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['security'])
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 10)
            ax.axis('off')

            # Title
            ax.text(7, 9.5, 'Security Architecture & Data Flow', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # Components
            self._add_box(ax, (1, 7.5), (3, 1.5), 'Mobile Client\n(SSL/TLS)', 
                         self.config['colors']['mobile'])
            self._add_box(ax, (5.5, 7.5), (3, 1.5), 'Security Gateway\n(Rate Limiting)', 
                         self.config['colors']['security'])
            self._add_box(ax, (10, 7.5), (3, 1.5), 'JWT Auth Server\n(Token Validation)', 
                         'darkred')

            # Security Layers
            security_layers = [
                ('Input Validation\n& Sanitization', 2, 6),
                ('CORS Policy\nEnforcement', 5, 6),
                ('Authorization\nMiddleware', 8, 6),
                ('Audit Logging\n& Monitoring', 11, 6)
            ]
            for layer, x, y in security_layers:
                self._add_box(ax, (x-1, y-0.5), (2, 1), layer, 
                             self.config['colors']['accent'], linewidth=1)

            # Data Protection
            protection_layers = [
                ('Password Hashing\n(Bcrypt)', 2, 4),
                ('Data Encryption\n(AES-256)', 5, 4),
                ('Secure Storage\n(Encrypted DB)', 8, 4),
                ('Backup Security\n(Encrypted)', 11, 4)
            ]
            for layer, x, y in protection_layers:
                self._add_box(ax, (x-1, y-0.5), (2, 1), layer, 
                             'darkgreen', linewidth=1)

            # Compliance & Monitoring
            self._add_box(ax, (2, 2), (9, 1), 
                         'Compliance & Monitoring (GDPR, SOC2, Activity Logs)', 
                         'purple')

            # Arrows
            arrows = [
                ((4, 8.25), (5.5, 8.25)),
                ((8.5, 8.25), (10, 8.25)),
                ((2, 7.5), (2, 6.5)),
                ((7, 7.5), (7, 6.5)),
                ((11.5, 7.5), (11.5, 6.5)),
                ((6.5, 5.5), (6.5, 4.5)),
                ((6.5, 3.5), (6.5, 3))
            ]
            for start, end in arrows:
                self._add_arrow(ax, start, end)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'security_architecture.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"Security architecture diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_security_architecture: {e}")

    def create_data_flow_diagram(self):
        """Create data flow diagram using networkx."""
        try:
            G = nx.DiGraph()
            nodes = {
                'Mobile App': {'pos': (0, 2), 'color': self.config['colors']['mobile']},
                'API Gateway': {'pos': (2, 2), 'color': self.config['colors']['api']},
                'Auth Service': {'pos': (4, 3), 'color': self.config['colors']['security']},
                'Attendance Service': {'pos': (4, 2), 'color': self.config['colors']['accent']},
                'Employee Service': {'pos': (4, 1), 'color': self.config['colors']['secondary']},
                'Database': {'pos': (6, 2), 'color': self.config['colors']['database']},
                'Redis Cache': {'pos': (6, 3), 'color': '#DC382D'},
                'External APIs': {'pos': (6, 1), 'color': 'gray'},
                'Push Notifications': {'pos': (2, 0), 'color': 'orange'}
            }
            for node, attrs in nodes.items():
                G.add_node(node, **attrs)
            
            edges = [
                ('Mobile App', 'API Gateway', 'HTTP/HTTPS'),
                ('API Gateway', 'Auth Service', 'JWT Validation'),
                ('API Gateway', 'Attendance Service', 'REST API'),
                ('API Gateway', 'Employee Service', 'REST API'),
                ('Auth Service', 'Database', 'User Auth'),
                ('Attendance Service', 'Database', 'Attendance Data'),
                ('Employee Service', 'Database', 'Employee Data'),
                ('Attendance Service', 'Redis Cache', 'Session Cache'),
                ('Attendance Service', 'External APIs', 'Location/Email'),
                ('Attendance Service', 'Push Notifications', 'Alerts'),
                ('Push Notifications', 'Mobile App', 'FCM/APNS')
            ]
            for source, target, label in edges:
                G.add_edge(source, target, label=label)
            
            plt.figure(figsize=self.config['figure_size']['data_flow'])
            pos = nx.get_node_attributes(G, 'pos')
            colors = [nodes[node]['color'] for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=colors, 
                    node_size=3000, font_size=self.config['font_sizes']['label'], 
                    font_weight='bold', arrows=True, arrowsize=20, edge_color='gray',
                    arrowstyle='->', connectionstyle='arc3,rad=0.1')
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels, 
                                       font_size=self.config['font_sizes']['small_label'])
            
            plt.title('Data Flow & Communication Diagram', 
                     fontsize=self.config['font_sizes']['title'], fontweight='bold', pad=20)
            plt.axis('off')
            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'data_flow.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"Data flow diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_data_flow_diagram: {e}")

    def create_file_structure_diagram(self):
        """Create project file structure diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['file_structure'])
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 28)
            ax.axis('off')

            # Title
            ax.text(8, 27.5, 'Mobile App Project Structure', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # File structure
            structure = [
                ('📱 AttendanceApp/', 0, 26, 'folder'),
                ('├── 📁 src/', 1, 25.5, 'folder'),
                ('│   ├── 📁 components/', 2, 25, 'folder'),
                ('│   │   ├── 📄 LoginForm.tsx', 3, 24.5, 'file'),
                ('│   │   ├── 📄 AttendanceCard.tsx', 3, 24, 'file'),
                ('│   │   ├── 📄 QRScanner.tsx', 3, 23.5, 'file'),
                ('│   │   └── 📄 LocationPicker.tsx', 3, 23, 'file'),
                ('│   ├── 📁 screens/', 2, 22.5, 'folder'),
                ('│   │   ├── 📄 LoginScreen.tsx', 3, 22, 'file'),
                ('│   │   ├── 📄 DashboardScreen.tsx', 3, 21.5, 'file'),
                ('│   │   ├── 📄 AttendanceScreen.tsx', 3, 21, 'file'),
                ('│   │   ├── 📄 ProfileScreen.tsx', 3, 20.5, 'file'),
                ('│   │   └── 📄 SettingsScreen.tsx', 3, 20, 'file'),
                ('│   ├── 📁 navigation/', 2, 19.5, 'folder'),
                ('│   │   ├── 📄 AppNavigator.tsx', 3, 19, 'file'),
                ('│   │   ├── 📄 AuthNavigator.tsx', 3, 18.5, 'file'),
                ('│   │   └── 📄 TabNavigator.tsx', 3, 18, 'file'),
                ('│   ├── 📁 services/', 2, 17.5, 'folder'),
                ('│   │   ├── 📄 ApiService.ts', 3, 17, 'file'),
                ('│   │   ├── 📄 AuthService.ts', 3, 16.5, 'file'),
                ('│   │   ├── 📄 AttendanceService.ts', 3, 16, 'file'),
                ('│   │   ├── 📄 LocationService.ts', 3, 15.5, 'file'),
                ('│   │   └── 📄 NotificationService.ts', 3, 15, 'file'),
                ('│   ├── 📁 store/', 2, 14.5, 'folder'),
                ('│   │   ├── 📄 index.ts', 3, 14, 'file'),
                ('│   │   ├── 📄 authSlice.ts', 3, 13.5, 'file'),
                ('│   │   ├── 📄 attendanceSlice.ts', 3, 13, 'file'),
                ('│   │   └── 📄 userSlice.ts', 3, 12.5, 'file'),
                ('│   ├── 📁 utils/', 2, 12, 'folder'),
                ('│   │   ├── 📄 constants.ts', 3, 11.5, 'file'),
                ('│   │   ├── 📄 helpers.ts', 3, 11, 'file'),
                ('│   │   ├── 📄 validators.ts', 3, 10.5, 'file'),
                ('│   │   └── 📄 storage.ts', 3, 10, 'file'),
                ('│   ├── 📁 types/', 2, 9.5, 'folder'),
                ('│   │   ├── 📄 auth.ts', 3, 9, 'file'),
                ('│   │   ├── 📄 attendance.ts', 3, 8.5, 'file'),
                ('│   │   └── 📄 user.ts', 3, 8, 'file'),
                ('│   └── 📄 App.tsx', 2, 7.5, 'file'),
                ('├── 📁 assets/', 1, 7, 'folder'),
                ('│   ├── 📁 images/', 2, 6.5, 'folder'),
                ('│   ├── 📁 icons/', 2, 6, 'folder'),
                ('│   └── 📁 fonts/', 2, 5.5, 'folder'),
                ('├── 📄 package.json', 1, 5, 'file'),
                ('├── 📄 tsconfig.json', 1, 4.5, 'file'),
                ('└── 📄 README.md', 1, 4, 'file')
            ]
            for item, indent, y, item_type in structure:
                color = self.config['colors']['accent'] if item_type == 'folder' else 'lightblue'
                fontweight = 'bold' if item_type == 'folder' else 'normal'
                ax.text(indent, y, item, fontsize=self.config['font_sizes']['label'], 
                       fontweight=fontweight, va='center', color='black')

            # Descriptions
            descriptions = [
                ('Components: Reusable UI components', 8, 24.5),
                ('Screens: Main application screens', 8, 21.5),
                ('Navigation: App navigation logic', 8, 19),
                ('Services: API and business logic', 8, 16.5),
                ('Store: State management (Redux)', 8, 13.5),
                ('Utils: Helper functions and constants', 8, 11),
                ('Types: TypeScript type definitions', 8, 8.5),
                ('Assets: Images, icons, and fonts', 8, 6)
            ]
            for desc, x, y in descriptions:
                desc_box = FancyBboxPatch((x, y-0.2), 6, 0.4, 
                                        boxstyle="round,pad=0.05", 
                                        facecolor='lightyellow', edgecolor='gray', linewidth=1)
                ax.add_patch(desc_box)
                ax.text(x+3, y, desc, ha='center', va='center', 
                       fontsize=self.config['font_sizes']['small_label'])

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'file_structure.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"File structure diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_file_structure_diagram: {e}")

    def create_user_flow_diagram(self):
        """Create user flow and interaction diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['user_flow'])
            ax.set_xlim(0, 18)
            ax.set_ylim(0, 14)
            ax.axis('off')

            # Title
            ax.text(9, 13.5, 'User Flow & Interaction Diagram', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # User flows
            flows = [
                ('Start', 1, 12, 'start'),
                ('Login Screen', 3, 12, 'screen'),
                ('Enter Credentials', 5, 12, 'action'),
                ('Authenticate', 7, 12, 'process'),
                ('Dashboard', 9, 12, 'screen'),
                ('Attendance Screen', 3, 10, 'screen'),
                ('Choose Method', 5, 10, 'decision'),
                ('QR Scan', 7, 11, 'action'),
                ('Location Check', 7, 9, 'action'),
                ('Verify Location', 9, 10, 'process'),
                ('Record Attendance', 11, 10, 'process'),
                ('Success Message', 13, 10, 'result'),
                ('Leave Screen', 3, 8, 'screen'),
                ('Fill Form', 5, 8, 'action'),
                ('Submit Request', 7, 8, 'process'),
                ('Notification Sent', 9, 8, 'process'),
                ('Approval Status', 11, 8, 'result'),
                ('Profile Screen', 3, 6, 'screen'),
                ('Edit Profile', 5, 6, 'action'),
                ('Update Data', 7, 6, 'process'),
                ('Save Changes', 9, 6, 'result'),
                ('Settings Screen', 3, 4, 'screen'),
                ('Change Settings', 5, 4, 'action'),
                ('Apply Changes', 7, 4, 'process'),
                ('Confirmation', 9, 4, 'result')
            ]

            # Color mapping for different flow types
            flow_colors = {
                'start': 'green',
                'screen': self.config['colors']['mobile'],
                'action': self.config['colors']['accent'],
                'decision': 'orange',
                'process': self.config['colors']['secondary'],
                'result': 'lightgreen'
            }

            # Draw flow elements
            for name, x, y, flow_type in flows:
                color = flow_colors.get(flow_type, 'gray')
                if flow_type == 'decision':
                    diamond = patches.RegularPolygon((x, y), 4, radius=0.5, 
                                                   orientation=np.pi/4,
                                                   facecolor=color, edgecolor='black')
                    ax.add_patch(diamond)
                elif flow_type == 'start':
                    circle = patches.Circle((x, y), 0.3, facecolor=color, edgecolor='black')
                    ax.add_patch(circle)
                else:
                    self._add_box(ax, (x-0.7, y-0.3), (1.4, 0.6), name, color, linewidth=1)

            # Arrows
            flow_arrows = [
                ((1.3, 12), (2.7, 12)),
                ((3.7, 12), (4.3, 12)),
                ((5.7, 12), (6.3, 12)),
                ((7.7, 12), (8.3, 12)),
                ((3, 11.7), (3, 10.3)),
                ((3.7, 10), (4.3, 10)),
                ((5.5, 10.3), (6.5, 10.7)),
                ((5.5, 9.7), (6.5, 9.3)),
                ((7.7, 10), (8.3, 10)),
                ((9.7, 10), (10.3, 10)),
                ((11.7, 10), (12.3, 10)),
                ((3, 9.7), (3, 8.3)),
                ((3.7, 8), (4.3, 8)),
                ((5.7, 8), (6.3, 8)),
                ((7.7, 8), (8.3, 8)),
                ((9.7, 8), (10.3, 8)),
                ((3, 7.7), (3, 6.3)),
                ((3.7, 6), (4.3, 6)),
                ((5.7, 6), (6.3, 6)),
                ((7.7, 6), (8.3, 6)),
                ((3, 5.7), (3, 4.3)),
                ((3.7, 4), (4.3, 4)),
                ((5.7, 4), (6.3, 4)),
                ((7.7, 4), (8.3, 4))
            ]
            for start, end in flow_arrows:
                self._add_arrow(ax, start, end)

            # Legend
            legend_elements = [
                ('Start/End', 'green'),
                ('Screen', self.config['colors']['mobile']),
                ('User Action', self.config['colors']['accent']),
                ('Decision', 'orange'),
                ('Process', self.config['colors']['secondary']),
                ('Result', 'lightgreen')
            ]
            for i, (label, color) in enumerate(legend_elements):
                self._add_box(ax, (15, 12-i*0.5), (1, 0.3), label, color, linewidth=1)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'user_flow.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"User flow diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_user_flow_diagram: {e}")

    def create_deployment_diagram(self):
        """Create deployment architecture diagram."""
        try:
            fig, ax = plt.subplots(figsize=self.config['figure_size']['deployment'])
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 12)
            ax.axis('off')

            # Title
            ax.text(8, 11.5, 'Deployment Architecture', 
                    fontsize=self.config['font_sizes']['title'], fontweight='bold', ha='center')

            # Cloud Infrastructure
            self._add_box(ax, (1, 8), (14, 2.5), 'Cloud Infrastructure (AWS/Azure/GCP)', 
                         self.config['colors']['cloud'], boxstyle="round,pad=0.2", shadow=True, linewidth=2)

            # Load Balancer
            self._add_box(ax, (2, 8.5), (2, 1), 'Load\nBalancer', 'orange', linewidth=1)

            # API Servers
            api_servers = [
                ('API Server 1', 6, 9),
                ('API Server 2', 8, 9),
                ('API Server 3', 10, 9)
            ]
            for server, x, y in api_servers:
                self._add_box(ax, (x-0.7, y-0.4), (1.4, 0.8), server, 
                             self.config['colors']['api'], linewidth=1)

            # Database Cluster
            self._add_box(ax, (12, 8.5), (2.5, 1), 'Database\nCluster', 
                         self.config['colors']['database'], linewidth=1)

            # Services Layer
            services = [
                ('Redis Cache', 2, 6.5),
                ('File Storage', 4.5, 6.5),
                ('Email Service', 7, 6.5),
                ('Push Notifications', 9.5, 6.5),
                ('Monitoring', 12, 6.5)
            ]
            for service, x, y in services:
                self._add_box(ax, (x-0.8, y-0.4), (1.6, 0.8), service, 
                             self.config['colors']['secondary'], linewidth=1)

            # Mobile Clients
            mobile_clients = [
                ('iOS App', 3, 4.5),
                ('Android App', 6, 4.5),
                ('Web App', 9, 4.5)
            ]
            for client, x, y in mobile_clients:
                self._add_box(ax, (x-0.8, y-0.4), (1.6, 0.8), client, 
                             self.config['colors']['mobile'], linewidth=1)

            # CDN
            self._add_box(ax, (12, 4.5), (2, 0.8), 'CDN', 'purple', linewidth=1)

            # Security Layer
            self._add_box(ax, (2, 2.5), (10, 1), 'Security Layer (WAF, DDoS Protection, SSL/TLS)', 
                         self.config['colors']['security'])

            # Monitoring & Analytics
            self._add_box(ax, (2, 1), (10, 1), 'Monitoring & Analytics (Logs, Metrics, Alerts)', 
                         self.config['colors']['monitoring'])

            # Arrows
            deployment_arrows = [
                ((4, 9), (5.3, 9)),
                ((4, 9), (7.3, 9)),
                ((4, 9), (9.3, 9)),
                ((8, 8.6), (12, 8.8)),
                ((3, 5.3), (3, 8.1)),
                ((6, 5.3), (3.5, 8.2)),
                ((9, 5.3), (3.8, 8.3)),
                ((8, 8.6), (8, 7.3))
            ]
            for start, end in deployment_arrows:
                self._add_arrow(ax, start, end)

            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'deployment_architecture.{self.config["output_format"]}')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=self.config['output_format'])
            plt.show()
            plt.close()
            self.diagrams_generated.append(output_path)
            logger.info(f"Deployment diagram saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_deployment_diagram: {e}")

    def create_performance_metrics_dashboard(self):
        """Create performance metrics visualization."""
        try:
            # Sample performance data
            dates = pd.date_range('2024-01-01', periods=30, freq='D')
            api_response_times = np.random.normal(150, 30, 30)  # ms
            database_query_times = np.random.normal(50, 15, 30)  # ms
            active_users = np.random.randint(800, 1200, 30)
            error_rates = np.random.exponential(0.5, 30)  # %

            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('API Response Times', 'Database Performance', 
                              'Active Users', 'Error Rates'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )

            # API Response Times
            fig.add_trace(
                go.Scatter(x=dates, y=api_response_times, 
                          mode='lines+markers', name='Response Time (ms)',
                          line=dict(color=self.config['colors']['primary']),
                          hovertemplate='%{x|%Y-%m-%d}<br>Response Time: %{y:.2f} ms'),
                row=1, col=1
            )

            # Database Performance
            fig.add_trace(
                go.Scatter(x=dates, y=database_query_times, 
                          mode='lines+markers', name='Query Time (ms)',
                          line=dict(color=self.config['colors']['database']),
                          hovertemplate='%{x|%Y-%m-%d}<br>Query Time: %{y:.2f} ms'),
                row=1, col=2
            )

            # Active Users
            fig.add_trace(
                go.Bar(x=dates, y=active_users, name='Active Users',
                       marker_color=self.config['colors']['success'],
                       hovertemplate='%{x|%Y-%m-%d}<br>Active Users: %{y}'),
                row=2, col=1
            )

            # Error Rates
            fig.add_trace(
                go.Scatter(x=dates, y=error_rates, 
                          mode='lines+markers', name='Error Rate (%)',
                          line=dict(color=self.config['colors']['secondary']),
                          hovertemplate='%{x|%Y-%m-%d}<br>Error Rate: %{y:.2f}%'),
                row=2, col=2
            )

            fig.update_layout(
                title_text="Performance Metrics Dashboard",
                title_x=0.5,
                height=800,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            output_path = os.path.join(self.output_dir, 'performance_dashboard.html')
            fig.write_html(output_path)
            fig.show()
            self.diagrams_generated.append(output_path)
            logger.info(f"Performance dashboard saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_performance_metrics_dashboard: {e}")

    def create_interactive_api_documentation(self):
        """Create interactive API documentation diagram."""
        try:
            # API endpoints data
            endpoints_data = {
                'Authentication': {
                    'POST /api/v1/auth/login': 'User login with credentials',
                    'POST /api/v1/auth/refresh': 'Refresh JWT token',
                    'GET /api/v1/auth/me': 'Get current user info',
                    'POST /api/v1/auth/logout': 'User logout'
                },
                'Attendance': {
                    'POST /api/v1/attendance/check-in': 'Check in attendance',
                    'POST /api/v1/attendance/check-out': 'Check out attendance',
                    'GET /api/v1/attendance/today': 'Get today\'s attendance',
                    'GET /api/v1/attendance/history': 'Get attendance history',
                    'GET /api/v1/attendance/reports': 'Generate attendance reports'
                },
                'Employees': {
                    'GET /api/v1/employees/': 'List all employees',
                    'POST /api/v1/employees/': 'Create new employee',
                    'GET /api/v1/employees/{id}': 'Get employee details',
                    'PUT /api/v1/employees/{id}': 'Update employee',
                    'DELETE /api/v1/employees/{id}': 'Delete employee'
                },
                'Leave Management': {
                    'POST /api/v1/leaves/request': 'Submit leave request',
                    'GET /api/v1/leaves/': 'Get leave requests',
                    'PUT /api/v1/leaves/{id}/approve': 'Approve leave request',
                    'PUT /api/v1/leaves/{id}/reject': 'Reject leave request',
                    'GET /api/v1/leaves/balance': 'Get leave balance'
                }
            }

            # Create interactive network graph
            fig = go.Figure()
            categories = list(endpoints_data.keys())
            colors_list = [self.config['colors']['primary'], self.config['colors']['secondary'], 
                          self.config['colors']['accent'], self.config['colors']['success']]

            for i, category in enumerate(categories):
                fig.add_trace(go.Scatter(
                    x=[i*2], y=[0],
                    mode='markers+text',
                    marker=dict(size=50, color=colors_list[i]),
                    text=[category],
                    textposition="middle center",
                    name=category,
                    hovertemplate=f"<b>{category}</b><br>" + 
                                "<br>".join([f"{endpoint}: {desc}" 
                                           for endpoint, desc in endpoints_data[category].items()])
                ))

            fig.update_layout(
                title="Interactive API Documentation",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=600,
                hovermode='closest',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )

            output_path = os.path.join(self.output_dir, 'api_documentation.html')
            fig.write_html(output_path)
            fig.show()
            self.diagrams_generated.append(output_path)
            logger.info(f"Interactive API documentation saved to {output_path}")
        except Exception as e:
            logger.error(f"Error in create_interactive_api_documentation: {e}")

    def generate_summary_report(self):
        """Generate a summary report of all created diagrams."""
        try:
            report = f"# Architecture Diagrams Summary\n\n"
            report += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            report += f"Total Diagrams Generated: {len(self.diagrams_generated)}\n\n"
            report += "## Diagrams\n"
            for i, path in enumerate(self.diagrams_generated, 1):
                report += f"{i}. {os.path.basename(path)}\n"
            
            report_path = os.path.join(self.output_dir, 'diagrams_summary.md')
            with open(report_path, 'w') as f:
                f.write(report)
            logger.info(f"Summary report saved to {report_path}")
        except Exception as e:
            logger.error(f"Error in generate_summary_report: {e}")

def main():
    """Generate all architecture diagrams with progress tracking."""
    try:
        logger.info("Starting diagram generation...")
        generator = AttendanceAppArchitectureDiagrams(output_format='png')
        
        diagram_methods = [
            (generator.create_system_overview, "System Overview"),
            (generator.create_mobile_app_structure, "Mobile App Structure"),
            (generator.create_api_endpoints_diagram, "API Endpoints Diagram"),
            (generator.create_security_architecture, "Security Architecture"),
            (generator.create_data_flow_diagram, "Data Flow Diagram"),
            (generator.create_file_structure_diagram, "File Structure Diagram"),
            (generator.create_user_flow_diagram, "User Flow Diagram"),
            (generator.create_deployment_diagram, "Deployment Diagram"),
            (generator.create_performance_metrics_dashboard, "Performance Dashboard"),
            (generator.create_interactive_api_documentation, "Interactive API Documentation")
        ]
        
        for method, name in tqdm(diagram_methods, desc="Generating Diagrams"):
            logger.info(f"Creating {name}...")
            method()
        
        generator.generate_summary_report()
        logger.info("All diagrams generated successfully!")
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()