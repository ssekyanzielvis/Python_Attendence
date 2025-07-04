import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import os

class MobileAppWireframes:
    def __init__(self):
        self.phone_width = 4
        self.phone_height = 7
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'background': '#F5F5F5',
            'text': '#333333'
        }
    
    def create_phone_frame(self, ax, x_offset=0, y_offset=0):
        """Create basic phone frame and return content area coordinates"""
        # Phone outline
        phone_frame = FancyBboxPatch(
            (x_offset + 0.5, y_offset + 0.5), self.phone_width, self.phone_height,
            boxstyle="round,pad=0.1",
            facecolor='white',
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(phone_frame)
        
        # Screen area
        content_x = x_offset + 0.7
        content_y = y_offset + 0.7
        content_w = self.phone_width - 0.4
        content_h = self.phone_height - 0.4
        
        screen = FancyBboxPatch(
            (content_x, content_y), content_w, content_h,
            boxstyle="round,pad=0.05",
            facecolor=self.colors['background'],
            edgecolor='gray'
        )
        ax.add_patch(screen)
        
        return content_x, content_y, content_w, content_h
    
    def create_login_screen(self, ax, x_offset=0, y_offset=0):
        """Create login screen wireframe"""
        content_x, content_y, content_w, content_h = self.create_phone_frame(ax, x_offset, y_offset)
        
        # App logo/title
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 1,
                'AttendanceApp', ha='center', fontsize=14, fontweight='bold',
                color=self.colors['primary'])
        
        # Login form
        # Username field
        username_field = FancyBboxPatch(
            (content_x + 0.2, content_y + content_h - 2.5), content_w - 0.4, 0.4,
            boxstyle="round,pad=0.05",
            facecolor='white',
            edgecolor='gray'
        )
        ax.add_patch(username_field)
        ax.text(content_x + 0.3, content_y + content_h - 2.3,
                'Username', fontsize=9, color='gray')
        
        # Password field
        password_field = FancyBboxPatch(
            (content_x + 0.2, content_y + content_h - 3.2), content_w - 0.4, 0.4,
            boxstyle="round,pad=0.05",
            facecolor='white',
            edgecolor='gray'
        )
        ax.add_patch(password_field)
        ax.text(content_x + 0.3, content_y + content_h - 3,
                'Password', fontsize=9, color='gray')
        
        # Login button
        login_btn = FancyBboxPatch(
            (content_x + 0.2, content_y + content_h - 4), content_w - 0.4, 0.5,
            boxstyle="round,pad=0.05",
            facecolor=self.colors['primary'],
            edgecolor='none'
        )
        ax.add_patch(login_btn)
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 3.75,
                'LOGIN', ha='center', va='center', fontsize=10,
                color='white', fontweight='bold')
        
        # Forgot password link
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 4.5,
                'Forgot Password?', ha='center', fontsize=8,
                color=self.colors['primary'], style='italic')
        
        # Biometric login option
        biometric_btn = patches.Circle((x_offset + self.phone_width/2, content_y + 1.5),
                                      0.3, facecolor=self.colors['accent'], alpha=0.8)
        ax.add_patch(biometric_btn)
        ax.text(x_offset + self.phone_width/2, content_y + 1.5,
                '👆', ha='center', va='center', fontsize=16)
        ax.text(x_offset + self.phone_width/2, content_y + 1,
                'Touch ID / Face ID', ha='center', fontsize=8)
    
    def create_dashboard_screen(self, ax, x_offset=0, y_offset=0):
        """Create dashboard screen wireframe"""
        content_x, content_y, content_w, content_h = self.create_phone_frame(ax, x_offset, y_offset)
        
        # Header
        header = FancyBboxPatch(
            (content_x, content_y + content_h - 0.8), content_w, 0.6,
            boxstyle="square,pad=0",
            facecolor=self.colors['primary'],
            edgecolor='none'
        )
        ax.add_patch(header)
        ax.text(content_x + 0.2, content_y + content_h - 0.5,
                'Dashboard', fontsize=11, color='white', fontweight='bold')
        ax.text(content_x + content_w - 0.2, content_y + content_h - 0.5,
                '☰', ha='right', fontsize=14, color='white')
        
        # Welcome message
        ax.text(content_x + 0.2, content_y + content_h - 1.2,
                'Welcome, John Doe', fontsize=10, fontweight='bold')
        ax.text(content_x + 0.2, content_y + content_h - 1.5,
                'Today: March 15, 2024', fontsize=8, color='gray')
        
        # Quick actions grid
        actions = [
            ('Check In', '📍', 0.5, 2.5),
            ('Check Out', '🚪', 2.2, 2.5),
            ('Leave Request', '📝', 0.5, 1.5),
            ('My Profile', '👤', 2.2, 1.5)
        ]
        
        for action, icon, rel_x, rel_y in actions:
            action_btn = FancyBboxPatch(
                (content_x + rel_x, content_y + content_h - rel_y - 0.6), 1.2, 0.8,
                boxstyle="round,pad=0.05",
                facecolor='white',
                edgecolor=self.colors['primary'],
                linewidth=1
            )
            ax.add_patch(action_btn)
            ax.text(content_x + rel_x + 0.6, content_y + content_h - rel_y - 0.3,
                    icon, ha='center', fontsize=16)
            ax.text(content_x + rel_x + 0.6, content_y + content_h - rel_y - 0.5,
                    action, ha='center', fontsize=8, fontweight='bold')
        
        # Today's status
        status_box = FancyBboxPatch(
            (content_x + 0.2, content_y + 0.5), content_w - 0.4, 1.2,
            boxstyle="round,pad=0.1",
            facecolor=self.colors['background'],
            edgecolor='gray'
        )
        ax.add_patch(status_box)
        ax.text(content_x + 0.3, content_y + 1.5,
                "Today's Status", fontsize=9, fontweight='bold')
        ax.text(content_x + 0.3, content_y + 1.2,
                'Check-in: 9:00 AM', fontsize=8)
        ax.text(content_x + 0.3, content_y + 1.0,
                'Hours worked: 6h 30m', fontsize=8)
        ax.text(content_x + 0.3, content_y + 0.8,
                'Status: Working', fontsize=8, color='green')
    
    def create_attendance_screen(self, ax, x_offset=0, y_offset=0):
        """Create attendance screen wireframe"""
        content_x, content_y, content_w, content_h = self.create_phone_frame(ax, x_offset, y_offset)
        
        # Header
        header = FancyBboxPatch(
            (content_x, content_y + content_h - 0.8), content_w, 0.6,
            boxstyle="square,pad=0",
            facecolor=self.colors['primary'],
            edgecolor='none'
        )
        ax.add_patch(header)
        ax.text(content_x + 0.2, content_y + content_h - 0.5,
                '← Attendance', fontsize=11, color='white', fontweight='bold')
        
        # Current time
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 1.3,
                '2:30 PM', ha='center', fontsize=16, fontweight='bold')
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 1.6,
                'March 15, 2024', ha='center', fontsize=10, color='gray')
        
        # Check-in/out buttons
        checkin_btn = FancyBboxPatch(
            (content_x + 0.2, content_y + content_h - 2.8), (content_w - 0.5)/2, 0.8,
            boxstyle="round,pad=0.05",
            facecolor='green',
            edgecolor='none'
        )
        ax.add_patch(checkin_btn)
        ax.text(content_x + 0.2 + (content_w - 0.5)/4, content_y + content_h - 2.4,
                'CHECK IN', ha='center', va='center', fontsize=9,
                color='white', fontweight='bold')
        
        checkout_btn = FancyBboxPatch(
            (content_x + 0.3 + (content_w - 0.5)/2, content_y + content_h - 2.8),
            (content_w - 0.5)/2, 0.8,
            boxstyle="round,pad=0.05",
            facecolor='red',
            edgecolor='none'
        )
        ax.add_patch(checkout_btn)
        ax.text(content_x + 0.3 + (content_w - 0.5)/2 + (content_w - 0.5)/4,
                content_y + content_h - 2.4,
                'CHECK OUT', ha='center', va='center', fontsize=9,
                color='white', fontweight='bold')
        
        # QR Code scanner
        qr_box = FancyBboxPatch(
            (content_x + 0.5, content_y + content_h - 4), content_w - 1, 0.8,
            boxstyle="round,pad=0.05",
            facecolor=self.colors['accent'],
            edgecolor='none'
        )
        ax.add_patch(qr_box)
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 3.6,
                '📱 Scan QR Code', ha='center', va='center', fontsize=10,
                color='white', fontweight='bold')
        
        # Location info
        location_box = FancyBboxPatch(
            (content_x + 0.2, content_y + 0.5), content_w - 0.4, 1,
            boxstyle="round,pad=0.1",
            facecolor='lightblue',
            edgecolor='blue',
            alpha=0.7
        )
        ax.add_patch(location_box)
        ax.text(content_x + 0.3, content_y + 1.2,
                '📍 Current Location', fontsize=9, fontweight='bold')
        ax.text(content_x + 0.3, content_y + 0.9,
                'Office Building A', fontsize=8)
        ax.text(content_x + 0.3, content_y + 0.7,
                'Within work area ✓', fontsize=8, color='green')
    
    def create_profile_screen(self, ax, x_offset=0, y_offset=0):
        """Create profile screen wireframe"""
        content_x, content_y, content_w, content_h = self.create_phone_frame(ax, x_offset, y_offset)
        
        # Header
        header = FancyBboxPatch(
            (content_x, content_y + content_h - 0.8), content_w, 0.6,
            boxstyle="square,pad=0",
            facecolor=self.colors['primary'],
            edgecolor='none'
        )
        ax.add_patch(header)
        ax.text(content_x + 0.2, content_y + content_h - 0.5,
                '← Profile', fontsize=11, color='white', fontweight='bold')
        
        # Profile picture
        profile_pic = patches.Circle((x_offset + self.phone_width/2, content_y + content_h - 1.5),
                                    0.4, facecolor='lightgray', edgecolor='gray')
        ax.add_patch(profile_pic)
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 1.5,
                '👤', ha='center', va='center', fontsize=20)
        
        # User info
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 2.1,
                'John Doe', ha='center', fontsize=12, fontweight='bold')
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 2.4,
                'Software Developer', ha='center', fontsize=10, color='gray')
        ax.text(x_offset + self.phone_width/2, content_y + content_h - 2.7,
                'ID: EMP001', ha='center', fontsize=9, color='gray')
        
               # Profile details (continuing from where it stopped)
        details = [
            ('📧 Email', 'john.doe@company.com'),
            ('📱 Phone', '+1 (555) 123-4567'),
            ('🏢 Department', 'Engineering'),
            ('📅 Join Date', 'January 15, 2023'),
            ('⏰ Work Hours', '9:00 AM - 6:00 PM')
        ]
        
        for i, (label, value) in enumerate(details):
            y_pos = content_y + content_h - 3.2 - (i * 0.4)
            ax.text(content_x + 0.2, y_pos, label, fontsize=8, fontweight='bold')
            ax.text(content_x + 0.2, y_pos - 0.15, value, fontsize=8, color='gray')
        
        # Edit button
        edit_btn = FancyBboxPatch(
            (content_x + 0.2, content_y + 0.3), content_w - 0.4, 0.4,
            boxstyle="round,pad=0.05",
            facecolor=self.colors['accent'],
            edgecolor='none'
        )
        ax.add_patch(edit_btn)
        ax.text(x_offset + self.phone_width/2, content_y + 0.5,
                'Edit Profile', ha='center', va='center', fontsize=9,
                color='white', fontweight='bold')
    
    def create_all_wireframes(self):
        """Create all wireframes in a single figure"""
        # Create diagrams directory if it doesn't exist
        os.makedirs('diagrams', exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 20))
        fig.suptitle('Mobile App Wireframes - Employee Attendance System',
                     fontsize=16, fontweight='bold', y=0.95)
        
        # Flatten axes for easier indexing
        axes = axes.flatten()
        
        # Set up each subplot
        for ax in axes:
            ax.set_xlim(0, 5)
            ax.set_ylim(0, 8)
            ax.set_aspect('equal')
            ax.axis('off')
        
        # Create wireframes
        self.create_login_screen(axes[0])
        axes[0].set_title('Login Screen', fontsize=12, fontweight='bold', pad=20)
        
        self.create_dashboard_screen(axes[1])
        axes[1].set_title('Dashboard Screen', fontsize=12, fontweight='bold', pad=20)
        
        self.create_attendance_screen(axes[2])
        axes[2].set_title('Attendance Screen', fontsize=12, fontweight='bold', pad=20)
        
        self.create_profile_screen(axes[3])
        axes[3].set_title('Profile Screen', fontsize=12, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('diagrams/mobile_wireframes.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    wireframes = MobileAppWireframes()
    wireframes.create_all_wireframes()

if __name__ == "__main__":
    main()
