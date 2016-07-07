# -*- encoding: utf-8 -*
import oss2
import sys,os,time
import os.path
import multiprocessing

auth = oss2.Auth('您的AccessKeyId', '您的AccessKeySecret')

	
class UploadOss(object):
	
	def __init__(self):
		self.updateTime = 12*60*60
		self.rootdir = 'E:\\Github\\hexoDemo\\public'
		self.bucket = 'dingxiaoyue'
		self.endpoint= 'http://oss-cn-shanghai.aliyuncs.com'
		
	def start(self):
		listenProcess = multiprocessing.Process(target=self.listenFile)
		listenProcess.start()
		while True:
			text = raw_input('')
			if text == 'quit':
					listenProcess.terminate()
					print('[*] quit')
					exit()
					
	def listenFile(self):		
		while True:
			bucket = oss2.Bucket(auth, self.endpoint, self.bucket)

			for parent,dirnames,filenames in os.walk(self.rootdir): 
				
				for filename in filenames:		
					try:
						localFilePath=os.path.join(parent,filename)
						ossFilePath=localFilePath.replace(self.rootdir,'').replace('\\','/').strip('/')					
						if time.time()-os.stat(localFilePath).st_mtime>self.updateTime:
							print ossFilePath + " is Not changed >> continue "	
							continue						
						result = bucket.put_object_from_file(ossFilePath, localFilePath)
						if result.status == 200:
							print ("%s successful" %ossFilePath)
						else:
							print ('%s Error' %ossFilePath)
					except expression as e:
						print str(e)
						raw_input("\n enter to exit")
						listenProcess.terminate() 
						exit	
			time.sleep(60)
if __name__ == '__main__':
	uposs = UploadOss()
	uposs.start()