import sys
print('Python:', sys.version.split()[0])
try:
    import fastapi, sqlmodel, pydantic
    print('fastapi:', fastapi.__version__)
    print('sqlmodel:', sqlmodel.__version__)
    print('pydantic:', pydantic.__version__)
    from app.main import app
    print('✓ app imported successfully')
except Exception as e:
    import traceback
    traceback.print_exc()

