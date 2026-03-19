import os
import secrets
import string
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netflix_dashboard.settings")

    import django  # noqa: PLC0415

    django.setup()

    from django.contrib.auth import get_user_model  # noqa: PLC0415

    User = get_user_model()

    username = "admin"
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits + "-_") for _ in range(20)
    )

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"is_staff": True, "is_superuser": True, "email": ""},
    )
    if not created:
        user.is_staff = True
        user.is_superuser = True
        if not getattr(user, "email", None):
            user.email = ""

    user.set_password(password)
    user.save()

    print(f"username={username}")
    print(f"password={password}")
    print(f"created={created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

