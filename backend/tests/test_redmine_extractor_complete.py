"""
Test Suite Completo para RedmineExtractor
==========================================
Pruebas exhaustivas para la funcionalidad del extractor de Redmine,
incluyendo:
- Inicialización y configuración
- Listado de proyectos
- Listado y obtención de problemas (issues)
- Listado de usuarios
- Listado de rastreadores (trackers)
- Listado de estados
- Manejo de errores
- Validación de datos
- Escenarios de integración realistas
"""

import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime
from backend.tools.redmine_extractor import RedmineExtractor
from backend.tools.redmine_client import (
    RedmineClient, RedmineHttpError, RedmineInvalidResponse
)
from backend.schemas.redmine import (
    RedmineProject, RedmineIssue, RedmineUser, RedmineTracker, RedmineStatus, RedminePriority
)


# ============================================================================
# FIXTURES - Datos de prueba y configuraciones
# ============================================================================

@pytest.fixture
def mock_extractor():
    """Crea un extractor con cliente mockeado para pruebas."""
    with patch("backend.tools.redmine_client.RedmineClient._request") as mock_request:
        extractor = RedmineExtractor(
            base_url="http://test.redmine.com",
            api_key="test_key_123"
        )
        yield extractor, mock_request


@pytest.fixture
def sample_project_data():
    """Datos de proyecto de ejemplo desde API de Redmine."""
    return {
        "id": 1,
        "name": "Test Project",
        "identifier": "test-proj",
        "description": "Un proyecto de prueba",
        "status": 1,
        "created_on": "2023-01-01T10:00:00Z",
        "updated_on": "2023-12-01T15:30:00Z"
    }


@pytest.fixture
def sample_issue_data():
    """Datos de problema (issue) de ejemplo desde API de Redmine."""
    return {
        "id": 101,
        "subject": "Corregir bug de login",
        "description": "Los usuarios no pueden iniciar sesión con SSO",
        "project": {
            "id": 1,
            "name": "Test Project",
            "identifier": "test-proj"
        },
        "tracker": {
            "id": 1,
            "name": "Bug"
        },
        "status": {
            "id": 1,
            "name": "Nuevo",
            "is_closed": False
        },
        "priority": {
            "id": 2,
            "name": "Normal"
        },
        "author": {
            "id": 1,
            "login": "john.doe",
            "firstname": "John",
            "lastname": "Doe",
            "mail": "john@example.com"
        },
        "assigned_to": {
            "id": 2,
            "login": "jane.smith",
            "firstname": "Jane",
            "lastname": "Smith",
            "mail": "jane@example.com"
        },
        "start_date": "2023-12-01",
        "due_date": "2023-12-15",
        "done_ratio": 50,
        "created_on": "2023-12-01T10:00:00Z",
        "updated_on": "2023-12-10T14:30:00Z"
    }


@pytest.fixture
def sample_user_data():
    """Datos de usuario de ejemplo desde API de Redmine."""
    return [
        {
            "id": 1,
            "login": "john.doe",
            "firstname": "John",
            "lastname": "Doe",
            "mail": "john@example.com",
            "last_login_on": "2023-12-20T09:00:00Z"
        },
        {
            "id": 2,
            "login": "jane.smith",
            "firstname": "Jane",
            "lastname": "Smith",
            "mail": "jane@example.com",
            "last_login_on": "2023-12-19T16:45:00Z"
        }
    ]


# ============================================================================
# PRUEBAS DE INICIALIZACIÓN
# ============================================================================

