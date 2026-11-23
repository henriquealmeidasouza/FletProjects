import asyncio
import cv2
import flet as ft
import flet_camera as fc
import httpx
import numpy as np
import os
import sys

from qrcode_utils import extract_pokefruit_code
from database import PokeFruitDatabase

PIC_IVAL = 1
SERVER_URL = os.getenv("POKEFRUITS_SERVER_URL", "http://127.0.0.1:5000")

@ft.control
class CameraWidget(ft.Container):
    def init(self):
        self.preview = None
        self.desktop = sys.platform.startswith("win")
        if self.desktop:
            self.content = ft.Text(
                "Leitura por câmera disponível apenas no dispositivo móvel.",
                text_align=ft.TextAlign.CENTER,
            )
        else:
            self.preview = fc.Camera(
                expand=True,
                preview_enabled=True,
            )
            self.content = self.preview
        self.camera_initialized = False
        self.on_detect_qrcode = None

    def set_on_detect_qrcode(self, on_detect_qrcode):
        self.on_detect_qrcode = on_detect_qrcode

    def read_qrcode(self, jpeg_bytes: bytes) -> str | None:
        buf = np.frombuffer(jpeg_bytes, dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if img is None:
            return None
        detector = cv2.QRCodeDetector()
        data = detector.detectAndDecode(img)[0]
        if data:
            return data
        return None

    async def init_camera(self):
        if self.desktop:
            raise RuntimeError("A câmera não é suportada no Windows desktop.")
        cameras = await self.preview.get_available_cameras()
        if not cameras:
            raise RuntimeError("Nenhuma câmera disponível no dispositivo.")

        selected_camera = cameras[0]
        for cm in cameras:
            lens_direction = getattr(cm, "lens_direction", None)
            if lens_direction is not None and lens_direction == fc.CameraLensDirection.BACK:
                selected_camera = cm
                break

        await self.preview.initialize(
            description=selected_camera,
            resolution_preset=fc.ResolutionPreset.MEDIUM,
            enable_audio=False,
            image_format_group=fc.ImageFormatGroup.JPEG,
        )
        self.camera_initialized = True

    async def capture_qrcode(self):
        while True:
            if self.camera_initialized:
                jpeg_bytes = await self.preview.take_picture()
                data = self.read_qrcode(jpeg_bytes)
                if data and self.on_detect_qrcode is not None:
                    self.on_detect_qrcode(data)
            await asyncio.sleep(PIC_IVAL)

    async def run(self):
        await self.init_camera()
        self.page.run_task(self.capture_qrcode)

@ft.control
class MainScreen(ft.Container):
    def init(self):
        self.camera = CameraWidget(width=400)
        self.camera.set_on_detect_qrcode(self.on_detect_qrcode)
        self.read_btn = ft.Button("Ler", on_click=self.on_click_read_btn)
        self.qr_content = ft.Text(value="Nenhum")
        self.database = PokeFruitDatabase()
        self._is_fetching = False
        self.details_screen = ft.Column(
            visible=False,
            controls=[],
        )
        self.content = ft.Column(
            controls=[
                self.camera,
                self.read_btn,
                self.qr_content,
                self.details_screen,
            ]
        )

    async def on_click_read_btn(self, e):
        try:
            await self.camera.run()
        except RuntimeError as error:
            self.qr_content.value = str(error)
            self.qr_content.visible = True
            self.qr_content.update()

    def on_detect_qrcode(self, data: str):
        try:
            code = extract_pokefruit_code(data)
        except ValueError as error:
            self.qr_content.value = str(error)
            self.qr_content.update()
        else:
            self.qr_content.value = code
            self.qr_content.update()
            if not self._is_fetching:
                self.page.run_task(self.fetch_pokefruit, code)

    async def fetch_pokefruit(self, code: str):
        self._is_fetching = True
        self.qr_content.value = f"Buscando {code}..."
        self.qr_content.update()

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{SERVER_URL.rstrip('/')}/fetch/{code}")
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError):
            self.qr_content.value = "Não foi possível obter os dados do servidor."
            self.qr_content.update()
            return
        finally:
            self._is_fetching = False

        if not isinstance(payload, dict) or payload.get("code") != code:
            self.qr_content.value = "Pokefruit não encontrado."
            self.qr_content.update()
            return

        self.database.save(payload)
        self.show_pokefruit(payload)

    def show_pokefruit(self, pokefruit: dict):
        name = pokefruit.get("name", "Sem nome")
        types = pokefruit.get("type", [])
        type_text = ", ".join(types) if isinstance(types, list) else str(types)

        self.camera.visible = False
        self.read_btn.visible = False
        self.qr_content.visible = False
        self.details_screen.visible = True
        self.details_screen.controls = [
            ft.Text(name, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Código: {pokefruit.get('code', '')}"),
            ft.Text(f"Tipo: {type_text}"),
            ft.Text(f"Peso: {pokefruit.get('weight_g', '-')} g"),
            ft.Text(f"Altura: {pokefruit.get('height_cm', '-')} cm"),
            ft.Button("Voltar", on_click=self.back_to_camera),
        ]
        self.update()

    def back_to_camera(self, e):
        self.camera.visible = True
        self.read_btn.visible = True
        self.qr_content.visible = True
        self.details_screen.visible = False
        self.details_screen.controls = []
        self.update()
