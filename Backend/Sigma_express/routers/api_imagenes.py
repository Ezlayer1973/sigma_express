import sys, os
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, UploadFile, File
from decouple import config

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

cloudinary.config(
    cloud_name = config('PO_cloudinary_cloud'),
    api_key    = config('PO_cloudinary_key'),
    api_secret = config('PO_cloudinary_secret')
)

router = APIRouter(prefix="/imagenes", tags=["Imágenes"])

@router.post("/articulo/{codigo}")
async def subir_imagen(codigo: int, file: UploadFile = File(...)):
    try:
        contenido = await file.read()
        resultado = cloudinary.uploader.upload(
            contenido,
            folder="sigma_express/articulos",
            public_id=f"articulo_{codigo}",
            overwrite=True,
            resource_type="image"
        )
        return {"url": resultado["secure_url"]}
    except Exception as ex:
        print("Error al subir imagen", ex)
        return {"error": str(ex)}