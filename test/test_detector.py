import pytest

from pytextractor.pytextractor import PyTextractor

class TestDetector(object):
    def setup_method(self, method):
        self.extractor = PyTextractor()

    @pytest.mark.parametrize('image', [
        ('assets/test_images/52.png'),
        ('assets/test_images/53.png'),
        ('assets/test_images/56.png'),
    ])
    def test_number_detector(self, image):
        detected = self.extractor.get_image_text(image, number=True)
        assert len(detected)


    @pytest.mark.parametrize('image,expected_number', [
        ('assets/test_images/52.png', 52),
        ('assets/test_images/53.png', 53),
        ('assets/test_images/56.png', 56),
    ])
    def test_number_extractor(self, image, expected_number):
        detected = self.extractor.get_image_text(image, number=True)
        assert int(detected[0]) == expected_number


    @pytest.mark.skip(reason="[LIMITATION] can't detect number")
    @pytest.mark.parametrize('image,expected_number', [
        ('assets/test_images/57.png', 57),
    ])
    def test_number_extractor_tweaked(self, image, expected_number):
        detected = self.extractor.get_image_text(image, number=True, percentage=4)
        assert int(detected[0]) == expected_number
