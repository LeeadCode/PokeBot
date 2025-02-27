import aiohttp
import cv2
import numpy as np
from io import BytesIO

async def create_black_silhouette_from_url(image_url: str) -> BytesIO:
    try:
        # Baixar a imagem da URL usando aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    raise ValueError(f"Falha ao baixar imagem: {response.status}")
                buffer = BytesIO(await response.read())

        # Ler a imagem usando OpenCV
        image_array = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError("Falha ao decodificar a imagem")

        # Converter imagem RGBA para BGR (OpenCV usa BGR por padrão)
        if image.shape[2] == 4:  # Se a imagem for RGBA
            # Substituir pixels com alfa > 0 por preto
            alpha_channel = image[:, :, 3]
            image[alpha_channel > 0] = [0, 0, 0, 255]

        # Converter para formato PNG
        _, output_buffer = cv2.imencode('.png', image)

        # Retornar a imagem como um buffer
        return BytesIO(output_buffer.tobytes())

    except Exception as e:
        print(f"Erro ao criar a silhueta: {e}")
        raise
