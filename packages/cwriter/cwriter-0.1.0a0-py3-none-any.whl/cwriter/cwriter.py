import itertools
import re
import string
import textwrap
import os.path

try:
	from collections.abc import Iterable
except:
	from collections import Iterable



def paddedHex(padding=2):
	def fn(value):
		if value>=(1<<32): 
			return hex(value)
		elif value>=(1<<16): 
			minp = 8
		elif value>=(1<<8): 
			minp = 4
		else: 
			minp = 2

		pad = max(padding,minp)

		pad +=2 # to account for the 0x

		return f"{value:#0{pad}x}"

	return fn


def printableOrHex(padding=2, casting_fn=None):
	def fn(value):
		if 128>value>=32:
			return f"'{chr(value)}'"
	
		if value>=(1<<32): 
			return hex(value)
		elif value>=(1<<16): 
			minp = 8
		elif value>=(1<<8): 
			minp = 4
		else: 
			minp = 2

		pad = max(padding,minp)

		pad +=2 # to account for the 0x

		s = f"{value:#0{pad}x}"

		if casting_fn:
			s = casting_fn(value, s)

		return s

	return fn


def quotedStr(v):
	return '"'+(str(v).replace('\\',r'\\').replace('"',r'\"'))+'"'


def makeValidCIdentifier(txt):
	ident=[]
	valid = string.ascii_letters+string.digits
	prev_c = '_'
	for c in str(txt):
		if c not in valid:
			c = '_'
		if c == '_' and prev_c == '_':
			continue
		prev_c = c
		ident.append(c)

	if not ident:
		return None

	if ident[0] in string.digits:
		ident.insert(0,'n')

	return ''.join(ident)

def _captures_text(fn):
	def inner(self, *args, **kargs):
		r = fn(self, *args, **kargs)
		if r is not None:
			self._all_text.extend(r)
		return r
	return inner


class CIntType:
	sets = {
		'stdint': {
			True:{
				1: 'int8_t',
				2: 'int16_t',
				4: 'int32_t',
				8: 'int64_t'
			},
			False: {
				1: 'uint8_t',
				2: 'uint16_t',
				4: 'uint32_t',
				8: 'uint64_t'
			}
		},
		'int16': {
			True:{
				1:'char',
				2:'int',
				4:'long',
				8:'long long'
			},
			False:{
				1:'unsigned char',
				2:'unsigned int',
				4:'unsigned long',
				8:'unsigned long long'
			}
		},
		'int32': {
			True: {
				1: 'char',
				2: 'short',
				4: 'int',
				8: 'long'
			},
			False: {
				1: 'unsigned char',
				2: 'unsigned short',
				4: 'unsigned int',
				8: 'unsigned long'
			}
		}
	}


	class _CIntTypeInstance:
		def __init__(self, int_type, signed, bytes, ctype):
			self._int_type = int_type
			self._signed = signed
			self._bytes = bytes
			self._ctype = ctype

		@property
		def min_val(self):
			if self._signed:
				return -(1<<(8*self._bytes-1))
			else:
				return 0

		@property
		def max_val(self):
			if self._signed:
				return (1<<(8*self._bytes-1))-1
			else:
				return (1<<(8*self._bytes))-1

		@property
		def bytes(self):
			return self._bytes

		@property
		def is_signed(self):
			return self._signed
		
		@property
		def int_std_name(self):
			return self._int_type.int_std_name

		@property
		def ctype(self):
			return self._ctype

	def __init__(self, type_set="stdint"):
		try:
			self._set = self.sets[type_set]
		except KeyError:
			raise ValueError(f"Don't understand this int type: {type_set}")
		self._int_std_name = type_set


	@classmethod
	def analyze(cls, a, b):
		if b<a:
			a,b=b,a

		v = 256
		n = 1

		if a<0:
			while a<-(v>>1) or b>=(v>>1):
				nn = n<<1 # twice as many bytes
				while n < nn:
					v <<= 8
					n+=1
		else:
			while b>=v:
				nn = n<<1
				while n < nn:
					v <<= 8
					n+=1
		
		# returns: (is_signed, bytes)
		return a<0, n


	# does a naive replacement, not checking things like
	# whether the types appear in a string or more complex stuff
	def refactor(self, src_txt, from_repr='stdint', replace=None):
		assert(from_repr in self.sets)
		if self._int_std_name != from_repr:
			# replace identifiers like in32_t -> int
			mapping = {}
			from_set = self.sets[from_repr]
			to_set = self._set
			regex_parts = []
			for signed, bits in itertools.product((False, True), (8,4,2,1)):
				from_str = from_set[signed][bits]
				to_str = to_set[signed][bits]
				mapping[from_str] = to_str
				regex_parts.append(from_str.replace(' ','\s+'))

			regex = re.compile("(" + '|'.join(regex_parts) + ")(\s+)")
			src_txt = regex.sub(lambda mo: mapping[mo.group(1)] + mo.group(2), src_txt)

		# replace things like {{something}}
		if replace:
			mapping = {}
			regex_parts = []
			for k,v in replace.items():
				mapping[k] = v
				regex_parts.append(k)

			regex = "{{(" + '|'.join(regex_parts) + ")}}"

			regex = re.compile(regex)
			src_txt = regex.sub(lambda mo: mapping[mo.group(1)], src_txt)

		return src_txt


	@property
	def int_std_name(self): # was type
		return self._int_std_name


	def getCType(self, a, b=0):
		signed,b = self.analyze(a, b)
		return self._set[signed][b]


	def getCTypeInstance(self, a, b=0):
		signed, bytes = CIntType.analyze(a, b)
		ctype = CIntType.sets[self._int_std_name][signed][bytes]
		return self._CIntTypeInstance(self, signed, bytes, ctype)



