configs = []
routers = []
servlets_before = []
servlets_before_out_context = []
servlets_back = []
servlets_back_out_context = []

# TODO：后续可尝试通过自定义容器(可能是扩展list)的方式实现上述容器，使其更加定制化


__all__ = [
    'configs',
    'routers',
    'servlets_before',
    'servlets_back',
    'servlets_before_out_context',
    'servlets_back_out_context'
]
