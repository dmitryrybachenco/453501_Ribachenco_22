class DisplayMixin:
    """Mixin class for display functionality"""

    def display_info(self) -> None:
        """Display object information"""
        print(str(self))