# This is replaced during release process.
__version_suffix__ = '177'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.24.17"
KUBECTL_SHA512 = {
    "linux": "7a8d578f3b1644c5a469c2e137e9287fb7349818512006b106d9feee38959b32808c4fa0ef31526131da688015db0b8c4a85392c68b92d323f5d47b0775553aa",
    "darwin": "09374af750a0bbc839844a9e70ac3e8f7572dfd4fbb10c13a3b13d6ff2012790afb0b92dac2bf52882fe822ae3de7c4d65a0b64f17c74ca1d12c88657fed3f7b",
}
STERN_VERSION = "1.26.0"
STERN_SHA256 = {
    "linux": "de79474d9197582e38da0dccc8cd14af23d6b52b72bee06b62943c19ab95125e",
    "darwin": "f89631ea73659e1db4e9d8ef94c58cd2c4e92d595e5d2b7be9184f86e755ee95",
}
KUBELOGIN_VERSION = "v1.28.0"
KUBELOGIN_SHA256 = {
    "linux": "83282148fcc70ee32b46edb600c7e4232cbad02a56de6dc17e43e843fa55e89e",
    "darwin": "8169c6e85174a910f256cf21f08c4243a4fb54cd03a44e61b45129457219e646",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
