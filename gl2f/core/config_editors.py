def max_image_size():
	w, h = map(int, input('width height (size in pixels): ').replace(',',' ').split())
	return (w, h)

def get():
	return {
		'max-image-size': max_image_size
	}