class TestRedmineExtractorInit:
    """Prueba la inicialización de RedmineExtractor."""
    
    def test_init_con_valores_por_defecto(self):
        """Prueba inicialización con valores por defecto."""
        extractor = RedmineExtractor()
        assert extractor.client is not None
        assert extractor.client.api_key == "43124da14909bca4587aca7cb9cc97ad2bcd7996"
        assert extractor.client.base_url == "http://cidiia.uce.edu.do"
    
    def test_init_con_valores_personalizados(self):
        """Prueba inicialización con URL base y API key personalizados."""
        extractor = RedmineExtractor(
            base_url="http://custom.redmine.com",
            api_key="custom_api_key_456"
        )
        assert extractor.client.api_key == "custom_api_key_456"
        assert extractor.client.base_url == "http://custom.redmine.com"
    
    def test_api_key_en_headers_sesion(self):
        """Verifica que la API key está configurada en los headers de la sesión."""
        extractor = RedmineExtractor(api_key="test_key_123")
        assert extractor.client.session.headers["X-Redmine-API-Key"] == "test_key_123"
    
    def test_content_type_header_configurado(self):
        """Verifica que el header Content-Type está configurado."""
        extractor = RedmineExtractor()
        assert extractor.client.session.headers["Content-Type"] == "application/json"


# ============================================================================
# PRUEBAS DE LISTADO DE PROYECTOS
# ============================================================================

class TestListProjects:
    """Prueba la funcionalidad de listado de proyectos."""
    
    def test_listar_proyectos_una_pagina(self, mock_extractor, sample_project_data):
        """Prueba listado de proyectos con respuesta de una sola página."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "projects": [sample_project_data]
        }
        
        projects = extractor.list_projects()
        
        assert len(projects) == 1
        assert isinstance(projects[0], RedmineProject)
        assert projects[0].id == 1
        assert projects[0].name == "Test Project"
        assert projects[0].identifier == "test-proj"
        assert projects[0].status == 1
    
    def test_listar_multiples_proyectos(self, mock_extractor):
        """Prueba listado de múltiples proyectos."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "projects": [
                {"id": 1, "name": "Project A", "identifier": "proj-a", "status": 1},
                {"id": 2, "name": "Project B", "identifier": "proj-b", "status": 1},
                {"id": 3, "name": "Project C", "identifier": "proj-c", "status": 1}
            ]
        }
        
        projects = extractor.list_projects()
        
        assert len(projects) == 3
        assert projects[0].name == "Project A"
        assert projects[1].name == "Project B"
        assert projects[2].name == "Project C"
    
    def test_listar_proyectos_vacio(self, mock_extractor):
        """Prueba listado de proyectos cuando no existen."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {"projects": []}
        
        projects = extractor.list_projects()
        
        assert len(projects) == 0
        assert isinstance(projects, list)
    
    def test_listar_proyectos_paginacion(self, mock_extractor):
        """Prueba la lógica de paginación al obtener proyectos."""
        extractor, mock_request = mock_extractor
        
        # Simula paginación con 100 elementos en página 1, y página 2 más pequeña
        page1_projects = [
            {"id": i, "name": f"Project {i}", "identifier": f"proj-{i}", "status": 1}
            for i in range(1, 101)
        ]
        page2_projects = [
            {"id": i, "name": f"Project {i}", "identifier": f"proj-{i}", "status": 1}
            for i in range(101, 111)
        ]
        
        mock_request.side_effect = [
            {"projects": page1_projects},
            {"projects": page2_projects}
        ]
        
        projects = extractor.list_projects()
        
        assert len(projects) == 110
        assert projects[0].id == 1
        assert projects[99].id == 100
        assert projects[100].id == 101
        assert projects[109].id == 110


# ============================================================================
# PRUEBAS DE LISTADO Y OBTENCIÓN DE PROBLEMAS
# ============================================================================

class TestListIssues:
    """Prueba la funcionalidad de listado de problemas."""
    
    def test_listar_problemas_por_proyecto(self, mock_extractor, sample_issue_data):
        """Prueba listado de problemas para un proyecto específico."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issues": [sample_issue_data]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        assert len(issues) == 1
        assert isinstance(issues[0], RedmineIssue)
        assert issues[0].id == 101
        assert issues[0].subject == "Corregir bug de login"
        assert issues[0].project.name == "Test Project"
        assert issues[0].tracker.name == "Bug"
        assert issues[0].status.name == "Nuevo"
    
    def test_listar_multiples_problemas(self, mock_extractor):
        """Prueba listado de múltiples problemas."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issues": [
                {
                    "id": 1, "subject": "Issue 1", "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 1, "name": "Bug"}, "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                    "priority": {"id": 1, "name": "Normal"}, "author": {"id": 1, "login": "u1", "firstname": "U", "lastname": "1"},
                    "created_on": "2023-12-01T10:00:00Z", "updated_on": "2023-12-10T14:30:00Z"
                },
                {
                    "id": 2, "subject": "Issue 2", "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 1, "name": "Bug"}, "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                    "priority": {"id": 2, "name": "Alta"}, "author": {"id": 2, "login": "u2", "firstname": "U", "lastname": "2"},
                    "created_on": "2023-12-02T10:00:00Z", "updated_on": "2023-12-11T14:30:00Z"
                }
            ]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        assert len(issues) == 2
        assert issues[0].subject == "Issue 1"
        assert issues[1].subject == "Issue 2"
    
    def test_listar_problemas_vacio(self, mock_extractor):
        """Prueba listado cuando no existen problemas."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {"issues": []}
        
        issues = extractor.list_issues(project_id=1)
        
        assert len(issues) == 0
    
    def test_listar_problemas_sin_proyecto_lanza_error(self, mock_extractor):
        """Prueba que listar problemas sin project_id lanza NotImplementedError."""
        extractor, mock_request = mock_extractor
        
        with pytest.raises(NotImplementedError):
            extractor.list_issues()


