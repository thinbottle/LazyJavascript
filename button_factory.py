from Tkinter import *
import shutil
import os

def attributesFromDict(d):
	self = d.pop('self')
	for n, v in d.iteritems():
		setattr(self, n, v)

class LabelButtonFactory(object):
	def __init__(self, label, frame, target_area, width=None, height=None):
		self.label = label 
		self.frame = frame 
		self.ta = target_area
		self.width = width
		self.height = height
		self.button = self.ret_button(self.ta, self.frame, self.label, self.width, self.height)
	
	def _label_wrap(self, label):
		return "<%s>" % label

	def _get_content(self, label):
		return self._label_wrap(label)

	def _make_command(self, target_area, label):
		cnt = self._label_wrap(label)
		cmd = lambda: target_area.insert(INSERT, cnt) 
		return cmd
	
	def ret_button(self, target_area, frame, label, width=None, height=None):
		cmd = self._make_command(target_area, label)
		if label == "\n":
			btn_name = "Enter"
		elif label == "\t":	
			btn_name = "Tab"
		else:
			btn_name = self._label_wrap(label)
		btn = Button(frame, text=btn_name, width=width, height=height, command=cmd )
		return btn

class AttrButtonFactory(LabelButtonFactory):
	def _label_wrap(self, label):
		return "%s" % label
	
class TemplateButtonFactory(LabelButtonFactory):
	def _label_wrap(self, label):
		return "{%% %s %%}" % label

#class DjangoTemplateButtonFactory(AttrButtonFactory):
#	def __init__(self, label, frame, target_area, content, width=None, height=None):
#		self.label = label 
#		self.frame = frame 
#		self.ta = target_area
#		self.cnt = content
#		self.width = width
#		self.height = height
#		self.button = self.ret_button(self.ta, self.frame, self.label, self.cnt, self.width, self.height)
	
#	def _make_command(self, target_area, label, content):
#		cnt = content
#		cmd = lambda: target_area.insert(INSERT, cnt)
#		return cmd
	
#	def ret_button(self, target_area, frame, label, content, width=None, height=None):
#		cmd = self._make_command(target_area, label, content)
#		btn_name = self._label_wrap(label)
#		btn = Button(frame, text=btn_name, width=width, height=height, command=cmd )
#		return btn
	
	
class ButtonFrame(object):
	def __init__(self, widget, target_area, label_list, btn_factory):
		self.widget = widget
		self.label_list = label_list
		self.ta = target_area
		self.btn_factory = btn_factory
		self.pack_button(self.widget, self.ta, self.label_list, self.btn_factory)
	
	def _get_frame(self, widget):
		frame_name = Frame(widget)
		frame_name.pack()
		return frame_name

	def pack_button(self, widget, ta, label_list, btn_factory):
		frame_name = self._get_frame(widget)
		max_btn_num = 6		
		btn_num = len(label_list)			
		row_num = btn_num/max_btn_num + 1
		for i in range(0, row_num):
			frame_tmp = Frame(frame_name)
			frame_tmp.pack()
			bgn = max_btn_num * i
			end = bgn + max_btn_num
			for label in label_list[bgn:end]:
				btn = btn_factory(label, frame_tmp, ta, 8, 1).button
				btn.pack(side=LEFT)

class LabelButtonFrame(ButtonFrame):
	def __init__(self, widget, target_area, label_list, btn_factory):
		self.widget = widget
		self.label_list = self.handle_label_list(label_list)
		self.ta = target_area
		self.btn_factory = btn_factory
		self.pack_button(self.widget, self.ta, self.label_list, self.btn_factory)

	def _sort_label_list(self, label_list):
		handle_element = lambda i : (i.startswith("/")) and  i[1:] or i			
		l1 = label_list
		l2 = [(i, handle_element(i)) for i in l1]
		l2.sort(key=lambda f:f[1])
		l3 = [i[0] for i in l2]
		return l3

	def handle_label_list(self, label_list):
		l_list = label_list
		l_list.extend([ "/"+i for i in l_list ])
		ret_list = self._sort_label_list(l_list)
		return ret_list

class MenuFunction(object):
	def __init__(self, target_area):
		self.target_area = target_area

	def hello(self):
		print "hello"

	def get_text(self):
		s = self.target_area.get('1.0', END)
		print "get_text : %s" % s
		#return target_area.get('1.0', END) 
		return s

	def create_template(self):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		text = self.get_text()
		tmp_file = open(template_file, 'w')
		tmp_file.write(text)
		tmp_file.close()
	
	def save_last_text(self):
		shutil.copy(template_file, tmp_file)
	
	def show_last_save_text(self):
		shutil.copy(tmp_file, template_file)
		
	def apache_restart(self):
		os.system("/etc/init.d/apache2 restart")    

if __name__ == '__main__':		
	root = Tk()
	root.title("Button Factory test")

	#init  target_area
	ta = Text(root)
	ta.pack(fill=X, side=TOP)

	#init some args
	templates_dir = '/opt/django/templetes'
	template_file = templates_dir + '/tktest.html'
	tmp_file = templates_dir + 'last_file_text'
	url = "http://127.0.0.1/tktest/"
	jqtest_1 = '{% extends "jq_base.html" %}\n{% block content %}\n\t<script>\n\n\t</script>\n{% endblock %}'

	#init menubar 
	menubar = Menu(root)
	menufunc = MenuFunction(ta)
	menubar.add_command(label="hello", command=menufunc.hello)
	menubar.add_command(label="create_template", command=menufunc.create_template)
	menubar.add_command(label="apache_restart", command=menufunc.apache_restart)
	menubar.add_command(label="get_text", command=menufunc.get_text)
	menubar.add_command(label="save", command=menufunc.save_last_text)
	menubar.add_command(label="show_last_save", command=menufunc.show_last_save_text)
	menubar.add_command(label="QUIT", command=root.quit)
	root.config(menu=menubar)

	#init button frame
	l_list =  ['html', 'body', 'p', 'div']
	l_list += ['ul', 'li', 'script','style'] 
	l_list += ['form', 'option','button','a']

	t_list =  ['extends', 'block', 'endblock']

	a_list =  ['$(', ')', '$("', '")','\n', '\t']
	a_list += ['content','document','window','var ', '$', 'text/javascript']
	a_list += ['alert(', ');', 'type=""', 'name=""', 'style=""','titile=""']
	a_list += ['.addClass("")','.removeClass("")', '.children("")']
	a_list += ['.show()', '.load()', '.ready()', '.hide()', '.end()', '.siblings()', '.click()']
	a_list += ['function(){\n\t\t}']
	a_list += [jqtest_1]


	attrBtnFrame = ButtonFrame(root, ta, a_list, AttrButtonFactory)
	labelBtnFrame = LabelButtonFrame(root, ta, l_list, LabelButtonFactory)
	djangoBtnFrame = ButtonFrame(root, ta, t_list, TemplateButtonFactory)
	#templatesBtnFrame = ButtonFrame(root, ta, d_list, AttrButtonFactory)
	#funcBtnFrame = ButtonFrame(root, ta, func_list, AttrButtonFactory)
	
	root.mainloop()
		
	

