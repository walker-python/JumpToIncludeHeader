import sublime, sublime_plugin
import re
import os
# get sys search Directory
# echo "#include <stdio.h> int main(){}" > t.c; g++ -v t.c; rm t.c

version  = "0.1"
jump_to_include_header_options = {}
jump_to_include_header_defaults = {
	"user_search_path":[".","include","src"],
	"sys_search_path":
	["c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/include/c++",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/include/c++/mingw32",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/include/c++/backward",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/../../../../include",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/include",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/include-fixed",
	"c:/e/software/mingw/bin/../lib/gcc/mingw32/4.4.0/../../../../mingw32/include",
	"c:/e/software/Lib/gui/wxWidgets-2.9.2/include",
    "c:/e/software/Lib/gui/wxWidgets-2.9.2/win32/release/share/include"
    ],
	"logging_enabled": False
}

def log(msg):
  global jump_to_include_header_options
  if not jump_to_include_header_options["logging_enabled"]:
    return

  global version
  print "JumpToIncludeHeader %s: %s" % (version, msg)

def assign_options(args):
  global jump_to_include_header_options
  global jump_to_include_header_defaults

  jump_to_include_header_options = jump_to_include_header_defaults
  for entry in args:
    jump_to_include_header_options[str(entry)] = args[str(entry)]

# todo: search current header dir
class JumpToIncludeHeaderCommand(sublime_plugin.TextCommand):
	def run(self, edit, options={"user_search_path":[],"logging_enabled": True,"sys_search_path":[]}):
		
		assign_options(options)
		window1 = self.view.window()
		
		view = window1.active_view()
		sel_header = view.sel()
		sel_str = view.substr(view.line(sel_header[0]))
		mode = '#include\s+[<\"]{1}([^>\"]+)[>\"]{1}'
		pattern = re.compile(mode)
		strMatch = pattern.findall(sel_str)
		if len(strMatch) == 0:
			log("No header file selected.")
			return
		search_path = jump_to_include_header_options["sys_search_path"] + jump_to_include_header_options["user_search_path"]
		# log(search_path)
		# 1.Add Project Dir
		folders = window1.folders()
		add_search_path = []
		for dir_path in search_path:
			if len(dir_path) >= 2 and dir_path[1] == ":":
					pass
			else:
				for folder in folders:
					add_search_path.append(folder+"/"+dir_path)

		# 2.Add Current File Dir
		search_path.append(os.path.dirname(view.file_name()))
		# 3.Merge Dir
		search_path = search_path+add_search_path

		log(search_path);
		finded = False
		for s in search_path:
			file_path = s + "/" + strMatch[0]
			# log("search file "+file_path);
			if os.path.exists(file_path):
				finded = True
				window1.open_file(file_path)
		if not finded:
			log("I can't find "+strMatch[0]);
