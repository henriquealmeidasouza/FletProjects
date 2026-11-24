import asyncio
import os
import random
import sys
import uuid

import cv2
import flet as ft
import flet_camera as fc
import numpy as np
import requests

from database import (
    PokeFruitDatabase,
    get_pokefruit_data,
    list_saved_pokefruits,
    save_pokefruit_data,
)
from qrcode_utils import extract_pokefruit_code

PIC_IVAL = 1
SERVER_URL = os.environ.get("POKEFRUIT_SERVER_URL", "http://192.168.3.11:5000").rstrip("/")


def normalize_code(code: str | None) -> str:
    return (code or "").strip()


def generate_unique_code() -> str:
    return f"CPDOG-{uuid.uuid4().hex[:12].upper()}"


LOCAL_POKEFRUIT_CATALOG = (
    {
        "name": "Bananachu",
        "type": ["Electric"],
        "weight_g": 6000,
        "height_cm": 40,
        "weakness": ["Ground"],
        "strength": ["Water", "Flying"],
        "Evolution": ["Bachu"],
        "url_image": "https://picsum.photos/400/400",
        "voice": "https://fake.sound/bananachu.ogg",
    },
    {
        "name": "Pearas",
        "type": ["Insect", "Grass"],
        "weight_g": 5400,
        "height_cm": 30,
        "weakness": ["Fire", "Ice", "Rock", "Poison", "Flying", "Insect"],
        "strength": ["Fighter", "Water", "Plant", "Electric", "Ground"],
        "evolution": [None],
        "url_image": "https://picsum.photos/400/400",
        "voice": "https://fake.sound/pearas.ogg",
    },
)


def create_random_pokefruit(code: str) -> dict:
    payload = dict(random.choice(LOCAL_POKEFRUIT_CATALOG))
    payload["code"] = code
    payload["generated"] = True
    payload["id"] = None
    return payload


def format_list(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item is not None) or "Nenhum"
    if value is None:
        return "Nenhum"
    return str(value)


def fetch_pokefruit_data(code: str | None):
    normalized = normalize_code(code)
    if not normalized:
        raise ValueError("Código do Pokefruit não informado.")

    try:
        response = requests.get(f"{SERVER_URL}/fetch/{normalized}", timeout=5)
        if response.status_code == 404:
            payload = create_random_pokefruit(normalized)
        else:
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or not payload:
                payload = create_random_pokefruit(normalized)
    except requests.RequestException:
        saved = get_pokefruit_data(normalized)
        if saved is not None:
            return saved
        payload = create_random_pokefruit(normalized)

    save_pokefruit_data(normalized, payload)
    return payload


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
        if self.page is not None:
            self.page.run_task(self.capture_qrcode)


