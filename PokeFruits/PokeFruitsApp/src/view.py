import asyncio
import cv2
import flet as ft
import flet_camera as fc
import numpy as np

from qrcode_utils import extract_pokefruit_code

PIC_IVAL = 1

@ft.control
class CameraWidget(ft.Container):
    def init(self):
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
        self.content = ft.Column(
            controls=[
                self.camera,
                self.read_btn,
                self.qr_content,
            ]
        )

    async def on_click_read_btn(self, e):
        await self.camera.run()

    def on_detect_qrcode(self, data: str):
        try:
            code = extract_pokefruit_code(data)
        except ValueError as error:
            self.qr_content.value = str(error)
        else:
            self.qr_content.value = code
        self.qr_content.update()
