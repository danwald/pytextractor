import pytest

from pytextractor.pytextractor import PyTextractor

class TestDetector(object):
    def setup_method(self, method):
        self.extractor = PyTextractor()

    @pytest.mark.parametrize('image,expected_number', [
        ('assets/test_images/52.png', 52),
        ('assets/test_images/53.png', 53),
        ('assets/test_images/56.png', 56),
        ('assets/test_images/57.png', 57),
    ])
    def test_number_extractor(self, image, expected_number):
        detected = self.extractor.get_image_text(image, number=True)
        assert len(detected)
