import glob
import libsixel as sx
from PIL import Image
from io import BytesIO


def media_file_from_id(media_id):
	files = glob.glob(f"./{media_id}.*")
	assert len(files) == 1
	return files[0]


def img(file):
	s = BytesIO()

	image = Image.open(file)
	width, height = image.size
	try:
		data = image.tobytes()
	except NotImplementedError:
		data = image.tostring()
	output = sx.sixel_output_new(lambda data, s: s.write(data), s)

	try:
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
	media_id = "687482244532536160"
	s = img(media_file_from_id(media_id)) or f'[image]({media_id})'
	print(s)

