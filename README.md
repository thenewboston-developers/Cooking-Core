## Project setup

Project setup instructions here.

```bash
mkdir -p local
cp cooking_core/project/settings/templates/settings.dev.py ./local/settings.dev.py
```

```bash
make shell

from cooking_core.config.models import Config
Config.objects.create(owner=None, transaction_fee=1)
```
