import click
from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..services.auth_service import AuthService
from ..repositories.employee_repository import EmployeeRepository
from ..models.employee import EmployeeRole

@click.group()
def cli():
    """Employee Attendance System CLI"""
    pass

@cli.command()
@click.option('--employee-code', prompt=True, help='Employee code')
@click.option('--email', prompt=True, help='Email address')
@click.option('--first-name', prompt=True, help='First name')
@click.option('--last-name', prompt=True, help='Last name')
@click.option('--password', prompt=True, hide_input=True, help='Password')
@click.option('--department', default='IT', help='Department')
@click.option('--position', default='Administrator', help='Position')
def create_admin(employee_code, email, first_name, last_name, password, department, position):
    """Create an admin user"""
    db: Session = SessionLocal()
    
    try:
        employee_repo = EmployeeRepository(db)
        auth_service = AuthService(db)
        
        # Check if employee already exists
        if employee_repo.get_by_email(email):
            click.echo(f"Error: Employee with email {email} already exists")
            return
        
        if employee_repo.get_by_employee_code(employee_code):
            click.echo(f"Error: Employee with code {employee_code} already exists")
            return
        
        # Create admin user
        password_hash = auth_service.get_password_hash(password)
        
        employee_data = {
            'employee_code': employee_code,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'department': department,
            'position': position,
            'role': EmployeeRole.ADMIN,
            'password_hash': password_hash,
            'is_active': True
        }
        
        employee = employee_repo.create(employee_data)
        click.echo(f"Admin user created successfully: {employee.full_name} ({employee.email})")
        
    except Exception as e:
        click.echo(f"Error creating admin user: {str(e)}")
    finally:
        db.close()

@cli.command()
@click.option('--email', prompt=True, help='Employee email')
def reset_password(email):
    """Reset employee password"""
    db: Session = SessionLocal()
    
    try:
        employee_repo = EmployeeRepository(db)
        auth_service = AuthService(db)
        
        employee = employee_repo.get_by_email(email)
        if not employee:
            click.echo(f"Error: Employee with email {email} not found")
            return
        
        new_password = click.prompt("Enter new password", hide_input=True)
        confirm_password = click.prompt("Confirm new password", hide_input=True)
        
        if new_password != confirm_password:
            click.echo("Error: Passwords do not match")
            return
        
        password_hash = auth_service.get_password_hash(new_password)
        employee_repo.update(str(employee.id), {'password_hash': password_hash})
        
        click.echo(f"Password reset successfully for {employee.full_name}")
        
    except Exception as e:
        click.echo(f"Error resetting password: {str(e)}")
    finally:
        db.close()

@cli.command()
def list_employees():
    """List all employees"""
    db: Session = SessionLocal()
    
    try:
        employee_repo = EmployeeRepository(db)
        employees = employee_repo.get_all()
        
        if not employees:
            click.echo("No employees found")
            return
        
        click.echo("\nEmployees:")
        click.echo("-" * 80)
        click.echo(f"{'Code':<10} {'Name':<25} {'Email':<30} {'Role':<10} {'Active'}")
        click.echo("-" * 80)
        
        for emp in employees:
            click.echo(f"{emp.employee_code:<10} {emp.full_name:<25} {emp.email:<30} {emp.role.value:<10} {'Yes' if emp.is_active else 'No'}")
        
    except Exception as e:
        click.echo(f"Error listing employees: {str(e)}")
    finally:
        db.close()

@cli.command()
@click.option('--employee-code', prompt=True, help='Employee code to deactivate')
def deactivate_employee(employee_code):
    """Deactivate an employee"""
    db: Session = SessionLocal()
    
    try:
        employee_repo = EmployeeRepository(db)
        employee = employee_repo.get_by_employee_code(employee_code)
        
        if not employee:
            click.echo(f"Error: Employee with code {employee_code} not found")
            return
        
        if not employee.is_active:
            click.echo(f"Employee {employee.full_name} is already inactive")
            return
        
        if click.confirm(f"Are you sure you want to deactivate {employee.full_name}?"):
            employee_repo.update(str(employee.id), {'is_active': False})
            click.echo(f"Employee {employee.full_name} deactivated successfully")
        
    except Exception as e:
        click.echo(f"Error deactivating employee: {str(e)}")
    finally:
        db.close()

if __name__ == '__main__':
    cli()
