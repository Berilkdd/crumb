import os

os.environ["SECRET_KEY"] = "sd81fc6c616fb9120b0e89bcf996d2a8094aac7b2422c4662276e795a5373ba84"
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_si8fXjxUM1KR@ep-patient-truth-agst2yfl.c-2.eu-central-1.aws.neon.tech/zippy_atlas_error_570126"
os.environ.setdefault('DEVELOPMENT', '1')