class CFile:

	def __init__(self, filename, line_len=100, cpp_style=True):
		self._line_len = line_len
		self._all_text = []
		self._filename = filename
		self._cpp_style = cpp_style


	def clear(self):
		self._all_text = []


	def getAll(self):
		return self._all_text

	@_captures_text
	def openGuard(self, gname=None):
		gname = gname or self._getGuardName()
		if not gname: return None
		lines = []
		lines.append(f"#ifndef {gname}")
		lines.append(f"#define {gname}")
		lines.append("")
		return lines


	@_captures_text
	def closeGuard(self, gname=None):
		gname = gname or self._getGuardName()
		if not gname: return None
		lines = []
		lines.append("")
		lines.append(f"#endif /* {gname} */")
		return lines


	@_captures_text
	def raw(self, txt, dedent=True, trim_blanks=True):
		if dedent:
			txt = textwrap.dedent(txt)

		lines = txt.split('\n')

		if trim_blanks:
			a = 0
			b = len(lines)

			tot_lines = b
			while a<tot_lines and not lines[a].strip(): a+=1
			while b>a and not lines[b-1].strip(): b-=1
			lines = lines[a:b]

		return lines

	def _comment(self, msg, auto_wrap=True, indent=None, style=None):
		indent = indent or ""

		def wrap(txt_list, indent, pre=None, post=None):
			lines = []
			pre = indent+(pre or '')
			ln = self._line_len - (len(post) if post else 0)
			for t in txt_list:
				if post:
					lines.extend(m+post for m in textwrap.wrap(t, width=ln, initial_indent=pre, subsequent_indent=pre))
				else:
					lines.extend(textwrap.wrap(t, width=ln, initial_indent=pre, subsequent_indent=pre))
			return lines

		if isinstance(msg, str):
			msg = [msg]

		lines = []

		#----
		if style is None:
			if self._cpp_style and len(msg)<3: # allow cpp-style comments?
				style = 0
			elif len(msg)<3:
				style = 2
			else:
				style = 1

		#----

		beg = None # beginning of each line
		end = None # end of each line
		pre = None # before all lines
		post= None # after all lines

		if style == 0: # // at the beginning of each line
			beg = '// '
			end = None
		elif style == 1: # /* before first line, then * then */ after last line
			beg = ' * '
			pre = '/*'
			post= ' */'
		elif style == 2: # /* */ surrounding each line
			beg = '/* '
			end = ' */'

		if pre: 
			lines.append(indent+pre)

		if auto_wrap:
			lines.extend(wrap(msg,indent,beg,end))
		else:
			lines.extend(indent+beg+m+end for m in msg)

		if post:
			lines.append(indent+post)

		return lines

	@_captures_text
	def comment(self, msg, auto_wrap=True, indent=None, style=None):
		lines = self._comment(msg, auto_wrap, indent, style)
		return lines

	@_captures_text
	def define(self, macro, value=None):
		if value is None:
			value = ""
		lines = [f"#define {macro} {value}"]
		return lines

	@_captures_text
	def include(self, filename, sys_file=False):
		if sys_file:
			return [f"#include <{filename}>"]
		else:
			return [f"#include \"{filename}\""]


	@_captures_text
	def openNamespace(self, name):
		lines = [f"namespace {name} {{"]
		return lines

	@_captures_text
	def closeNamespace(self, name):
		lines = [f"}} /* namespace {name} */"]
		return lines

	@_captures_text
	def typedef(self, type_type, type_name, extra_attribs=None, extra_type=None):
		var = self._buildType(type_type, type_name, extra_attribs, extra_type)
		lines = []
		lines.append(f"typedef {var};")
		return lines

	@_captures_text
	def varDeclaration(self, var_type, var_name, extern=True, extra_attribs=None, extra_type=None):
		var = self._buildType(var_type, var_name, extra_attribs, extra_type)
		lines = []
		ex = "extern " if extern else ""
		lines.append(f"{ex}{var};")
		return lines
	
	@classmethod	
	def _iterData(cls, data, to_str_fn):
		if isinstance(data,dict):
			for n,kv in enumerate(data.items()):
				k,v = kv
				yield str(k)+':'+to_str_fn(v,n,k)
		else:
			for n,v in enumerate(data):
				yield to_str_fn(v,n,None)

	@classmethod	
	def _iterEnumData(cls, data):
		for d in data:
			if isinstance(d, tuple):
				yield f"{d[0]}={d[1]}"
			else:
				yield str(d)

	@classmethod	
	def _getToStrFn(cls, fn):
		if fn is None:
			return lambda s,n,k:str(s)
			
		n = fn.__code__.co_argcount

		if n>=3:
			return fn
		elif n==2:
			return lambda s,n,k:fn(s,n)
		elif n==1:
			return lambda s,n,k:fn(s)
		else:
			raise ValueError("A function that takes 1-3 arguments needed")


	def _outputArrayValues(self, var, open_close_chars, data, annotations, one_per_line, closing=';\n'):
		i_begin = open_close_chars[0]
		i_end = open_close_chars[1]

		vardef = var+i_begin

		if not annotations and (len(data)==1 or not one_per_line):
			# try to fit all data in a single line
			ln = len(vardef)+len(i_end)-1 # -1 for an extra , we're not adding
			for d in data:
				ln += 1+len(d) # +1 for each ,
				if ln > self._line_len:
					break
			else:
				ls = ', '.join(data)
				return [vardef+ls+i_end+";\n"]

		# nope, it has to be multiline
		lines = [vardef]

		indent = "    " 

		items = []

		pos = len(indent)
		has_an = False
		break_line = one_per_line
		for i,s in enumerate(data):
			
			has_an = annotations and (i in annotations)

			if ((len(s) + pos >= self._line_len) and items) or break_line or has_an:
				if items:
					lines.append(indent+(", ".join(items))+",")
					items = []
				pos = len(indent)

			break_line = one_per_line

			if has_an:
				an = annotations[i]
				if isinstance(an,tuple):
					msg,single_item = an
				else:
					msg,single_item = an,False
					
				lines.append("\n".join(self._comment(msg,indent=indent)))
				break_line = one_per_line or single_item

			items.append(s)
			pos += len(s)+2

		if items:
			lines.append(indent+(", ".join(items)) )
			
		lines.append(indent+i_end+closing)
		return lines



	# init type can be one of "list", "args" or "raw"
	@_captures_text
	def enum(self, var_type, var_name, data, extra_attribs=None, extra_type=None, annotations=None, one_per_line=False, typedef=None):
		if typedef is None:
			typedef = not self._cpp_style

		var = self._buildType(var_type, var_name, extra_attribs, extra_type)

		if typedef:
			closing = " "+var_name+';\n'
			opening = "typedef enum "+var+" "
		else:
			closing = ';\n'
			opening = "enum "+var+" "

		return self._outputArrayValues(opening,"{}", list(self._iterEnumData(data)), annotations, one_per_line, closing=closing)	


	# init type can be one of "list", "args" or "raw"
	@_captures_text
	def varDefinition(self, var_type, var_name, data=None, to_str_fn=None, init_type=None, extra_attribs=None, extra_type=None, annotations=None, one_per_line=False):
		var = self._buildType(var_type, var_name, extra_attribs, extra_type)

		if data is None:
			return [var]

		if not isinstance(data,Iterable) or isinstance(data,str):
			data = [data]
			if init_type is None:
				init_type='raw' if isinstance(data, str) else 'str'

		if init_type is None:
			init_type='list'

		i_begin, i_end = self._initType(init_type)
		to_str_fn = self._getToStrFn(to_str_fn)

		return self._outputArrayValues(var,(i_begin,i_end), list(self._iterData(data, to_str_fn)), annotations, one_per_line)	


	@_captures_text
	def newLine(self, number=1):
		return ['']*number


	def print(self):
		print('\n'.join(self._all_text))


	def write(self):
		with open(self._filename,"wt") as f:
			f.write('\n'.join(self._all_text))
			f.write("\n")

	
	def _initType(self, itype):
		if itype == 'list':
			return (' = {','}')
		if itype == 'args':
			return ('(',')')
		if itype == 'raw':
			return (' = ','')
		if itype == 'str':
			return (' = "','"')
		else:
			raise ValueError(f"Don't know how to apply initialization of type '{itype}'")


	def _getGuardName(self, tail="_GUARD"):
		if not self._filename: return None
		ident = makeValidCIdentifier(os.path.basename(self._filename))
		if ident is None: return None
		return ident.upper()+tail


	def _buildType(self, var_type, var_name, extra_attribs, extra_type):
		if not var_type:
			var_type = ""
		else:
			if isinstance(var_type, (list, tuple)):
				var_type = ' '.join(str(s) for s in var_type)
			else:
				var_type = str(var_type)

			if '[' in var_type:
				p = var_type.index('[')
				var_name += var_type[p:]
				var_type = var_type[:p]
			
		if extra_type:
			if isinstance(extra_type,(list,tuple)):
				extra_type = ' '.join(extra_type)

			var_type = extra_type + ' ' + var_type

		if var_type:
			v = [var_type,var_name]
		else:
			v = [var_name]
		if extra_attribs:
			if isinstance(extra_attribs,(list, tuple)):
				v.extend(extra_attribs)
			else:
				v.append(extra_attribs)
		return ' '.join(v)



if __name__=="__main__": # test
	numbers = [i for i in range(100)]

	f = CFile("example.h")

	f.openGuard()
	f.define("THIS",0)
	f.newLine()
	an = {5:"This is a message", 30:("Another message, but with single=True",True)}
	f.varDefinition("const int[]","values", numbers, to_str_fn=paddedHex(2), annotations=an)
	f.newLine(2)
	f.comment("This is a test comment")
	f.varDeclaration("const int[]","values")

	f.comment(["Now a multilne","comment","here"])
	f.varDefinition("const char[]","other",[1,2,3,4,5])
	f.varDefinition(["const", "char[]"],
					"var_name","this is a string",
					extra_attribs="__attribute__ ((aligned (16)))")
	f.closeGuard()

	f.print()
	f.write()

