from infra.routes import app
import uvicorn

from infra.adapters.database.migrations.migration import execute_migration

execute_migration()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
