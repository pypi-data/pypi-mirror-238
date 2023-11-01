from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections

from isapilib.exceptions import SepaException


def add_conn(username, gwmbac):
    try:
        user_model_path = getattr(settings, 'AUTH_USER_MODEL', 'isapilib.UserAPI')
        branch_model_path = getattr(settings, 'BRANCH_MODEL', 'isapilib.SepaBranch')
        permission_model_path = getattr(settings, 'PERMISSION_MODEL', 'isapilib.SepaBranchUsers')

        user_model = apps.get_model(user_model_path, require_ready=False)
        branch_model = apps.get_model(branch_model_path, require_ready=False)
        permission_model = apps.get_model(permission_model_path, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError as e:
        if settings.AUTH_USER_MODEL in str(e):
            raise ImproperlyConfigured(
                f"AUTH_USER_MODEL refers to model '{settings.AUTH_USER_MODEL}' that has not been installed"
            )
        elif settings.BRANCH_MODEL in str(e):
            raise ImproperlyConfigured(
                f"BRANCH_MODEL refers to model '{settings.BRANCH_MODEL}' that has not been installed"
            )
        elif settings.PERMISSION_MODEL in str(e):
            raise ImproperlyConfigured(
                f"PERMISSION_MODEL refers to model '{settings.PERMISSION_MODEL}' that has not been installed"
            )
        else:
            raise e

    try:
        user = user_model.objects.get(usuario=username)
        branch = branch_model.objects.get(gwmbac=gwmbac)
        permission_model.objects.get(iduser_id=user.id, idbranch_id=branch.id)

        conn = f'external-{branch.id}'
        if conn not in connections.databases:
            connections.databases[conn] = {
                'ENGINE': 'mssql',
                'NAME': branch.conf_db if branch.conf_db else '',
                'USER': branch.conf_user if branch.conf_user else '',
                'PASSWORD': branch.conf_pass if branch.conf_pass else '',
                'HOST': branch.conf_ip_ext if branch.conf_ip_ext else '',
                'PORT': branch.conf_port if branch.conf_port else '',
                'TIME_ZONE': None,
                'CONN_HEALTH_CHECKS': None,
                'CONN_MAX_AGE': None,
                'ATOMIC_REQUESTS': None,
                'AUTOCOMMIT': True,
                'OPTIONS': {
                    'driver': 'ODBC Driver 17 for SQL Server',
                }
            }
        return conn
    except user_model.DoesNotExist:
        raise SepaException('The user does not exist')
    except branch_model.DoesNotExist:
        raise SepaException('The agency does not exist')
    except permission_model.DoesNotExist:
        raise SepaException('You do not have permissions on the agency')
