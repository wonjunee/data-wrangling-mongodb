import xlrd

datafile = "native_Load_2016.xlsx"

def parse_file(datafile):
	workbook = xlrd.open_workbook(datafile)
	sheet = workbook.sheet_by_index(0)
	
	data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

	cv = sheet.col_values(1, start_rowx=1, end_rowx = None)

	maxval = max(cv)
	minval = min(cv)

	maxpos = cv.index(maxval) + 1
	minpos = cv.index(minval) + 1

	maxtime = sheet.cell_value(maxpos, 0)
	realtime = xlrd.xldate_as_tuple(maxtime, 0)
	mintime = sheet.cell_value(minpos, 0)
	realmintime = xlrd.xldate_as_tuple(mintime,0)
	data = {
			'maxtime':realtime,
			'maxvalue':maxval,
			'mintime':realmintime,
			'minvalue':minval,
			'avgcoast':sum(cv) / float(len(cv))
	}
	return data

data= parse_file(datafile)
import pprint
pprint.pprint(data)

assert data['maxtime'] == (2014,8,13,17,0,0)