@ft.control
class MainScreen(ft.Container):
    def init(self):
        self.camera = CameraWidget(width=400, height=260)
        self.camera.set_on_detect_qrcode(self.on_detect_qrcode)
        self.generated_code = ""
        self.code_input = ft.TextField(label="Código do Pokefruit")
        self.status_text = ft.Text("Nenhum código identificado.")
        self.read_btn = ft.Button("Ler QR Code", on_click=self.on_click_read_btn)
        self.generate_btn = ft.Button("Gerar código único", on_click=self.on_click_generate_btn)
        self.manual_btn = ft.Button("Abrir código", on_click=self.on_click_open_manual_code)
        self.saved_pokefruits_list = ft.ListView(expand=True, spacing=4)
        self.load_saved_pokefruits_list()
        self.content = self.home_view()

    def saved_sidebar(self):
        return ft.Container(
            width=220,
            padding=10,
            bgcolor=ft.Colors.SURFACE,
            border=ft.Border.all(width=1, color=ft.Colors.OUTLINE),
            content=ft.Column(
                controls=[
                    ft.Text("Pokefruits Salvos", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.saved_pokefruits_list,
                ],
                spacing=8,
                expand=True,
            ),
        )

    def app_layout(self, main_content):
        return ft.Row(
            controls=[
                self.saved_sidebar(),
                ft.Container(
                    expand=True,
                    padding=20,
                    content=main_content,
                ),
            ],
            spacing=12,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def home_view(self):
        main_content = ft.Column(
            controls=[
                ft.Text("PokeFruits", size=24, weight=ft.FontWeight.BOLD),
                self.camera,
                self.read_btn,
                self.generate_btn,
                self.code_input,
                self.manual_btn,
                self.status_text,
            ],
            spacing=12,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        return self.app_layout(main_content)

    async def on_click_read_btn(self, e):
        try:
            await self.camera.run()
        except RuntimeError:
            code = generate_unique_code()
            self.generated_code = code
            self.status_text.value = f"Câmera não encontrada. Código gerado: {code}"
            self.status_text.update()

    def on_click_generate_btn(self, e):
        code = generate_unique_code()
        self.generated_code = code
        self.code_input.value = code
        self.code_input.update()
        self.status_text.value = f"Código único gerado: {code}"
        self.status_text.update()

    def on_click_open_manual_code(self, e):
        code = normalize_code(self.code_input.value)
        if not code:
            self.status_text.value = "Informe um código para abrir os dados."
            self.status_text.update()
            return
        self.open_detail(code)

    def on_detect_qrcode(self, data: str):
        try:
            code = extract_pokefruit_code(data)
        except ValueError as error:
            self.status_text.value = str(error)
            self.status_text.update()
            return

        self.code_input.value = code
        self.code_input.update()
        self.open_detail(code)

    def open_detail(self, code: str):
        normalized = normalize_code(code)
        if not normalized:
            self.status_text.value = "Código inválido."
            self.status_text.update()
            return

        try:
            payload = fetch_pokefruit_data(normalized)
        except (LookupError, ValueError) as error:
            self.status_text.value = str(error)
            self.status_text.update()
            return

        self.generated_code = normalized
        self.update_saved_pokefruits_list()
        self.content = self.app_layout(self.detail_view(payload))
        self.update()

    def detail_view(self, payload):
        evolution = payload.get("Evolution", payload.get("evolution", []))
        image_url = payload.get("url_image")
        image = ft.Image(
            src=image_url,
            width=260,
            height=260,
            fit=ft.BoxFit.CONTAIN,
        ) if image_url else ft.Text("Imagem não disponível")

        controls = [
            ft.Text("Dados do Pokefruit", size=22, weight=ft.FontWeight.BOLD),
            image,
            ft.Text(f"Código: {payload.get('code', '')}"),
            ft.Text(f"Nome: {payload.get('name', '---')}"),
            ft.Text(f"Tipo: {format_list(payload.get('type'))}"),
            ft.Text(f"Peso: {payload.get('weight_g', '---')} g"),
            ft.Text(f"Altura: {payload.get('height_cm', '---')} cm"),
            ft.Text(f"Fraquezas: {format_list(payload.get('weakness'))}"),
            ft.Text(f"Forças: {format_list(payload.get('strength'))}"),
            ft.Text(f"Evolução: {format_list(evolution)}"),
            ft.Text(f"Voz: {payload.get('voice', 'Não disponível')}"),
            ft.Button("Voltar", on_click=self.on_click_back),
        ]

        return ft.Column(
            controls=controls,
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def on_click_back(self, e):
        self.content = self.home_view()
        self.update()

    def load_saved_pokefruits_list(self):
        self.saved_pokefruits_list.controls.clear()
        try:
            saved_pokefruits = list_saved_pokefruits()
            for pokefruit in saved_pokefruits:
                self.saved_pokefruits_list.controls.append(
                    ft.ListTile(
                        title=pokefruit.get("name", "Sem nome"),
                        subtitle=pokefruit.get("code", ""),
                        on_click=lambda e, code=pokefruit.get("code"): self.open_detail(code),
                    )
                )
        except Exception as error:
            print(f"Erro ao listar Pokefruits salvos: {error}")

    def update_saved_pokefruits_list(self):
        self.load_saved_pokefruits_list()
        if self.saved_pokefruits_list.page is not None:
            self.saved_pokefruits_list.update()