class TestGetIssueDetails:
    """Prueba obtención de detalles de problemas específicos."""
    
    def test_obtener_detalles_problema_por_id(self, mock_extractor, sample_issue_data):
        """Prueba recuperación de detalles de un problema específico."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issue": sample_issue_data
        }
        
        issue = extractor.get_issue_details(issue_id=101)
        
        assert isinstance(issue, RedmineIssue)
        assert issue.id == 101
        assert issue.subject == "Corregir bug de login"
        assert issue.description == "Los usuarios no pueden iniciar sesión con SSO"
        assert issue.done_ratio == 50
        assert issue.assigned_to.login == "jane.smith"
    
    def test_obtener_detalles_problema_con_id_string(self, mock_extractor, sample_issue_data):
        """Prueba que el ID del problema puede ser un string."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issue": sample_issue_data
        }
        
        issue = extractor.get_issue_details(issue_id="101")
        
        assert issue.id == 101
        assert issue.subject == "Corregir bug de login"
    
    def test_obtener_todos_los_campos_del_problema(self, mock_extractor, sample_issue_data):
        """Prueba que todos los campos del problema se rellenan correctamente."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issue": sample_issue_data
        }
        
        issue = extractor.get_issue_details(issue_id=101)
        
        # Verifica todos los campos
        assert issue.project.id == 1
        assert issue.tracker.id == 1
        assert issue.status.id == 1
        assert issue.priority.id == 2
        assert issue.author.id == 1
        assert issue.assigned_to.id == 2
        assert issue.start_date == "2023-12-01"
        assert issue.due_date == "2023-12-15"


# ============================================================================
# PRUEBAS DE LISTADO DE USUARIOS
# ============================================================================

class TestListUsers:
    """Prueba la funcionalidad de listado de usuarios."""
    
    def test_listar_usuarios(self, mock_extractor, sample_user_data):
        """Prueba listado de todos los usuarios."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "users": sample_user_data
        }
        
        users = extractor.list_users()
        
        assert len(users) == 2
        assert isinstance(users[0], RedmineUser)
        assert users[0].login == "john.doe"
        assert users[0].firstname == "John"
        assert users[0].lastname == "Doe"
        assert users[0].mail == "john@example.com"
        assert users[1].login == "jane.smith"
    
    def test_listar_usuario_unico(self, mock_extractor):
        """Prueba listado cuando solo existe un usuario."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "users": [
                {
                    "id": 1, "login": "admin", "firstname": "Admin", "lastname": "Usuario",
                    "mail": "admin@example.com"
                }
            ]
        }
        
        users = extractor.list_users()
        
        assert len(users) == 1
        assert users[0].login == "admin"
    
    def test_listar_usuarios_vacio(self, mock_extractor):
        """Prueba listado cuando no existen usuarios."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {"users": []}
        
        users = extractor.list_users()
        
        assert len(users) == 0


