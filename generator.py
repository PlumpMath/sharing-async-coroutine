def gen_fn():
	print('start')
	yield 1

	print('middle')
	print('middle2')
	print('middle3')

	yield 2

	print('done')
