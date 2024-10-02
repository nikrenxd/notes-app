from dj_rest_auth.serializers import LoginSerializer


class EmailLoginSerializer(LoginSerializer):
    username = None
