from gui.constants.colors import AppColors


def format_criterion_tooltip(level: int, description: str) -> str:
    colors = {
        1: AppColors.TOOLTIP_CRITERION_1,
        2: AppColors.TOOLTIP_CRITERION_2,
        3: AppColors.TOOLTIP_CRITERION_3,
    }
    color = colors.get(level, AppColors.CANVAS)

    return f"""
    <div style='margin: 2px;'>
        <b style='color: {color}; font-size: 13px;'>{level}-деңгей</b>
        <hr style='border: 0.5px solid {AppColors.BORDER};'>
        <p style='width: 180px; line-height: 1.2;'>{description}</p>
    </div>
    """
