"""Pantalla de inicio de sesion (REQ-USU-02).

El sistema Java abria directo en el menu principal. Aqui esta pantalla es
obligatoria: sin sesion las politicas RLS de Supabase no devuelven ni un
libro, asi que no hay forma de saltarsela.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QWidget

from biblioteca.core.sesion import ErrorDeAcceso, Sesion, iniciar_sesion
from biblioteca.ui.estilo import COLOR_ERROR, aplicar_estilo_titulo
from biblioteca.ui.generado.ui_login import Ui_DialogoLogin


class DialogoLogin(QDialog):
    """Pide las credenciales y deja lista la sesion del bibliotecario."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoLogin()
        self.ui.setupUi(self)

        self.sesion: Sesion | None = None

        aplicar_estilo_titulo(self.ui.etiquetaTitulo, self.ui.etiquetaEscuela)
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")

        self.ui.botonEntrar.clicked.connect(self._entrar)
        self.ui.campoCorreo.returnPressed.connect(self._entrar)
        self.ui.campoContrasena.returnPressed.connect(self._entrar)

        self.ui.campoCorreo.setFocus()

    def _entrar(self) -> None:
        correo = self.ui.campoCorreo.text().strip()
        contrasena = self.ui.campoContrasena.text()

        if not correo or not contrasena:
            self._mostrar_error("Escribe tu correo y tu contraseña.")
            return

        self._ocupado(True)
        try:
            self.sesion = iniciar_sesion(correo, contrasena)
        except ErrorDeAcceso as error:
            self._mostrar_error(str(error))
            self.ui.campoContrasena.clear()
            self.ui.campoContrasena.setFocus()
            return
        except Exception:
            self._mostrar_error(
                "No se pudo conectar con el servidor. Revisa tu conexión a internet."
            )
            return
        finally:
            self._ocupado(False)

        self.accept()

    def _mostrar_error(self, mensaje: str) -> None:
        self.ui.etiquetaError.setText(mensaje)

    def _ocupado(self, ocupado: bool) -> None:
        """Evita dobles clics mientras se valida contra el servidor."""
        self.ui.botonEntrar.setEnabled(not ocupado)
        self.ui.botonEntrar.setText("Verificando…" if ocupado else "Entrar")
        if ocupado:
            self.ui.etiquetaError.clear()
        QApplication.processEvents()


def pedir_sesion(padre: QWidget | None = None) -> Sesion | None:
    """Muestra el dialogo y devuelve la sesion, o None si se cancelo."""
    dialogo = DialogoLogin(padre)
    if dialogo.exec() == QDialog.DialogCode.Accepted:
        return dialogo.sesion
    return None
