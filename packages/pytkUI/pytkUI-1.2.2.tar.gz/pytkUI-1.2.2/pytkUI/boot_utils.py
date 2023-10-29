from ttkbootstrap import Style


def get_color(color):
    """
    通过ttkbootstrap的主题颜色字符 获取颜色值
    """
    return Style().colors.get(color)
