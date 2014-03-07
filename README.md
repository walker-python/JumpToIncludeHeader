JumpToIncludeHeader
===================

Sublime Text 2 Plugins,select include file,then press f12 jump to C++ include file location.


First,copy jump_to_include_header.py to Sublime Text 2.0.2\Data\Packages\JumpToIncludeHeader\jump_to_include_header.py

Second,Click Preferences->Key Binding User,Add follow keys define.

{ "keys": ["f12"], "command": "jump_to_include_header",
    "args":{
      "options":{
        "user_search_path":[".", "include", "src",
        "C:/software/Python27/include"]
      }
    }
}

Third,you can modify Key Bindings User,set user_search_path for your project need,and modify jump_to_include_header.py sys_search_path for your global need.

Notice,you can execute "echo "#include <stdio.h> int main(){}" > t.c; g++ -v t.c; rm t.c" to get g++ header file search path.
  
BLOG: http://blog.csdn.net/infoworld/article/details/20748261
