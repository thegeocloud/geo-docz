# Debug properties
DEBUG = False

# Authentication
AUTH0_DOMAIN = ''
ALGORITHMS = 'RS256'
API_AUDIENCE = ''

# Database configuration
DB_NAME = ""
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PATH = "postgres://{}:{}@{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)

# Output location for qr codes
QR_CODE_FOLDER = r".\static\qrcodes"

# Cookies
SESSION_COOKIE_SECURE = True

