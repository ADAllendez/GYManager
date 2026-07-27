"""
╔══════════════════════════════════════════════════════════╗
║           RESETEO DE CONTRASEÑA - Usuario Root          ║
║                                                          ║
║  Ejecutar desde la carpeta backend:                      ║
║    python reset_root.py                                  ║
║                                                          ║
║  Esto resetea la contraseña del usuario root (o del      ║
║  usuario con rol 'root') para que puedas volver a        ║
║  ingresar al sistema.                                    ║
╚══════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import getpass

# ── Cargar .env ──────────────────────────────────────────
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ[key.strip()] = val.strip()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "mysql+aiomysql://root:@localhost/gym_manager"
)

# ── Imports de la app ────────────────────────────────────
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update
from passlib.context import CryptContext

# Modelo — importar directamente para evitar dependencias circulares
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def resetear():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # Buscar el usuario con rol 'root'
        result = await db.execute(select(Usuario).where(Usuario.rol == "root"))
        user = result.scalar_one_or_none()

        if not user:
            print("\n❌ No se encontró ningún usuario con rol 'root' en la base de datos.")
            print("   Puede que necesites crear uno manualmente.")
            await engine.dispose()
            return

        print(f"\n🔍 Usuario root encontrado:")
        print(f"   ID:       {user.id_usuario}")
        print(f"   Username: {user.username}")
        print(f"   Nombre:   {user.nombre or '-'} {user.apellido or '-'}")
        print(f"   Rol:      {user.rol}")
        print()

        # Preguntar nueva contraseña
        while True:
            nueva_pass = getpass.getpass("🔑 Nueva contraseña (mín. 4 caracteres): ")
            if len(nueva_pass.strip()) < 4:
                print("   ⚠️  La contraseña debe tener al menos 4 caracteres. Intentá de nuevo.")
                continue
            confirmar = getpass.getpass("🔑 Confirmar contraseña: ")
            if nueva_pass != confirmar:
                print("   ⚠️  Las contraseñas no coinciden. Intentá de nuevo.")
                continue
            break

        # También preguntar si quiere resetear el username
        cambiar_user = input("\n¿Querés cambiar también el nombre de usuario? (s/N): ").strip().lower()
        nuevo_username = None
        if cambiar_user == "s":
            nuevo_username = input("   Nuevo username: ").strip()
            if len(nuevo_username) < 3:
                print("   ⚠️  El username debe tener al menos 3 caracteres. Se mantiene el actual.")
                nuevo_username = None

        # Aplicar cambios
        user.password_hash = pwd_context.hash(nueva_pass)
        if nuevo_username:
            user.username = nuevo_username

        await db.commit()
        await db.refresh(user)

        print(f"\n✅ ¡Contraseña reseteada correctamente!")
        if nuevo_username:
            print(f"   Nuevo username: {user.username}")
        print(f"   Ahora podés ingresar con:")
        print(f"   → Usuario:    {user.username}")
        print(f"   → Contraseña: (la que acabás de poner)")
        print()

    await engine.dispose()


if __name__ == "__main__":
    print(__doc__)
    try:
        asyncio.run(resetear())
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
