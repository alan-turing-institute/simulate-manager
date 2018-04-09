class BaseConfig:
    """Base configuration"""
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SSH_USERNAME='testuser'
    SSH_HOSTNAME='gateway_simulator_1'
    SSH_PORT=22
    SSH_PRIVATE_KEY_PATH='keys/simulator_key'
    SIM_ROOT='/home/testuser'
    AZURE_ACCOUNT_NAME='sgmiddleware'
    AZURE_ACCOUNT_KEY='INSERT_ACCOUNT_KEY_HERE'
    TMP_SCRIPT_DIR="/tmp/"

    
class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
