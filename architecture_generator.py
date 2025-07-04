import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import numpy as np
from datetime import datetime
import json

class AttendanceAppArchitectureDiagrams:
    def __init__(self):
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'background': '#F5F5F5',
            'text': '#333333',
            'api': '#4CAF50',
            'database': '#FF9800',
            'mobile': '#2196F3',
            'security': '#F44336'
        }
        
    def create_system_overview(self):
        """Create high-level system architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'Employee Attendance System - Architecture Overview', 
                fontsize=20, fontweight='bold', ha='center')
        
        # Mobile App Layer
        mobile_box = FancyBboxPatch((0.5, 7), 2, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=self.colors['mobile'], 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(mobile_box)
        ax.text(1.5, 7.75, 'Mobile App\n(React Native/Flutter)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # API Gateway
        api_box = FancyBboxPatch((4, 7), 2, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=self.colors['api'], 
                                edgecolor='black', linewidth=2)
        ax.add_patch(api_box)
        ax.text(5, 7.75, 'API Gateway\n(FastAPI)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Authentication Service
        auth_box = FancyBboxPatch((7.5, 7), 2, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=self.colors['security'], 
                                 edgecolor='black', linewidth=2)
        ax.add_patch(auth_box)
        ax.text(8.5, 7.75, 'Authentication\n(JWT)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Business Logic Layer
        services = [
            ('Attendance\nService', 1, 5),
            ('Employee\nService', 3, 5),
            ('Leave\nService', 5, 5),
            ('QR Code\nService', 7, 5),
            ('Notification\nService', 9, 5)
        ]
        
        for service, x, y in services:
            service_box = FancyBboxPatch((x-0.7, y-0.5), 1.4, 1, 
                                        boxstyle="round,pad=0.05", 
                                        facecolor=self.colors['accent'], 
                                        edgecolor='black', linewidth=1)
            ax.add_patch(service_box)
            ax.text(x, y, service, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Data Layer
        db_box = FancyBboxPatch((1, 2.5), 2.5, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=self.colors['database'], 
                               edgecolor='black', linewidth=2)
        ax.add_patch(db_box)
        ax.text(2.25, 3.25, 'PostgreSQL\nDatabase', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        redis_box = FancyBboxPatch((4, 2.5), 2, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor='#DC382D', 
                                  edgecolor='black', linewidth=2)
        ax.add_patch(redis_box)
        ax.text(5, 3.25, 'Redis\nCache', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # External Services
        ext_box = FancyBboxPatch((6.5, 2.5), 2.5, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor=self.colors['secondary'], 
                                edgecolor='black', linewidth=2)
        ax.add_patch(ext_box)
        ax.text(7.75, 3.25, 'External Services\n(Email, SMS, Maps)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Add arrows showing data flow
        arrows = [
            # Mobile to API
            ((2.5, 7.75), (4, 7.75)),
            # API to Auth
            ((6, 7.75), (7.5, 7.75)),
            # API to Services
            ((5, 7), (5, 5.5)),
            # Services to Database
            ((2.25, 4.5), (2.25, 4)),
            ((5, 4.5), (5, 4)),
            ((7.75, 4.5), (7.75, 4))
        ]
        
        for start, end in arrows:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="black")
            ax.add_patch(arrow)
        
        plt.tight_layout()
        plt.savefig('diagrams/system_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_mobile_app_structure(self):
        """Create mobile app structure diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(6, 9.5, 'Mobile App Structure & Architecture', 
                fontsize=18, fontweight='bold', ha='center')
        
        # App Shell
        shell_box = FancyBboxPatch((1, 0.5), 10, 8, 
                                  boxstyle="round,pad=0.2", 
                                  facecolor='lightgray', 
                                  edgecolor='black', linewidth=2, alpha=0.3)
        ax.add_patch(shell_box)
        ax.text(6, 8.2, 'Mobile Application Shell', 
                ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Presentation Layer
        presentation_layers = [
            ('Login/Auth\nScreens', 2, 7),
            ('Dashboard\nScreen', 4, 7),
            ('Attendance\nScreens', 6, 7),
            ('Profile\nScreens', 8, 7),
            ('Settings\nScreens', 10, 7)
        ]
        
        for layer, x, y in presentation_layers:
            layer_box = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor=self.colors['mobile'], 
                                      edgecolor='black', linewidth=1)
            ax.add_patch(layer_box)
            ax.text(x, y, layer, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Navigation Layer
        nav_box = FancyBboxPatch((1.5, 5.5), 9, 0.8, 
                                boxstyle="round,pad=0.05", 
                                facecolor=self.colors['accent'], 
                                edgecolor='black', linewidth=1)
        ax.add_patch(nav_box)
        ax.text(6, 5.9, 'Navigation Layer (React Navigation / Flutter Navigator)', 
                ha='center', va='center', fontsize=11, fontweight='bold')
        
        # State Management
        state_layers = [
            ('Redux/Bloc\nState Management', 3, 4.5),
            ('Local Storage\n(AsyncStorage)', 6, 4.5),
            ('API Client\n(Axios/Dio)', 9, 4.5)
        ]
        
        for layer, x, y in state_layers:
            layer_box = FancyBboxPatch((x-1, y-0.4), 2, 0.8, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor=self.colors['secondary'], 
                                      edgecolor='black', linewidth=1)
            ax.add_patch(layer_box)
            ax.text(x, y, layer, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Native Modules
        native_modules = [
            ('Camera\nModule', 2, 3),
            ('Location\nServices', 4, 3),
            ('Biometric\nAuth', 6, 3),
            ('Push\nNotifications', 8, 3),
            ('QR Scanner', 10, 3)
        ]
        
        for module, x, y in native_modules:
            module_box = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8, 
                                       boxstyle="round,pad=0.05", 
                                       facecolor=self.colors['success'], 
                                       edgecolor='black', linewidth=1)
            ax.add_patch(module_box)
            ax.text(x, y, module, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Device APIs
        device_box = FancyBboxPatch((1.5, 1.5), 9, 0.8, 
                                   boxstyle="round,pad=0.05", 
                                   facecolor='darkgray', 
                                   edgecolor='black', linewidth=1)
        ax.add_patch(device_box)
        ax.text(6, 1.9, 'Device APIs (GPS, Camera, Sensors, Storage)', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        plt.tight_layout()
        plt.savefig('diagrams/mobile_app_structure.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_api_endpoints_diagram(self):
        """Create API endpoints and communication flow diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Title
        ax.text(8, 11.5, 'API Endpoints & Communication Flow', 
                fontsize=18, fontweight='bold', ha='center')
        
        # Mobile App
        mobile_box = FancyBboxPatch((1, 9), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=self.colors['mobile'], 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(mobile_box)
        ax.text(2.5, 9.75, 'Mobile App\nClient', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # API Gateway
        gateway_box = FancyBboxPatch((6, 9), 4, 1.5, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor=self.colors['api'], 
                                    edgecolor='black', linewidth=2)
        ax.add_patch(gateway_box)
        ax.text(8, 9.75, 'API Gateway\n(FastAPI)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Authentication Middleware
        auth_box = FancyBboxPatch((12, 9), 3, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=self.colors['security'], 
                                 edgecolor='black', linewidth=2)
        ax.add_patch(auth_box)
        ax.text(13.5, 9.75, 'JWT Auth\nMiddleware', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # API Endpoints
        endpoints = [
            ('Authentication API', '/api/v1/auth/*', 2, 7),
            ('Employee API', '/api/v1/employees/*', 5, 7),
            ('Attendance API', '/api/v1/attendance/*', 8, 7),
            ('Leave API', '/api/v1/leaves/*', 11, 7),
            ('QR Code API', '/api/v1/qr-codes/*', 14, 7)
        ]
        
        for name, endpoint, x, y in endpoints:
            endpoint_box = FancyBboxPatch((x-1, y-0.5), 2, 1, 
                                         boxstyle="round,pad=0.05", 
                                         facecolor=self.colors['accent'], 
                                         edgecolor='black', linewidth=1)
            ax.add_patch(endpoint_box)
            ax.text(x, y, f'{name}\n{endpoint}', 
                   ha='center', va='center', fontsize=8, fontweight='bold')
        
        # HTTP Methods
       # ... continuing from previous code

        methods = [
            ('POST /login\nPOST /refresh\nGET /me', 2, 5.5),
            ('GET /\nPOST /\nPUT /{id}\nDELETE /{id}', 5, 5.5),
            ('POST /check-in\nPOST /check-out\nGET /history\nGET /reports', 8, 5.5),
            ('POST /request\nGET /\nPUT /{id}/approve\nGET /balance', 11, 5.5),
            ('POST /generate\nGET /\nPOST /validate\nDELETE /{id}', 14, 5.5)
        ]
        
        for method, x, y in methods:
            method_box = FancyBboxPatch((x-1, y-0.7), 2, 1.4, 
                                       boxstyle="round,pad=0.05", 
                                       facecolor='lightblue', 
                                       edgecolor='black', linewidth=1)
            ax.add_patch(method_box)
            ax.text(x, y, method, ha='center', va='center', fontsize=7, fontweight='bold')
        
        # Services Layer
        services = [
            ('Auth Service', 2, 3.5),
            ('Employee Service', 5, 3.5),
            ('Attendance Service', 8, 3.5),
            ('Leave Service', 11, 3.5),
            ('QR Service', 14, 3.5)
        ]
        
        for service, x, y in services:
            service_box = FancyBboxPatch((x-1, y-0.4), 2, 0.8, 
                                        boxstyle="round,pad=0.05", 
                                        facecolor=self.colors['secondary'], 
                                        edgecolor='black', linewidth=1)
            ax.add_patch(service_box)
            ax.text(x, y, service, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Database Layer
        db_box = FancyBboxPatch((3, 1.5), 10, 1, 
                               boxstyle="round,pad=0.1", 
                               facecolor=self.colors['database'], 
                               edgecolor='black', linewidth=2)
        ax.add_patch(db_box)
        ax.text(8, 2, 'PostgreSQL Database + Redis Cache', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Add communication arrows
        arrows = [
            # Mobile to Gateway
            ((4, 9.75), (6, 9.75)),
            # Gateway to Auth
            ((10, 9.75), (12, 9.75)),
            # Endpoints to Services
            ((2, 6.5), (2, 3.9)),
            ((5, 6.5), (5, 3.9)),
            ((8, 6.5), (8, 3.9)),
            ((11, 6.5), (11, 3.9)),
            ((14, 6.5), (14, 3.9)),
            # Services to Database
            ((8, 3.1), (8, 2.5))
        ]
        
        for start, end in arrows:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="black")
            ax.add_patch(arrow)
        
        plt.tight_layout()
        plt.savefig('diagrams/api_endpoints.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_security_architecture(self):
        """Create security architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(7, 9.5, 'Security Architecture & Data Flow', 
                fontsize=18, fontweight='bold', ha='center')
        
        # Client Layer
        client_box = FancyBboxPatch((1, 7.5), 3, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor=self.colors['mobile'], 
                                   edgecolor='black', linewidth=2)
        ax.add_patch(client_box)
        ax.text(2.5, 8.25, 'Mobile Client\n(SSL/TLS)', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        # Security Gateway
        gateway_box = FancyBboxPatch((5.5, 7.5), 3, 1.5, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor=self.colors['security'], 
                                    edgecolor='black', linewidth=2)
        ax.add_patch(gateway_box)
        ax.text(7, 8.25, 'Security Gateway\n(Rate Limiting)', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        # Authentication Server
        auth_box = FancyBboxPatch((10, 7.5), 3, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='darkred', 
                                 edgecolor='black', linewidth=2)
        ax.add_patch(auth_box)
        ax.text(11.5, 8.25, 'JWT Auth Server\n(Token Validation)', 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        # Security Layers
        security_layers = [
            ('Input Validation\n& Sanitization', 2, 6),
            ('CORS Policy\nEnforcement', 5, 6),
            ('Authorization\nMiddleware', 8, 6),
            ('Audit Logging\n& Monitoring', 11, 6)
        ]
        
        for layer, x, y in security_layers:
            layer_box = FancyBboxPatch((x-1, y-0.5), 2, 1, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor=self.colors['accent'], 
                                      edgecolor='black', linewidth=1)
            ax.add_patch(layer_box)
            ax.text(x, y, layer, ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Data Protection
        protection_layers = [
            ('Password Hashing\n(Bcrypt)', 2, 4),
            ('Data Encryption\n(AES-256)', 5, 4),
            ('Secure Storage\n(Encrypted DB)', 8, 4),
            ('Backup Security\n(Encrypted)', 11, 4)
        ]
        
        for layer, x, y in protection_layers:
            layer_box = FancyBboxPatch((x-1, y-0.5), 2, 1, 
                                      boxstyle="round,pad=0.05", 
                                      facecolor='darkgreen', 
                                      edgecolor='black', linewidth=1)
            ax.add_patch(layer_box)
            ax.text(x, y, layer, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Compliance & Monitoring
        compliance_box = FancyBboxPatch((2, 2), 9, 1, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='purple', 
                                       edgecolor='black', linewidth=2)
        ax.add_patch(compliance_box)
        ax.text(6.5, 2.5, 'Compliance & Monitoring (GDPR, SOC2, Activity Logs)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Security flow arrows
        security_arrows = [
            ((4, 8.25), (5.5, 8.25)),
            ((8.5, 8.25), (10, 8.25)),
            ((2, 7.5), (2, 6.5)),
            ((7, 7.5), (7, 6.5)),
            ((11.5, 7.5), (11.5, 6.5)),
            ((6.5, 5.5), (6.5, 4.5)),
            ((6.5, 3.5), (6.5, 3))
        ]
        
        for start, end in security_arrows:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=20, fc="red")
            ax.add_patch(arrow)
        
        plt.tight_layout()
        plt.savefig('diagrams/security_architecture.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_data_flow_diagram(self):
        """Create data flow diagram using networkx"""
        G = nx.DiGraph()
        
        # Add nodes
        nodes = {
            'Mobile App': {'pos': (0, 2), 'color': self.colors['mobile']},
            'API Gateway': {'pos': (2, 2), 'color': self.colors['api']},
            'Auth Service': {'pos': (4, 3), 'color': self.colors['security']},
            'Attendance Service': {'pos': (4, 2), 'color': self.colors['accent']},
            'Employee Service': {'pos': (4, 1), 'color': self.colors['secondary']},
            'Database': {'pos': (6, 2), 'color': self.colors['database']},
            'Redis Cache': {'pos': (6, 3), 'color': '#DC382D'},
            'External APIs': {'pos': (6, 1), 'color': 'gray'},
            'Push Notifications': {'pos': (2, 0), 'color': 'orange'}
        }
        
        for node, attrs in nodes.items():
            G.add_node(node, **attrs)
        
        # Add edges with labels
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
        
        # Create the plot
        plt.figure(figsize=(16, 12))
        pos = nx.get_node_attributes(G, 'pos')
        colors = [nodes[node]['color'] for node in G.nodes()]
        
        # Draw the network
        nx.draw(G, pos, with_labels=True, node_color=colors, 
                node_size=3000, font_size=10, font_weight='bold',
                arrows=True, arrowsize=20, edge_color='gray',
                arrowstyle='->', connectionstyle='arc3,rad=0.1')
        
        # Add edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
        
        plt.title('Data Flow & Communication Diagram', fontsize=18, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('diagrams/data_flow.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_file_structure_diagram(self):
        """Create project file structure diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 20))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 25)
        ax.axis('off')
        
        # Title
        ax.text(8, 24.5, 'Mobile App Project Structure', 
                fontsize=18, fontweight='bold', ha='center')
        
        # File structure data
        structure = [
            ('📱 AttendanceApp/', 0, 23, 'folder'),
            ('├── 📁 src/', 1, 22, 'folder'),
            ('│   ├── 📁 components/', 2, 21.5, 'folder'),
            ('│   │   ├── 📄 LoginForm.tsx', 3, 21, 'file'),
            ('│   │   ├── 📄 AttendanceCard.tsx', 3, 20.5, 'file'),
            ('│   │   ├── 📄 QRScanner.tsx', 3, 20, 'file'),
            ('│   │   └── 📄 LocationPicker.tsx', 3, 19.5, 'file'),
            ('│   ├── 📁 screens/', 2, 19, 'folder'),
            ('│   │   ├── 📄 LoginScreen.tsx', 3, 18.5, 'file'),
            ('│   │   ├── 📄 DashboardScreen.tsx', 3, 18, 'file'),
            ('│   │   ├── 📄 AttendanceScreen.tsx', 3, 17.5, 'file'),
            ('│   │   ├── 📄 ProfileScreen.tsx', 3, 17, 'file'),
            ('│   │   └── 📄 SettingsScreen.tsx', 3, 16.5, 'file'),
            ('│   ├── 📁 navigation/', 2, 16, 'folder'),
            ('│   │   ├── 📄 AppNavigator.tsx', 3, 15.5, 'file'),
            ('│   │   ├── 📄 AuthNavigator.tsx', 3, 15, 'file'),
            ('│   │   └── 📄 TabNavigator.tsx', 3, 14.5, 'file'),
            ('│   ├── 📁 services/', 2, 14, 'folder'),
            ('│   │   ├── 📄 ApiService.ts', 3, 13.5, 'file'),
            # ... continuing from previous code

            ('│   │   ├── 📄 AuthService.ts', 3, 13, 'file'),
            ('│   │   ├── 📄 AttendanceService.ts', 3, 12.5, 'file'),
            ('│   │   ├── 📄 LocationService.ts', 3, 12, 'file'),
            ('│   │   └── 📄 NotificationService.ts', 3, 11.5, 'file'),
            ('│   ├── 📁 store/', 2, 11, 'folder'),
            ('│   │   ├── 📄 index.ts', 3, 10.5, 'file'),
            ('│   │   ├── 📄 authSlice.ts', 3, 10, 'file'),
            ('│   │   ├── 📄 attendanceSlice.ts', 3, 9.5, 'file'),
            ('│   │   └── 📄 userSlice.ts', 3, 9, 'file'),
            ('│   ├── 📁 utils/', 2, 8.5, 'folder'),
            ('│   │   ├── 📄 constants.ts', 3, 8, 'file'),
            ('│   │   ├── 📄 helpers.ts', 3, 7.5, 'file'),
            ('│   │   ├── 📄 validators.ts', 3, 7, 'file'),
            ('│   │   └── 📄 storage.ts', 3, 6.5, 'file'),
            ('│   ├── 📁 types/', 2, 6, 'folder'),
            ('│   │   ├── 📄 auth.ts', 3, 5.5, 'file'),
            ('│   │   ├── 📄 attendance.ts', 3, 5, 'file'),
            ('│   │   └── 📄 user.ts', 3, 4.5, 'file'),
            ('│   └── 📄 App.tsx', 2, 4, 'file'),
            ('├── 📁 assets/', 1, 3.5, 'folder'),
            ('│   ├── 📁 images/', 2, 3, 'folder'),
            ('│   ├── 📁 icons/', 2, 2.5, 'folder'),
            ('│   └── 📁 fonts/', 2, 2, 'folder'),
            ('├── 📄 package.json', 1, 1.5, 'file'),
            ('├── 📄 tsconfig.json', 1, 1, 'file'),
            ('└── 📄 README.md', 1, 0.5, 'file')
        ]
        
        # Draw file structure
        for item, indent, y, item_type in structure:
            color = self.colors['accent'] if item_type == 'folder' else 'lightblue'
            fontweight = 'bold' if item_type == 'folder' else 'normal'
            
            ax.text(indent, y, item, fontsize=10, fontweight=fontweight, 
                   va='center', color='black')
        
        # Add descriptions on the right side
        descriptions = [
            ('Components: Reusable UI components', 8, 20.5),
            ('Screens: Main application screens', 8, 18),
            ('Navigation: App navigation logic', 8, 15),
            ('Services: API and business logic', 8, 12.5),
            ('Store: State management (Redux)', 8, 10),
            ('Utils: Helper functions and constants', 8, 7.5),
            ('Types: TypeScript type definitions', 8, 5.5),
            ('Assets: Images, icons, and fonts', 8, 2.5)
        ]
        
        for desc, x, y in descriptions:
            desc_box = FancyBboxPatch((x, y-0.2), 6, 0.4, 
                                     boxstyle="round,pad=0.05", 
                                     facecolor='lightyellow', 
                                     edgecolor='gray', linewidth=1)
            ax.add_patch(desc_box)
            ax.text(x+3, y, desc, ha='center', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('diagrams/file_structure.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_user_flow_diagram(self):
        """Create user flow and interaction diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(18, 14))
        ax.set_xlim(0, 18)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Title
        ax.text(9, 13.5, 'User Flow & Interaction Diagram', 
                fontsize=18, fontweight='bold', ha='center')
        
        # User flows
        flows = [
            # Login Flow
            ('Start', 1, 12, 'start'),
            ('Login Screen', 3, 12, 'screen'),
            ('Enter Credentials', 5, 12, 'action'),
            ('Authenticate', 7, 12, 'process'),
            ('Dashboard', 9, 12, 'screen'),
            
            # Attendance Flow
            ('Attendance Screen', 3, 10, 'screen'),
            ('Choose Method', 5, 10, 'decision'),
            ('QR Scan', 7, 11, 'action'),
            ('Location Check', 7, 9, 'action'),
            ('Verify Location', 9, 10, 'process'),
            ('Record Attendance', 11, 10, 'process'),
            ('Success Message', 13, 10, 'result'),
            
            # Leave Request Flow
            ('Leave Screen', 3, 8, 'screen'),
            ('Fill Form', 5, 8, 'action'),
            ('Submit Request', 7, 8, 'process'),
            ('Notification Sent', 9, 8, 'process'),
            ('Approval Status', 11, 8, 'result'),
            
            # Profile Flow
            ('Profile Screen', 3, 6, 'screen'),
            ('Edit Profile', 5, 6, 'action'),
            ('Update Data', 7, 6, 'process'),
            ('Save Changes', 9, 6, 'result'),
            
            # Settings Flow
            ('Settings Screen', 3, 4, 'screen'),
            ('Change Settings', 5, 4, 'action'),
            ('Apply Changes', 7, 4, 'process'),
            ('Confirmation', 9, 4, 'result')
        ]
        
        # Color mapping for different flow types
        flow_colors = {
            'start': 'green',
            'screen': self.colors['mobile'],
            'action': self.colors['accent'],
            'decision': 'orange',
            'process': self.colors['secondary'],
            'result': 'lightgreen'
        }
        
        # Draw flow elements
        for name, x, y, flow_type in flows:
            color = flow_colors.get(flow_type, 'gray')
            
            if flow_type == 'decision':
                # Diamond shape for decisions
                diamond = patches.RegularPolygon((x, y), 4, radius=0.5, 
                                               orientation=np.pi/4,
                                               facecolor=color, edgecolor='black')
                ax.add_patch(diamond)
            elif flow_type == 'start':
                # Circle for start
                circle = patches.Circle((x, y), 0.3, facecolor=color, edgecolor='black')
                ax.add_patch(circle)
            else:
                # Rectangle for other elements
                rect = FancyBboxPatch((x-0.7, y-0.3), 1.4, 0.6, 
                                     boxstyle="round,pad=0.05", 
                                     facecolor=color, edgecolor='black')
                ax.add_patch(rect)
            
            ax.text(x, y, name, ha='center', va='center', fontsize=8, 
                   fontweight='bold', color='white' if flow_type != 'result' else 'black')
        
        # Add flow arrows
        flow_arrows = [
            # Login flow
            ((1.3, 12), (2.7, 12)),
            ((3.7, 12), (4.3, 12)),
            ((5.7, 12), (6.3, 12)),
            ((7.7, 12), (8.3, 12)),
            
            # Attendance flow
            ((3, 11.7), (3, 10.3)),
            ((3.7, 10), (4.3, 10)),
            ((5.5, 10.3), (6.5, 10.7)),
            ((5.5, 9.7), (6.5, 9.3)),
            ((7.7, 10), (8.3, 10)),
            ((9.7, 10), (10.3, 10)),
            ((11.7, 10), (12.3, 10)),
            
            # Leave flow
            ((3, 9.7), (3, 8.3)),
            ((3.7, 8), (4.3, 8)),
            ((5.7, 8), (6.3, 8)),
            ((7.7, 8), (8.3, 8)),
            ((9.7, 8), (10.3, 8)),
            
            # Profile flow
            ((3, 7.7), (3, 6.3)),
            ((3.7, 6), (4.3, 6)),
            ((5.7, 6), (6.3, 6)),
            ((7.7, 6), (8.3, 6)),
            
            # Settings flow
            ((3, 5.7), (3, 4.3)),
            ((3.7, 4), (4.3, 4)),
            ((5.7, 4), (6.3, 4)),
            ((7.7, 4), (8.3, 4))
        ]
        
        for start, end in flow_arrows:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=15, fc="black")
            ax.add_patch(arrow)
        
        # Add legend
        legend_elements = [
            ('Start/End', 'green'),
            ('Screen', self.colors['mobile']),
            ('User Action', self.colors['accent']),
            ('Decision', 'orange'),
            ('Process', self.colors['secondary']),
            ('Result', 'lightgreen')
        ]
        
        for i, (label, color) in enumerate(legend_elements):
            legend_box = FancyBboxPatch((15, 12-i*0.5), 1, 0.3, 
                                       boxstyle="round,pad=0.02", 
                                       facecolor=color, edgecolor='black')
            ax.add_patch(legend_box)
            ax.text(16.2, 12.15-i*0.5, label, va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('diagrams/user_flow.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_deployment_diagram(self):
        """Create deployment architecture diagram"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Title
        ax.text(8, 11.5, 'Deployment Architecture', 
                fontsize=18, fontweight='bold', ha='center')
        
        # Cloud Infrastructure
        cloud_box = FancyBboxPatch((1, 8), 14, 2.5, 
                                  boxstyle="round,pad=0.2", 
                                  facecolor='lightblue', 
                                  edgecolor='blue', linewidth=2, alpha=0.3)
        ax.add_patch(cloud_box)
        ax.text(8, 10.2, 'Cloud Infrastructure (AWS/Azure/GCP)', 
                ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Load Balancer
        lb_box = FancyBboxPatch((2, 8.5), 2, 1, 
                               boxstyle="round,pad=0.1", 
                               facecolor='orange', 
                               edgecolor='black', linewidth=1)
        ax.add_patch(lb_box)
        ax.text(3, 9, 'Load\nBalancer', ha='center', va='center', 
               fontsize=10, fontweight='bold')
        
        # API Servers
        api_servers = [
            ('API Server 1', 6, 9),
            ('API Server 2', 8, 9),
            ('API Server 3', 10, 9)
        ]
        
        for server, x, y in api_servers:
            server_box = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8, 
                                       boxstyle="round,pad=0.05", 
                                       facecolor=self.colors['api'], 
                                       edgecolor='black', linewidth=1)
            ax.add_patch(server_box)
            ax.text(x, y, server, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # Database Cluster
        db_box = FancyBboxPatch((12, 8.5), 2.5, 1, 
                               boxstyle="round,pad=0.1", 
                               facecolor=self.colors['database'], 
                               edgecolor='black', linewidth=1)
        ax.add_patch(db_box)
        ax.text(13.25, 9, 'Database\nCluster', ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white')
        
        # Services Layer
        services = [
            ('Redis Cache', 2, 6.5),
            ('File Storage', 4.5, 6.5),
            ('Email Service', 7, 6.5),
            ('Push Notifications', 9.5, 6.5),
            ('Monitoring', 12, 6.5)
        ]
        
        for service, x, y in services:
            service_box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, 
                                        boxstyle="round,pad=0.05", 
                                        facecolor=self.colors['secondary'], 
                                        edgecolor='black', linewidth=1)
            ax.add_patch(service_box)
            ax.text(x, y, service, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # ... continuing from previous code

        # Mobile Clients
        mobile_clients = [
            ('iOS App', 3, 4.5),
            ('Android App', 6, 4.5),
            ('Web App', 9, 4.5)
        ]
        
        for client, x, y in mobile_clients:
            client_box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, 
                                       boxstyle="round,pad=0.05", 
                                       facecolor=self.colors['mobile'], 
                                       edgecolor='black', linewidth=1)
            ax.add_patch(client_box)
            ax.text(x, y, client, ha='center', va='center', fontsize=9, 
                   fontweight='bold', color='white')
        
        # CDN
        cdn_box = FancyBboxPatch((12, 4.5), 2, 0.8, 
                                boxstyle="round,pad=0.05", 
                                facecolor='purple', 
                                edgecolor='black', linewidth=1)
        ax.add_patch(cdn_box)
        ax.text(13, 4.9, 'CDN', ha='center', va='center', fontsize=10, 
               fontweight='bold', color='white')
        
        # Security Layer
        security_box = FancyBboxPatch((2, 2.5), 10, 1, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor=self.colors['security'], 
                                     edgecolor='black', linewidth=2)
        ax.add_patch(security_box)
        ax.text(7, 3, 'Security Layer (WAF, DDoS Protection, SSL/TLS)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Monitoring & Analytics
        monitoring_box = FancyBboxPatch((2, 1), 10, 1, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='darkgreen', 
                                       edgecolor='black', linewidth=2)
        ax.add_patch(monitoring_box)
        ax.text(7, 1.5, 'Monitoring & Analytics (Logs, Metrics, Alerts)', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Add deployment arrows
        deployment_arrows = [
            # Load balancer to API servers
            ((4, 9), (5.3, 9)),
            ((4, 9), (7.3, 9)),
            ((4, 9), (9.3, 9)),
            # API servers to database
            ((8, 8.6), (12, 8.8)),
            # Mobile clients to load balancer
            ((3, 5.3), (3, 8.1)),
            ((6, 5.3), (3.5, 8.2)),
            ((9, 5.3), (3.8, 8.3)),
            # Services connections
            ((8, 8.6), (8, 7.3))
        ]
        
        for start, end in deployment_arrows:
            arrow = ConnectionPatch(start, end, "data", "data",
                                  arrowstyle="->", shrinkA=5, shrinkB=5,
                                  mutation_scale=15, fc="black")
            ax.add_patch(arrow)
        
        plt.tight_layout()
        plt.savefig('diagrams/deployment_architecture.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_performance_metrics_dashboard(self):
        """Create performance metrics visualization"""
        # Create sample performance data
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        
        # Sample metrics data
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
                      line=dict(color=self.colors['primary'])),
            row=1, col=1
        )
        
        # Database Performance
        fig.add_trace(
            go.Scatter(x=dates, y=database_query_times, 
                      mode='lines+markers', name='Query Time (ms)',
                      line=dict(color=self.colors['database'])),
            row=1, col=2
        )
        
        # Active Users
        fig.add_trace(
            go.Bar(x=dates, y=active_users, name='Active Users',
                   marker_color=self.colors['success']),
            row=2, col=1
        )
        
        # Error Rates
        fig.add_trace(
            go.Scatter(x=dates, y=error_rates, 
                      mode='lines+markers', name='Error Rate (%)',
                      line=dict(color=self.colors['secondary'])),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Performance Metrics Dashboard",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        fig.write_html('diagrams/performance_dashboard.html')
        fig.show()
    
    def create_interactive_api_documentation(self):
        """Create interactive API documentation diagram"""
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
        
        # Add nodes for each API category
        categories = list(endpoints_data.keys())
        colors_list = [self.colors['primary'], self.colors['secondary'], 
                      self.colors['accent'], self.colors['success']]
        
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
            hovermode='closest'
        )
        
        fig.write_html('diagrams/api_documentation.html')
        fig.show()

def main():
    """Generate all architecture diagrams"""
    generator = AttendanceAppArchitectureDiagrams()
    
    print("Generating Architecture Diagrams...")
    
    # Create diagrams directory
    import os
    os.makedirs('diagrams', exist_ok=True)
    
    # Generate all diagrams
    print("1. Creating System Overview...")
    generator.create_system_overview()
    
    print("2. Creating Mobile App Structure...")
    generator.create_mobile_app_structure()
    
    print("3. Creating API Endpoints Diagram...")
    generator.create_api_endpoints_diagram()
    
    print("4. Creating Security Architecture...")
    generator.create_security_architecture()
    
    print("5. Creating Data Flow Diagram...")
    generator.create_data_flow_diagram()
    
    print("6. Creating File Structure Diagram...")
    generator.create_file_structure_diagram()
    
    print("7. Creating User Flow Diagram...")
    generator.create_user_flow_diagram()
    
    print("8. Creating Deployment Diagram...")
    generator.create_deployment_diagram()
    
    print("9. Creating Performance Dashboard...")
    generator.create_performance_metrics_dashboard()
    
    print("10. Creating Interactive API Documentation...")
    generator.create_interactive_api_documentation()
    
    print("All diagrams generated successfully!")

if __name__ == "__main__":
    main()
