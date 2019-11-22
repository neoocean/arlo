from arlo import Arlo

from datetime import timedelta, date
import datetime
import sys
import platform

import os.path
from os import path


USERNAME = ''
PASSWORD = ''

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD)
	# At this point you're logged into Arlo.

	today = (date.today()-timedelta(days=0)).strftime("%Y%m%d")
	seven_days_ago = (date.today() - timedelta(days=6)).strftime("%Y%m%d")

	# Get all of the recordings for a date range.
	library = arlo.GetLibrary(seven_days_ago, today)

	# 실행하는 기계에 따라 원드라이브 동기화 위치 변경
	if platform.node() == 'surface': 
		storage = 'E:/OneDrive/Video/arlo/Video/'
	elif platform.node() == 'home': 
		storage = 'D:/OneDrive/Video/arlo/Video/'
	elif platform.node() == 'DESKTOP-F4EOHEL': 
		storage = 'D:/OneDrive/Video/arlo/Video/'
	else:
		storage = 'E:/OneDrive/Video/arlo/Video/'
	print('platform.node() = ' + platform.node())

	# 다운로드 할지말지 결정.
	doDownload = False

	# Iterate through the recordings in the library.
	for recording in library:

		videofilename = datetime.datetime.fromtimestamp(int(recording['name'])//1000).strftime('%Y-%m-%d %H-%M-%S') + ' ' + recording['uniqueId'] + '.mp4'

		# 다운로드가 필요한지 확인. 파일이 없으면 다운로드. 파일이 있지만 0바이트이면 다운로드.
		if path.exists(storage + videofilename) == False: 
			doDownload = True
		elif path.exists(storage + videofilename) == True and os.path.getsize(storage + videofilename) > 0: 
			doDownload = False
		else: 
			doDownload = True

		# 다운로드 실행.
		if doDownload == True: 
			stream = arlo.StreamRecording(recording['presignedContentUrl'])
			with open(storage + videofilename, 'wb') as f:
				for chunk in stream:
					f.write(chunk)
				f.close()
			print('Downloaded: '+videofilename+' from '+recording['createdDate']+'.')
		# else: 
			# print('Skipped: '+videofilename+' from '+recording['createdDate']+'.')

	# Delete all of the videos you just downloaded from the Arlo library.
	# Notice that you can pass the "library" object we got back from the GetLibrary() call.
	# result = arlo.BatchDeleteRecordings(library)

	# If we made it here without an exception, then the videos were successfully deleted.
	# print('Batch deletion of videos completed successfully.')

except Exception as e:
    print(e)