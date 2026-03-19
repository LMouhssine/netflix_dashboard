## Scripts

Ces scripts fournissent un workflow propre et cross-platform pour installer et lancer le projet.

### Windows (PowerShell)

- Setup (venv + deps + `.env` + migrations) :

```powershell
.\scripts\setup.ps1
```

- Run server :

```powershell
.\scripts\run.ps1
```

- Import dataset :

```powershell
.\scripts\import_data.ps1
# ou
.\scripts\import_data.ps1 -Path .\data\netflix_titles.csv
```

- Diagnostic rapide :

```powershell
.\scripts\doctor.ps1
```

### macOS / Linux (bash)

```bash
./scripts/setup.sh
./scripts/run.sh
./scripts/import_data.sh ./data/netflix_titles.csv
./scripts/doctor.sh
```
