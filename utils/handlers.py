import os
import sys
from os.path import join,getsize
import hashlib


class Printer():
	"""
	Print things to stdout on one line dynamically
	"""
	
	def __init__(self,data):

		sys.stdout.write("\r\x1b[K"+data.__str__())
		sys.stdout.flush()


class SortList():
	"""
	Sort Lists
	"""

	def __init__(self,data):
		self.data = data
		
	def noCase(self,reverse=False):
		"Case insensitive forward sorting"
		self.r = reverse
		
		return self.data.sort(reverse=self.r,key=lambda t : tuple(s.lower() if isinstance(s,basestring) else s for s in t))


class Walker():
	"""
	Walk a given directory tree and generate some data
		takes in an ignore list that will filter out filenames with any of the ignore elements
	"""

	def __init__(self,directory,ignore=[],pathignore=[],defaults=False,type=''):

		self.directory = directory
		self.defaults = defaults
		self.type = type
		self.ignore = ignore
		self.ignorePath = pathignore
		self.data = []
		self.skipped = []

		if self.defaults:
			self.defaultIgnores = ['._']
			self.ignore = self.ignore+self.defaultIgnores

		self.extTypes = {
				'music' : ['.2sf', '.aac', '.aiff', '.als', '.amr', '.ape', '.asf', '.asx', '.au', '.aup', '.band', '.cdda', '.cel', '.cpr', '.cust', '.cwp', '.drm', '.dsf', '.dwd', '.flac', '.gsf', '.gsm', '.gym', '.iff-16sv', '.iff-8svx', '.it', '.jam', '.la', '.ly', '.m3u', '.m4a', '.m4p', '.mid', '.minipsf', '.mmr', '.mng', '.mod', '.mp1', '.mp2', '.mp3', '.mp4', '.mpc', '.mscz', '.mscz,', '.mt2', '.mus', '.musicxml', '.niff', '.npr', '.nsf', '.omf', '.optimfrog', '.ots', '.pac', '.pls', '.psf', '.psf2', '.psflib', '.ptb', '.qsf', '.ra', '.ram', '.raw', '.rka', '.rm', '.rmj', '.s3m', '.ses', '.shn', '.sib', '.smp', '.snd', '.sng', '.spc', '.speex', '.ssf', '.stf', '.swa', '.syn', '.tta', '.txm', '.usf', '.vgm', '.voc', '.vox', '.vqf', '.wav', '.wma', '.wv', '.xm', '.xspf', '.ym', '.zpl', '.3gp', '.aiff', '.alac', '.au', '.ivs', '.tta', '.aac', '.act', '.amr', '.atrac', '.awb', '.dct', '.dss', '.dvf', '.flac', '.gsm', '.iklax', '.m4a', '.m4p', '.mmf', '.mp3', '.mpc', '.msv', '.mxp4', '.ogg', '.ra', '.ram', '.raw', '.rm', '.vox', '.wav', '.wma'],
				'movies' : ['.iso','.3gp', '.aaf', '.asf', '.avchd', '.avi', '.cam', '.dat', '.dsh', '.divx', '.fcp', '.fla', '.flr', '.flv', '.gif', '.imovieproj', '.m1v', '.m2v', '.m4v', '.mkv', '.mng', '.mov', '.mp4', '.mpe', '.mpeg', '.mpg', '.mswmm', '.mxf', '.nsv', '.ogg', '.ogm', '.ogv', '.ppj', '.rm', '.roq', '.smi', '.sol', '.suf', '.svi', '.swf', '.veg', '.veg-bak', '.wmv', '.wrap'],
				'books' : ['.arg', '.azw', '.bmp', '.cbr', '.cbz', '.chm', '.djvu', '.doc', '.docx', '.epub', '.fb2', '.gif', '.html', '.html', '.jpg', '.lbr', '.lit', '.lrf', '.mobi', '.mp3', '.opf', '.pdb', '.pdf', '.pdg', '.png', '.rtf', '.tcr', '.tiff', '.tr3', '.txt']
			}

		self.doWalk()


	def doWalk(self):

		for root,dirs,files in os.walk(self.directory):
			for file in files:
				self.filterData(file) 
				self.filterPath(root)
				i = []
				for x in file,root,getsize(join(root,file)):
					i.append(x)
				if self.fileEncodeError or self.pathEncodeError or self.pathIgnoreHit or self.typeError or self.ignoreHit:
					self.skipped.append(i)
				else:
					self.data.append(i)
		
		SortList(self.data).noCase()
		SortList(self.skipped).noCase()


	def filterPath(self,element):
		self.pathIgnoreHit = False
		self.pathEncodeError = False

		if not self.ignorePath:
			pass

		else:
			for i in self.ignorePath:
				if i.lower() in element.lower():
					self.pathIgnoreHit = True
				else:
					pass
		try:
			element.encode('ascii')
		except:
			self.pathEncodeError = True


	def filterData(self,element):
		self.fileEncodeError = False
		self.typeError = False
		self.ignoreHit = False

		if self.defaults and self.type:
			try:
				sn = element.rsplit('.',1)
				ext = "."+sn[1].lower()	
			except:
				ext = "?"

			try:
				if ext not in self.extTypes[self.type]:
					self.typeError = True
			except:
				pass

		if not self.ignore:
			pass

		else:
			for i in self.ignore:
				if i.lower() in element.lower():
					self.ignoreHit = True
				else:
					pass

		try:
			element.encode('ascii')
		except:
			self.fileEncodeError = True


class Populate():
	"""
	Drop stuffs into the database.
	"""

	def __init__(self,data,obj,pathobj,formatobj,results=False):
		self.data = data
		self.obj = obj
		self.pathobj = pathobj
		self.formatobj = formatobj
		self.results = results
		self.error = []

		self.total = len(data)
		self.counter = 1.0
		
		for file in self.data:
			try:
				try:
					sn = file[0].rsplit('.',1)
					n,f = sn[0],sn[1]
				except:
					n,f = file[0],"?"

				p,s = file[1],file[2]

				thisPath = self.pathobj.objects.get_or_create(fullpath=p)[0]
				thisEntry = self.obj.objects.get_or_create(name=n,size=int(s),path=thisPath)[0]
				thisFormat = self.formatobj.objects.get_or_create(format=f)[0]
				thisEntry.formats.add(thisFormat)			

				thisResult = "Added %s -- %s" % (n,f)

			except:
				thisResult = 'Could not add file [ %s ]' % str(file[1]+file[0])
				self.error.append(thisResult)

			percentage = round(self.counter/self.total*100,3)
			output = " %f percent of %d  -- %s" % (percentage,self.total,thisResult)

			Printer(output)

			self.counter += 1	

		if self.results:
			self.items = self.obj.objects.all()


class ContentHash():
	"""
	MD5 sum file contents
	"""
	
	def __init__(self,f):
		self.f = f
		self.blocksize = 128
	
	def md5sum(self):
		obj = open(self.f,'r')
		md5 = hashlib.md5()
		while True:
			objData = obj.read(self.blocksize)
			if not objData:
				break
			md5.update(objData)
			
		return md5.digest()
		

class Hasher():
	"""
	Hash stuff. Duh!
	"""

	def __init__(self, *args):
		self.s = ""
		for a in args:
			self.s += a.__str__()

	def sha1(self):
		hash = hashlib.sha1(self.s).hexdigest()

		return hash
		
	def sha256(self):
		hash = hashlib.sha256(self.s).hexdigest()

		return hash

