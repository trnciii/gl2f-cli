import glob
import libsixel as sx
from PIL import Image
from io import BytesIO
from gl2f.util import path
import os

def media_file_from_id(media_id):
	files = glob.glob(f'{os.path.join(path.media(), media_id)}.*')
	assert len(files) == 1
	return files[0]


def fit(image, size):
	w, h = image.size
	r = min(size[0]/w, size[1]/h)
	w, h = int(r*w), int(r*h)
	return image.resize((w, h))


def limit(image, size):
	w, h = image.size
	r = min(size[0]/w, size[1]/h)
	if r < 1:
		w, h = int(r*w), int(r*h)
	return image.resize((w, h))


def img(media_id):
	file = media_file_from_id(media_id)
	image = Image.open(file)
	image = limit(image, (1000, 1000))
	return to_sixel(image)


def to_sixel(image):
	s = BytesIO()
	try:
		data = image.tobytes()
	except NotImplementedError:
		data = image.tostring()
	output = sx.sixel_output_new(lambda data, s: s.write(data), s)

	try:
		width, height = image.size
		if image.mode == 'RGBA':
			dither = sx.sixel_dither_new(256)
			sx.sixel_dither_initialize(dither, data, width, height, sx.SIXEL_PIXELFORMAT_RGBA8888)
		elif image.mode == 'RGB':
			dither = sx.sixel_dither_new(256)
			sx.sixel_dither_initialize(dither, data, width, height, sx.SIXEL_PIXELFORMAT_RGB888)
		elif image.mode == 'P':
			palette = image.getpalette()
			dither = sx.sixel_dither_new(256)
			sx.sixel_dither_set_palette(dither, palette)
			sx.sixel_dither_set_pixelformat(dither, sx.SIXEL_PIXELFORMAT_PAL8)
		elif image.mode == 'L':
			dither = sixel_dither_get(sx.SIXEL_BUILTIN_G8)
			sx.sixel_dither_set_pixelformat(dither, sx.SIXEL_PIXELFORMAT_G8)
		elif image.mode == '1':
			dither = sixel_dither_get(sx.SIXEL_BUILTIN_G1)
			sx.sixel_dither_set_pixelformat(dither, sx.SIXEL_PIXELFORMAT_G1)
		else:
			raise RuntimeError('unexpected image mode')

		try:
			sx.sixel_encode(data, width, height, 1, dither, output)
			return s.getvalue().decode('ascii')
		finally:
			sx.sixel_dither_unref(dither)
	finally:
		sx.sixel_output_unref(output)


if __name__ == '__main__':
	media_id = "688741780203504480"
	s = img(media_id)
	print('111')
	print(s)