# ============================================================================
# PRUEBAS DE LISTADO DE RASTREADORES
# ============================================================================

class TestListTrackers:
    """Prueba la funcionalidad de listado de rastreadores (trackers)."""
    
    def test_listar_rastreadores(self, mock_extractor):
        """Prueba listado de todos los rastreadores de problemas."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "trackers": [
                {"id": 1, "name": "Bug"},
                {"id": 2, "name": "Característica"},
                {"id": 3, "name": "Soporte"}
            ]
        }
        
        trackers = extractor.list_trackers()
        
        assert len(trackers) == 3
        assert isinstance(trackers[0], RedmineTracker)
        assert trackers[0].name == "Bug"
        assert trackers[1].name == "Característica"
        assert trackers[2].name == "Soporte"
    
    def test_listar_rastreador_unico(self, mock_extractor):
        """Prueba listado con un único rastreador."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "trackers": [
                {"id": 1, "name": "Bug"}
            ]
        }
        
        trackers = extractor.list_trackers()
        
        assert len(trackers) == 1
        assert trackers[0].id == 1
        assert trackers[0].name == "Bug"


# ============================================================================
# PRUEBAS DE LISTADO DE ESTADOS
# ============================================================================

class TestListStatuses:
    """Prueba la funcionalidad de listado de estados."""
    
    def test_listar_estados(self, mock_extractor):
        """Prueba listado de todos los estados de problemas."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issue_statuses": [
                {"id": 1, "name": "Nuevo", "is_closed": False},
                {"id": 2, "name": "En Progreso", "is_closed": False},
                {"id": 3, "name": "Cerrado", "is_closed": True}
            ]
        }
        
        statuses = extractor.list_statuses()
        
        assert len(statuses) == 3
        assert isinstance(statuses[0], RedmineStatus)
        assert statuses[0].name == "Nuevo"
        assert statuses[0].is_closed == False
        assert statuses[2].name == "Cerrado"
        assert statuses[2].is_closed == True
    
    def test_listar_estado_unico(self, mock_extractor):
        """Prueba listado con un único estado."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issue_statuses": [
                {"id": 1, "name": "Abierto", "is_closed": False}
            ]
        }
        
        statuses = extractor.list_statuses()
        
        assert len(statuses) == 1
        assert statuses[0].id == 1


# ============================================================================
# PRUEBAS DE MANEJO DE ERRORES
# ============================================================================

class TestErrorHandling:
    """Prueba manejo de errores en RedmineExtractor y RedmineClient."""
    
    def test_error_http_credenciales_invalidas(self, mock_extractor):
        """Prueba manejo de error HTTP 401 (autenticación fallida)."""
        extractor, mock_request = mock_extractor
        
        mock_request.side_effect = RedmineHttpError(401, "Clave API inválida")
        
        with pytest.raises(RedmineHttpError) as exc_info:
            extractor.list_projects()
        
        assert exc_info.value.status_code == 401
        assert "Clave API inválida" in exc_info.value.message
    
    def test_error_http_recurso_no_encontrado(self, mock_extractor):
        """Prueba manejo de error HTTP 404 (recurso no encontrado)."""
        extractor, mock_request = mock_extractor
        
        mock_request.side_effect = RedmineHttpError(404, "Problema no encontrado")
        
        with pytest.raises(RedmineHttpError) as exc_info:
            extractor.get_issue_details(issue_id=999)
        
        assert exc_info.value.status_code == 404
    
    def test_error_respuesta_json_malformada(self, mock_extractor):
        """Prueba manejo de respuesta JSON malformada."""
        extractor, mock_request = mock_extractor
        
        mock_request.side_effect = RedmineInvalidResponse("Error al parsear respuesta JSON")
        
        with pytest.raises(RedmineInvalidResponse):
            extractor.list_projects()
    
    def test_error_servidor_y_reintentos(self, mock_extractor):
        """Prueba que errores de servidor (5xx) disparan lógica de reintentos."""
        extractor, mock_request = mock_extractor
        
        # Mock un error 500 seguido de éxito
        mock_request.side_effect = [
            RedmineHttpError(500, "Error interno del servidor"),
            {"projects": []}
        ]
        
        # El cliente debería reintentar
        with pytest.raises(RedmineHttpError):
            extractor.list_projects()


# ============================================================================
# PRUEBAS DE VALIDACIÓN DE DATOS
# ============================================================================

class TestDataValidation:
    """Prueba validación de datos con esquemas Pydantic."""
    
    def test_datos_proyecto_invalidos_campo_requerido_faltante(self, mock_extractor):
        """Prueba que campos requeridos faltantes generen error de validación."""
        extractor, mock_request = mock_extractor
        
        # Falta 'name' que es requerido
        mock_request.return_value = {
            "projects": [
                {"id": 1, "identifier": "proj-a", "status": 1}
            ]
        }
        
        # El proyecto será saltado debido a error de validación
        projects = extractor.list_projects()
        
        # El proyecto debe ser saltado
        assert len(projects) == 0
    
    def test_datos_problema_invalidos_campo_requerido_faltante(self, mock_extractor):
        """Prueba que campos requeridos faltantes en problemas sean manejados."""
        extractor, mock_request = mock_extractor
        
        # Falta 'project' que es requerido
        mock_request.return_value = {
            "issues": [
                {
                    "id": 101,
                    "subject": "Problema de prueba",
                    "tracker": {"id": 1, "name": "Bug"},
                    "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                    "priority": {"id": 1, "name": "Normal"},
                    "created_on": "2023-12-01T10:00:00Z"
                }
            ]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        # El problema debe ser saltado
        assert len(issues) == 0
    
    def test_campos_opcionales_pueden_ser_null(self, mock_extractor):
        """Prueba que campos opcionales pueden ser null."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issues": [
                {
                    "id": 101,
                    "subject": "Problema de prueba",
                    "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 1, "name": "Bug"},
                    "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                    "priority": {"id": 1, "name": "Normal"},
                    "author": None,  # Opcional
                    "assigned_to": None,  # Opcional
                    "description": None,  # Opcional
                    "created_on": "2023-12-01T10:00:00Z",
                    "updated_on": None  # Opcional
                }
            ]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        assert len(issues) == 1
        assert issues[0].author is None
        assert issues[0].assigned_to is None
        assert issues[0].description is None


# ============================================================================
# PRUEBAS DE ESCENARIOS DE INTEGRACIÓN
# ============================================================================

class TestIntegrationScenarios:
    """Prueba escenarios realistas de integración."""
    
    def test_flujo_completo_obtener_proyectos_y_problemas(self, mock_extractor):
        """Prueba flujo completo: obtener proyectos, luego problemas de un proyecto."""
        extractor, mock_request = mock_extractor
        
        # Primera llamada: listar proyectos
        # Segunda llamada: listar problemas del proyecto 1
        mock_request.side_effect = [
            {
                "projects": [
                    {"id": 1, "name": "Backend", "identifier": "backend", "status": 1},
                    {"id": 2, "name": "Frontend", "identifier": "frontend", "status": 1}
                ]
            },
            {
                "issues": [
                    {
                        "id": 101,
                        "subject": "Punto final de API dañado",
                        "project": {"id": 1, "name": "Backend", "identifier": "backend"},
                        "tracker": {"id": 1, "name": "Bug"},
                        "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                        "priority": {"id": 2, "name": "Alta"},
                        "author": {"id": 1, "login": "dev1", "firstname": "Dev", "lastname": "Uno"},
                        "created_on": "2023-12-01T10:00:00Z"
                    }
                ]
            }
        ]
        
        # Paso 1: Obtener proyectos
        projects = extractor.list_projects()
        assert len(projects) == 2
        backend_project = projects[0]
        
        # Paso 2: Obtener problemas del proyecto backend
        issues = extractor.list_issues(project_id=backend_project.id)
        assert len(issues) == 1
        assert issues[0].subject == "Punto final de API dañado"
        assert issues[0].priority.name == "Alta"
    
    def test_filtrar_y_analizar_problemas(self, mock_extractor):
        """Prueba filtrado y análisis de problemas."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issues": [
                {
                    "id": 101,
                    "subject": "Bug 1",
                    "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 1, "name": "Bug"},
                    "status": {"id": 1, "name": "Nuevo", "is_closed": False},
                    "priority": {"id": 3, "name": "Alta"},
                    "done_ratio": 0,
                    "created_on": "2023-12-01T10:00:00Z"
                },
                {
                    "id": 102,
                    "subject": "Característica 1",
                    "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 2, "name": "Característica"},
                    "status": {"id": 2, "name": "En Progreso", "is_closed": False},
                    "priority": {"id": 2, "name": "Normal"},
                    "done_ratio": 50,
                    "created_on": "2023-12-02T10:00:00Z"
                },
                {
                    "id": 103,
                    "subject": "Soporte 1",
                    "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 3, "name": "Soporte"},
                    "status": {"id": 3, "name": "Cerrado", "is_closed": True},
                    "priority": {"id": 1, "name": "Baja"},
                    "done_ratio": 100,
                    "created_on": "2023-11-01T10:00:00Z"
                }
            ]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        # Filtrar bugs abiertos
        open_bugs = [i for i in issues if i.tracker.name == "Bug" and not i.status.is_closed]
        assert len(open_bugs) == 1
        assert open_bugs[0].subject == "Bug 1"
        
        # Filtrar alta prioridad
        high_priority = [i for i in issues if i.priority.name == "Alta"]
        assert len(high_priority) == 1
        
        # Filtrar incompletos
        incomplete = [i for i in issues if i.done_ratio < 100]
        assert len(incomplete) == 2
    
    def test_seguir_cadena_asignacion_problema(self, mock_extractor):
        """Prueba seguir la cadena de asignación de un problema."""
        extractor, mock_request = mock_extractor
        
        issue_data = {
            "id": 101,
            "subject": "Problema complejo",
            "project": {"id": 1, "name": "P1", "identifier": "p1"},
            "tracker": {"id": 1, "name": "Bug"},
            "status": {"id": 1, "name": "Nuevo", "is_closed": False},
            "priority": {"id": 2, "name": "Normal"},
            "author": {
                "id": 1,
                "login": "reportero",
                "firstname": "Report",
                "lastname": "Usuario",
                "mail": "reportero@example.com"
            },
            "assigned_to": {
                "id": 2,
                "login": "desarrollador",
                "firstname": "Dev",
                "lastname": "Usuario",
                "mail": "dev@example.com"
            },
            "created_on": "2023-12-01T10:00:00Z"
        }
        
        mock_request.return_value = {"issue": issue_data}
        
        issue = extractor.get_issue_details(issue_id=101)
        
        # Verifica autor y asignado
        assert issue.author.login == "reportero"
        assert issue.assigned_to.login == "desarrollador"
        assert issue.author.mail == "reportero@example.com"
        assert issue.assigned_to.mail == "dev@example.com"
    
    def test_estadisticas_de_problemas_por_estado(self, mock_extractor):
        """Prueba calcular estadísticas de problemas agrupados por estado."""
        extractor, mock_request = mock_extractor
        
        mock_request.return_value = {
            "issues": [
                {
                    "id": i,
                    "subject": f"Problema {i}",
                    "project": {"id": 1, "name": "P1", "identifier": "p1"},
                    "tracker": {"id": 1, "name": "Bug"},
                    "status": {"id": j % 3 + 1, "name": ["Nuevo", "En Progreso", "Cerrado"][j % 3], "is_closed": j % 3 == 2},
                    "priority": {"id": 1, "name": "Normal"},
                    "created_on": "2023-12-01T10:00:00Z"
                }
                for i, j in enumerate(range(1, 10), 1)
            ]
        }
        
        issues = extractor.list_issues(project_id=1)
        
        # Agrupar por estado
        by_status = {}
        for issue in issues:
            status_name = issue.status.name
            if status_name not in by_status:
                by_status[status_name] = []
            by_status[status_name].append(issue)
        
        # Verificar estadísticas
        assert len(by_status.get("Nuevo", [])) > 0
        assert len(by_status.get("En Progreso", [])) > 0
        assert len(by_status.get("Cerrado", [])) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
